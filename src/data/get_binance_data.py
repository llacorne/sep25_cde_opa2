import src.apis.binance as binance
import pandas as pd
import binance_sdk_spot.rest_api.models as Models

class ExchangeInfos:
    def __init__(self, client: binance, data: Models.ExchangeInfoResponse | None):
        self.client=client
        self.ei=data

        # Extract symbols from exchangeInfos
        self.symbols=self.ei.symbols
        self.symbolsDf=pd.DataFrame([symbol.to_dict() for symbol in self.symbols])

    @classmethod
    def from_api(cls, client: binance):
        # Get only active symbols, with TRADING status
        exchangeInfos=client.getExchangeInfo(binance.DEFAULT_STATUS_SYMBOL)
        return cls(client, exchangeInfos)
    
    def getSymbolsKeys(self):
        return self.symbols.keys()

class Klines:
    def __init__(
        self,
        client: binance,
        symbol: str,
        interval: Models.KlinesIntervalEnum | None = None,
        limit: int | None = None,
        data: Models.KlinesResponse | None = None
    ):
        self.client=client
        self.symbol=symbol
        self.interval=interval
        self.limit=limit
        self.df=pd.DataFrame()

        # Binance indicates the last element is unused, so we remove it from the response.
        if data is not None:
            filtered_data=[d[:-1] for d in data]
            self.klines=filtered_data
            columns=['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'nbTrades', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume']

            self.df=pd.DataFrame(self.klines, columns=columns)

    @classmethod
    def from_api(
        cls,
        client: binance,
        symbol: str,
        interval: Models.KlinesIntervalEnum | None = None,
        limit: int | None = None
    ):
        klines=client.getKlines(symbol, interval, limit)
        return cls(client, symbol, interval, limit, klines)


ei=ExchangeInfos.from_api(binance)
klines=Klines.from_api(binance, symbol=binance.DEFAULT_SYMBOL)
