"""
app.py — Flask 訂單管理系統
"""
import sqlite3
import os
import sys
import base64
from io import BytesIO
from datetime import date
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, g, jsonify
)

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.secret_key = 'order-mgmt-secret-2024'

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders.db')

# 自動檢查並初始化資料庫 (針對 Render 或全新部署環境)
if not os.path.exists(DATABASE):
    try:
        import create_db
    except Exception as e:
        print(f"[WARNING] 無法自動初始化資料庫: {e}")

# 管理員帳密
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'



# ═══════════════════════════════════════════════════════════════
#  資料庫連線
# ═══════════════════════════════════════════════════════════════

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ═══════════════════════════════════════════════════════════════
#  登入驗證裝飾器
# ═══════════════════════════════════════════════════════════════

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            flash('請先登入系統', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════
#  QR Code 產生
# ═══════════════════════════════════════════════════════════════

def generate_qr(data):
    """產生 QR Code 並回傳 base64 字串"""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=8, border=3)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='#1e293b', back_color='white')
        buf = BytesIO()
        img.save(buf, format='PNG')
        return base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        return None


# ═══════════════════════════════════════════════════════════════
#  登入 / 登出
# ═══════════════════════════════════════════════════════════════

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            session['username'] = username
            flash('登入成功！歡迎回來', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('帳號或密碼錯誤', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('已安全登出', 'info')
    return redirect(url_for('login'))


# ═══════════════════════════════════════════════════════════════
#  儀表板
# ═══════════════════════════════════════════════════════════════

@app.route('/')
@login_required
def dashboard():
    db = get_db()
    stats = {
        'customers': db.execute('SELECT COUNT(*) FROM customer').fetchone()[0],
        'products':  db.execute('SELECT COUNT(*) FROM product').fetchone()[0],
        'orders':    db.execute('SELECT COUNT(*) FROM orders').fetchone()[0],
        'pending':   db.execute("SELECT COUNT(*) FROM orders WHERE 狀態='處理中'").fetchone()[0],
    }
    recent_orders = db.execute('''
        SELECT o.*, c.名稱 AS 客戶名稱,
               COALESCE(SUM(oi.數量 * oi.單價), 0) AS 訂單總額
        FROM orders o
        JOIN customer c ON o.客戶編號 = c.客戶編號
        LEFT JOIN order_item oi ON o.訂單編號 = oi.訂單編號
        GROUP BY o.訂單編號
        ORDER BY o.訂單日期 DESC
        LIMIT 5
    ''').fetchall()
    return render_template('dashboard.html', stats=stats, recent_orders=recent_orders)


# ═══════════════════════════════════════════════════════════════
#  客戶管理
# ═══════════════════════════════════════════════════════════════

@app.route('/customers')
@login_required
def customers():
    rows = get_db().execute('SELECT * FROM customer ORDER BY 客戶編號').fetchall()
    return render_template('customers.html', customers=rows)


@app.route('/customer/add', methods=['GET', 'POST'])
@login_required
def customer_add():
    if request.method == 'POST':
        db = get_db()
        try:
            db.execute('INSERT INTO customer VALUES (?,?,?,?)',
                       (request.form['id'], request.form['name'],
                        request.form['phone'], request.form['address']))
            db.commit()
            flash('客戶新增成功', 'success')
            return redirect(url_for('customers'))
        except sqlite3.IntegrityError:
            flash('客戶編號已存在', 'danger')
        except Exception as e:
            flash(f'新增失敗：{e}', 'danger')
    return render_template('customer_form.html', action='add')


@app.route('/customer/edit/<cid>', methods=['GET', 'POST'])
@login_required
def customer_edit(cid):
    db = get_db()
    if request.method == 'POST':
        try:
            db.execute('UPDATE customer SET 名稱=?, 電話=?, 地址=? WHERE 客戶編號=?',
                       (request.form['name'], request.form['phone'],
                        request.form['address'], cid))
            db.commit()
            flash('客戶更新成功', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            flash(f'更新失敗：{e}', 'danger')
    customer = db.execute('SELECT * FROM customer WHERE 客戶編號=?', (cid,)).fetchone()
    if not customer:
        flash('找不到該客戶', 'warning')
        return redirect(url_for('customers'))
    return render_template('customer_form.html', action='edit', customer=customer)


@app.route('/customer/delete/<cid>')
@login_required
def customer_delete(cid):
    db = get_db()
    try:
        db.execute('DELETE FROM customer WHERE 客戶編號=?', (cid,))
        db.commit()
        flash('客戶已刪除', 'success')
    except Exception as e:
        flash(f'刪除失敗（可能有關聯訂單）：{e}', 'danger')
    return redirect(url_for('customers'))


# ═══════════════════════════════════════════════════════════════
#  商品管理
# ═══════════════════════════════════════════════════════════════

@app.route('/products')
@login_required
def products():
    rows = get_db().execute('SELECT * FROM product ORDER BY 商品編號').fetchall()
    return render_template('products.html', products=rows)


@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def product_add():
    if request.method == 'POST':
        db = get_db()
        try:
            db.execute('INSERT INTO product VALUES (?,?,?,?,?)',
                       (request.form['id'], request.form['name'],
                        float(request.form['price']), int(request.form['stock']),
                        request.form['category']))
            db.commit()
            flash('商品新增成功', 'success')
            return redirect(url_for('products'))
        except sqlite3.IntegrityError:
            flash('商品編號已存在', 'danger')
        except Exception as e:
            flash(f'新增失敗：{e}', 'danger')
    return render_template('product_form.html', action='add')


@app.route('/product/edit/<pid>', methods=['GET', 'POST'])
@login_required
def product_edit(pid):
    db = get_db()
    if request.method == 'POST':
        try:
            db.execute('UPDATE product SET 名稱=?, 單價=?, 庫存=?, 分類=? WHERE 商品編號=?',
                       (request.form['name'], float(request.form['price']),
                        int(request.form['stock']), request.form['category'], pid))
            db.commit()
            flash('商品更新成功', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash(f'更新失敗：{e}', 'danger')
    product = db.execute('SELECT * FROM product WHERE 商品編號=?', (pid,)).fetchone()
    if not product:
        flash('找不到該商品', 'warning')
        return redirect(url_for('products'))
    return render_template('product_form.html', action='edit', product=product)


@app.route('/product/delete/<pid>')
@login_required
def product_delete(pid):
    db = get_db()
    try:
        db.execute('DELETE FROM product WHERE 商品編號=?', (pid,))
        db.commit()
        flash('商品已刪除', 'success')
    except Exception as e:
        flash(f'刪除失敗（可能有關聯訂單）：{e}', 'danger')
    return redirect(url_for('products'))


# ═══════════════════════════════════════════════════════════════
#  訂單管理
# ═══════════════════════════════════════════════════════════════

@app.route('/orders')
@login_required
def orders():
    rows = get_db().execute('''
        SELECT o.*, c.名稱 AS 客戶名稱,
               COALESCE(SUM(oi.數量 * oi.單價), 0) AS 訂單總額
        FROM orders o
        JOIN customer c ON o.客戶編號 = c.客戶編號
        LEFT JOIN order_item oi ON o.訂單編號 = oi.訂單編號
        GROUP BY o.訂單編號
        ORDER BY o.訂單日期 DESC
    ''').fetchall()
    return render_template('orders.html', orders=rows)


@app.route('/order/add', methods=['GET', 'POST'])
@login_required
def order_add():
    db = get_db()

    if request.method == 'POST':
        try:
            order_id     = request.form['order_id']
            customer_id  = request.form['customer_id']
            order_date   = request.form['order_date']
            sales_person = request.form['sales_person']
            product_ids  = request.form.getlist('product_ids')

            if not product_ids:
                flash('請至少選擇一項商品', 'warning')
                raise ValueError('No products selected')

            # 新增訂單主檔
            db.execute('INSERT INTO orders VALUES (?,?,?,?,?)',
                       (order_id, customer_id, order_date, '處理中', sales_person))

            # 新增訂單明細（單價取商品表的當前價格）
            for pid in product_ids:
                qty = int(request.form.get(f'qty_{pid}', 0))
                if qty > 0:
                    price = db.execute(
                        'SELECT 單價 FROM product WHERE 商品編號=?', (pid,)
                    ).fetchone()['單價']
                    db.execute('INSERT INTO order_item VALUES (?,?,?,?)',
                               (order_id, pid, qty, price))

            db.commit()
            flash('訂單新增成功', 'success')
            return redirect(url_for('order_detail', order_id=order_id))

        except ValueError:
            pass  # flash already shown
        except Exception as e:
            db.rollback()
            flash(f'新增失敗：{e}', 'danger')

    # GET: 準備表單資料
    customers_list = db.execute('SELECT * FROM customer ORDER BY 客戶編號').fetchall()
    products_list  = db.execute('SELECT * FROM product ORDER BY 商品編號').fetchall()

    # 自動產生下一個訂單編號
    last = db.execute('SELECT 訂單編號 FROM orders ORDER BY 訂單編號 DESC LIMIT 1').fetchone()
    next_id = f'O{int(last["訂單編號"][1:]) + 1:03d}' if last else 'O001'

    return render_template('order_form.html',
                           customers=customers_list,
                           products=products_list,
                           next_id=next_id,
                           today=date.today().isoformat())


@app.route('/order/<order_id>')
@login_required
def order_detail(order_id):
    db = get_db()
    order = db.execute('''
        SELECT o.*, c.名稱 AS 客戶名稱, c.電話 AS 客戶電話, c.地址 AS 客戶地址
        FROM orders o
        JOIN customer c ON o.客戶編號 = c.客戶編號
        WHERE o.訂單編號 = ?
    ''', (order_id,)).fetchone()

    if not order:
        flash('找不到該訂單', 'warning')
        return redirect(url_for('orders'))

    items = db.execute('''
        SELECT oi.*, p.名稱 AS 商品名稱
        FROM order_item oi
        JOIN product p ON oi.商品編號 = p.商品編號
        WHERE oi.訂單編號 = ?
    ''', (order_id,)).fetchall()

    total = sum(item['數量'] * item['單價'] for item in items)

    # QR Code 內容 = 此訂單的完整 URL
    qr_url = request.url_root.rstrip('/') + url_for('order_detail', order_id=order_id)
    qr_base64 = generate_qr(qr_url)

    return render_template('order_detail.html',
                           order=order, items=items,
                           total=total, qr_base64=qr_base64)


@app.route('/order/<order_id>/status', methods=['POST'])
@login_required
def order_status_update(order_id):
    """AJAX 端點：更新訂單狀態"""
    new_status = request.form.get('status', '')
    valid = ['處理中', '已出貨', '已完成', '已取消']
    if new_status not in valid:
        return jsonify({'success': False, 'msg': '無效的狀態'}), 400

    db = get_db()
    db.execute('UPDATE orders SET 狀態=? WHERE 訂單編號=?', (new_status, order_id))
    db.commit()
    return jsonify({'success': True, 'status': new_status})


@app.route('/order/delete/<order_id>')
@login_required
def order_delete(order_id):
    db = get_db()
    try:
        db.execute('DELETE FROM order_item WHERE 訂單編號=?', (order_id,))
        db.execute('DELETE FROM orders WHERE 訂單編號=?', (order_id,))
        db.commit()
        flash('訂單已刪除', 'success')
    except Exception as e:
        flash(f'刪除失敗：{e}', 'danger')
    return redirect(url_for('orders'))


# ═══════════════════════════════════════════════════════════════
#  啟動
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        print('[WARNING] orders.db 不存在，請先執行 python init_db.py')
    app.run(debug=True, host='127.0.0.1', port=5000)
