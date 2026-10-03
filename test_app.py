import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """測試首頁是否能正常載入並回傳 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask" in response.data

def test_api_hello_with_name(client):
    """測試帶有訪客名稱的 API 問候功能"""
    response = client.post('/api/hello', json={'name': 'Freda'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'Freda' in data['message']

def test_api_hello_default(client):
    """測試未傳入訪客名稱時的預設問候功能"""
    response = client.post('/api/hello', json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'Hello, World!' in data['message']
