from app import create_app

app = create_app('PROD')

if __name__ == '__main__':
    app.run(app.config['HOST'])
