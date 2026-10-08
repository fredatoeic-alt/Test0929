import pytest
import sqlite3
from app import app, DATABASE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['username'] = 'admin'
            sess['role'] = 'admin'
        yield client

def test_login_page():
    """測試訪問登入頁面"""
    app.config['TESTING'] = True
    with app.test_client() as anon_client:
        response = anon_client.get('/login')
        assert response.status_code == 200
        assert 'OrderPro'.encode('utf-8') in response.data

def test_login_hash_verification():
    """需求1：測試 werkzeug 密碼雜湊登入驗證"""
    app.config['TESTING'] = True
    # 正確密碼測試
    with app.test_client() as anon_client1:
        resp_correct = anon_client1.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        assert resp_correct.status_code == 200
        assert '登入成功'.encode('utf-8') in resp_correct.data

    # 錯誤密碼測試
    with app.test_client() as anon_client2:
        resp_wrong = anon_client2.post('/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
        assert '帳號或密碼錯誤'.encode('utf-8') in resp_wrong.data

def test_admin_login_required_protection():
    """需求2：測試未登入或非管理員存取後台被擋住並重定向至 /login"""
    app.config['TESTING'] = True
    with app.test_client() as anon_client:
        # 測試存取後台多個頁面
        for path in ['/', '/customers', '/products', '/orders', '/order/add']:
            resp = anon_client.get(path)
            assert resp.status_code == 302
            assert '/login' in resp.headers['Location']

def test_dashboard(client):
    """測試儀表板頁面"""
    response = client.get('/')
    assert response.status_code == 200
    assert '儀表板'.encode('utf-8') in response.data

def test_customers_list(client):
    """測試客戶清單與繁體中文測試資料"""
    response = client.get('/customers')
    assert response.status_code == 200
    assert '台灣半導體股份有限公司'.encode('utf-8') in response.data
    assert '長榮航空股份有限公司'.encode('utf-8') in response.data

def test_products_list(client):
    """測試商品清單與測試資料"""
    response = client.get('/products')
    assert response.status_code == 200
    assert '無線藍牙耳機'.encode('utf-8') in response.data
    assert '人體工學椅'.encode('utf-8') in response.data

def test_orders_list(client):
    """測試訂單清單與狀態 (SO001)"""
    response = client.get('/orders')
    assert response.status_code == 200
    assert 'SO001'.encode('utf-8') in response.data

def test_order_detail_and_qr(client):
    """測試專屬訂單頁面 /order/<id> 與 QR code 呈現"""
    response = client.get('/order/SO001')
    assert response.status_code == 200
    assert 'SO001'.encode('utf-8') in response.data
    assert '出貨單'.encode('utf-8') in response.data
    assert 'data:image/png;base64,'.encode('utf-8') in response.data

def test_order_status_update(client):
    """測試列表直接更新訂單狀態"""
    response = client.post('/order/SO001/status', data={'status': '已完成'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['status'] == '已完成'

from werkzeug.datastructures import MultiDict

def test_order_id_format_validation(client):
    """需求4：測試訂單編號 SO+數字 格式驗證"""
    # 測試非法格式 (例如 INVALID123)
    data_invalid = MultiDict([
        ('order_id', 'INVALID123'),
        ('customer_id', 'C001'),
        ('order_date', '2024-06-25'),
        ('sales_person', '測試人員'),
        ('product_ids', 'P001'),
        ('quantities', '1')
    ])
    resp_invalid = client.post('/order/add', data=data_invalid, follow_redirects=True)
    assert '訂單編號格式不正確'.encode('utf-8') in resp_invalid.data

    # 測試合法格式 SO999
    data_valid = MultiDict([
        ('order_id', 'SO999'),
        ('customer_id', 'C001'),
        ('order_date', '2024-06-25'),
        ('sales_person', '測試人員'),
        ('product_ids', 'P001'),
        ('quantities', '2')
    ])
    resp_valid = client.post('/order/add', data=data_valid, follow_redirects=True)
    assert resp_valid.status_code == 200
    assert 'SO999'.encode('utf-8') in resp_valid.data, f"Response content: {resp_valid.data.decode('utf-8')}"

def test_quantity_positive_integer_validation(client):
    """需求5：測試數量正整數驗證 (後端與資料庫)"""
    # 測試數量為 0
    resp_zero = client.post('/order/add', data=MultiDict([
        ('order_id', 'SO088'),
        ('customer_id', 'C001'),
        ('order_date', '2024-06-25'),
        ('sales_person', '測試人員'),
        ('product_ids', 'P001'),
        ('quantities', '0')
    ]), follow_redirects=True)
    assert '數量必須為正整數'.encode('utf-8') in resp_zero.data

    # 測試數量為負數 -5
    resp_neg = client.post('/order/add', data=MultiDict([
        ('order_id', 'SO088'),
        ('customer_id', 'C001'),
        ('order_date', '2024-06-25'),
        ('sales_person', '測試人員'),
        ('product_ids', 'P001'),
        ('quantities', '-5')
    ]), follow_redirects=True)
    assert '數量必須為正整數'.encode('utf-8') in resp_neg.data

    # 測試數量為小數 2.5
    resp_float = client.post('/order/add', data=MultiDict([
        ('order_id', 'SO088'),
        ('customer_id', 'C001'),
        ('order_date', '2024-06-25'),
        ('sales_person', '測試人員'),
        ('product_ids', 'P001'),
        ('quantities', '2.5')
    ]), follow_redirects=True)
    assert '數量必須為正整數'.encode('utf-8') in resp_float.data

def test_db_check_constraint():
    """需求5：測試資料庫 CHECK(數量 > 0) 約束"""
    conn = sqlite3.connect(DATABASE)
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO order_item VALUES ('SO001', 'P003', -1, 8900.0)")
        conn.commit()
    conn.close()

def test_order_historical_price_isolation(client):
    """驗證：商品改價不影響歷史訂單 order_item 的單價"""
    # 1. 取得現有訂單 SO001 中的 P001 單價
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT 單價 FROM order_item WHERE 訂單編號='SO001' AND 商品編號='P001'")
    orig_order_price = cur.fetchone()[0]
    conn.close()

    # 2. 修改商品 P001 的單價
    client.post('/product/edit/P001', data={
        'id': 'P001',
        'name': '無線藍牙耳機',
        'price': '9999.0',
        'stock': '150',
        'category': '3C電子'
    })

    # 3. 驗證歷史訂單 SO001 中的 P001 單價未受影響
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT 單價 FROM order_item WHERE 訂單編號='SO001' AND 商品編號='P001'")
    current_order_price = cur.fetchone()[0]
    conn.close()

    assert orig_order_price == current_order_price
