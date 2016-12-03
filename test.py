import stockAnalyzer

stocks = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM", "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE", "BAC"]
for stock in stocks:
    print stock + ": "
    print stockAnalyzer.growthProbability(stock)
