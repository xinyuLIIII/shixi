from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/get_video')
def get_video():
    # 假设这是从数据库或其他服务获取数据的逻辑
    video_url = "http://192.168.1.202:8080/test-live?port=11935&app=myapp&stream=test"
    code = 0  
    
    if code == 0:
        response = make_response(jsonify({"code": code, "video": video_url}), 200)
    else:
        # 如果code不为0，视为异常情况
        response = make_response(jsonify({"code": code, "error": "Something went wrong"}), 400)
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
