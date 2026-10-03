import sys
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    """首頁路由：渲染一頁式網站模板"""
    server_info = {
        'python_version': sys.version.split()[0],
        'flask_version': '3.1.2',
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render_template('index.html', info=server_info)

@app.route('/api/hello', methods=['POST'])
def api_hello():
    """API 端點：接收前端訪客姓名並回傳客製化 Hello World 問候訊息"""
    data = request.get_json(silent=True) or {}
    visitor_name = data.get('name', '').strip()
    
    if not visitor_name:
        greeting = "Hello, World! 歡迎探索 Flask 的精彩世界！(freda5)"
    else:
        greeting = f"Hello, {visitor_name}! 很高興認識你，祝你有美好的一天！(freda5)"
    
    return jsonify({
        'status': 'success',
        'message': greeting,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

if __name__ == '__main__':
    # 啟動本機開發伺服器，開啟 debug 模式便於除錯
    print("Flask 網站正在啟動中...")
    print("請在瀏覽器開啟: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
