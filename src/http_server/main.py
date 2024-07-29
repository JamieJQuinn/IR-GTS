from http_server import app

def main():
    app.run(host='0.0.0.0', port=80, debug=False)

if __name__ == '__main__':
    main()