from app import create_app

app = create_app('LOCAL')

if __name__ == '__main__':
    print('waiting to receive post request to /run_etl')
    app.run(app.config['HOST'], port=5001)
