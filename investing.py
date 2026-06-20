import yfinance as yf  # 야후 파이낸스에서 주식 데이터를 가져오는 라이브러리 불러오기
stock = yf.Ticker("005930.KS")   # yf.Ticker() : 특정 주식을 지정하는 함수 # "005930.KS" : 삼성전자 종목코드 (.KS는 한국 주식 표시)
data = stock.history(period="1y")  # .history() : 주가 기록을 가져오는 함수 # period="1y" : 기간을 1년으로 설정 (1d=1일, 1mo=1달, 5y=5년)
print(data)  # 가져온 데이터를 터미널에 출력

