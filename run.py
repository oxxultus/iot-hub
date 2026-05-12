from app import create_app

app = create_app()

if __name__ == '__main__':
    # IoT 허브 특성상 여러 클라이언트 접속을 위해 threaded=True 권장
    app.run(host='0.0.0.0', port=5000, debug=True)
