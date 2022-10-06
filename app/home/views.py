# views.py
from . import home_bp
import datetime
import time
from app.home.tools.home import main as Fm


@home_bp.route('/', strict_slashes=False)
def home():
    return '{"status": "healthy"}'


@home_bp.route('/run_etl', methods=['POST'], strict_slashes=False)
def run_etl():


    while True:

        try:
            Fm.run_coinbase()
        except Exception as error:
            dtmz = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{dtmz} Coinbase Failed')

        try:
            Fm.run_binance()
        except Exception as error:
            dtmz = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{dtmz} Binance Failed')

        time.sleep(60)