from binance_common.configuration import ConfigurationRestAPI
from binance_common.constants import SPOT_REST_API_PROD_URL
from binance_sdk_spot.spot import Spot
import binance_sdk_spot.rest_api.models as Models
import binance_common.errors as Errors

from functools import wraps
from typing import TypeVar, Callable, ParamSpec, ParamSpecArgs, ParamSpecKwargs

DEFAULT_SYMBOL="ETHEUR"
DEFAULT_STATUS_SYMBOL=Models.ExchangeInfoSymbolStatusEnum.TRADING

configuration = ConfigurationRestAPI(base_path=SPOT_REST_API_PROD_URL)

client = Spot(config_rest_api=configuration)

P=ParamSpec("P")
R=TypeVar("R")

def safeApiCall(function: Callable[P, R])->Callable[P, R | None]:
    @wraps(function)
    def wrapper(*args: ParamSpecArgs, **kwargs: ParamSpecKwargs)->R | None:
        try:
            return function(*args, **kwargs)
        except Errors.ClientError as error:
            print(f'Binance api ClientError: {error}')
        except Errors.ServerError as error:
            print(f'Binance api ServerError: {error}')
        except Errors.Error as error:
            print(f'Binance api error: {error}')
        except Exception as error:
            print(f'Api exception: {error}')
        return None
    return wrapper

@safeApiCall
def checkConnectivity():
    response=client.rest_api.ping()
    return response.data()

@safeApiCall
def getExchangeInfo(status: Models.ExchangeInfoSymbolStatusEnum | None = None):
    '''
    show_permission_sets to False
    permissionsSet is a List of internal account/permissions group code
    probably useless for our bot
    '''
    response=client.rest_api.exchange_info(symbol_status=status, show_permission_sets=False)
    return response.data()

@safeApiCall        
def getKlines(
        symbol: str = DEFAULT_SYMBOL,
        interval: Models.KlinesIntervalEnum | None = None,
        limit: str | None = None
    ):
    if interval is None:
        interval=Models.KlinesIntervalEnum.INTERVAL_1h

    response=client.rest_api.klines(symbol, interval, limit)
    return response.data()
