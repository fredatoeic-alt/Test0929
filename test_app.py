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
        yield client

def test_login_page():
    """測試未登入時訪問登入頁面"""
    app.config['TESTING'] = True
    with app.test_client() as anon_client:
        response = anon_client.get('/login')
        assert response.status_code == 200
        assert 'OrderPro'.encode('utf-8') in response.data

def test_dashboard(client):
    """測試儀表板頁面"""
    response = client.get('/')
    assert response.status_code == 200
    assert '儀表板'.encode('utf-8') in response.data

def test_customers_list(client):
    """測試客戶清單與 5 筆繁體中文測試資料"""
    response = client.get('/customers')
    assert response.status_code == 200
    assert '台灣半導體股份有限公司'.encode('utf-8') in response.data
    assert '長榮航空股份有限公司'.encode('utf-8') in response.data

def test_products_list(client):
    """測試商品清單與 5 筆測試資料"""
    response = client.get('/products')
    assert response.status_code == 200
    assert '無線藍牙耳機'.encode('utf-8') in response.data
    assert '人體工學椅'.encode('utf-8') in response.data

def test_orders_list(client):
    """測試訂單清單與狀態"""
    response = client.get('/orders')
    assert response.status_code == 200
    assert 'O001'.encode('utf-8') in response.data

def test_order_detail_and_qr(client):
    """測試專屬訂單頁面 /order/<id> 與 QR code 呈現"""
    response = client.get('/order/O001')
    assert response.status_code == 200
    assert 'O001'.encode('utf-8') in response.data
    assert '出貨單'.encode('utf-8') in response.data
    assert 'data:image/png;base64,'.encode('utf-8') in response.data

def test_order_status_update(client):
    """測試列表直接更新訂單狀態"""
    response = client.post('/order/O001/status', data={'status': '已完成'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['status'] == '已完成'

def test_order_historical_price_isolation(client):
    """驗證：商品改價不影響歷史訂單 order_item 的單價"""
    # 1. 取得現有訂單 O001 中的 P001 單價
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT 單價 FROM order_item WHERE 訂單編號='O001' AND 商品編號='P001'")
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

    # 3. 驗證歷史訂單 O001 中的 P001 單價未受影響
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT 單價 FROM order_item WHERE 訂單編號='O001' AND 商品編號='P001'")
    current_order_price = cur.fetchone()[0]
    conn.close()

    assert orig_order_price == current_order_price
