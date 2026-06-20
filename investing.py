import yfinance as yf  # import: 외부 라이브러리를 불러옴. as yf: yfinance를 yf라는 별명으로 사용
from notion_client import Client  # from: notion_client 라이브러리 안에서 Client 클래스만 가져옴
from datetime import datetime  # from: datetime 라이브러리 안에서 datetime 클래스만 가져옴
from dotenv import load_dotenv  # from: dotenv 라이브러리 안에서 load_dotenv 함수만 가져옴
import os  # os 모듈 불러옴 (운영체제 기능 사용, 여기선 환경변수 읽으려고)

load_dotenv()  # 함수 호출: .env 파일을 읽어서 환경변수로 등록

notion = Client(auth=os.getenv("NOTION_TOKEN"))  # Client 클래스로 객체 생성. os.getenv(): 환경변수에서 토큰값 읽어옴
DATABASE_ID = "385f5b90c2f080a7bd96c75d1986e198"  # 문자열 변수: 노션 DB 주소 저장

# 딕셔너리(key:value 쌍): 한글 종목명을 key, yfinance 티커 심볼을 value로 매핑
TICKERS = {
    "다우지수": "^DJI",
    "S&P500": "^GSPC",
    "나스닥": "^IXIC",
    "코스피": "^KS11",
    "엔비디아": "NVDA",
    "비스트라에너지": "VST",
    "SK하이닉스": "000660.KS",
    "삼성전자": "005930.KS",
}

def get_price(ticker):  # def: 함수 정의. ticker를 매개변수로 받아서 가격과 변동률을 반환
    data = yf.Ticker(ticker)  # yf.Ticker(): 티커 심볼로 종목 객체 생성
    hist = data.history(period="2d")  # .history(): 종목의 주가 기록을 DataFrame으로 가져옴. period="2d": 2일치
    close = hist["Close"]  # DataFrame에서 "Close"(종가) 컬럼만 추출
    today = close.iloc[-1]  # iloc[-1]: 리스트 맨 마지막 값 = 가장 최근 종가
    prev = close.iloc[-2]  # iloc[-2]: 뒤에서 두번째 값 = 하루 전 종가
    change = ((today - prev) / prev) * 100  # 변동률 공식: (오늘-어제)/어제 * 100
    return round(today, 2), round(change, 2)  # return: 두 값을 튜플로 반환. round(): 소수점 2자리 반올림

def add_to_notion(date, ticker_name, price, change):  # def: 함수 정의. 4개 매개변수 받음
    notion.pages.create(  # notion 객체의 pages.create() 메서드 호출: DB에 새 행 추가
        parent={"database_id": DATABASE_ID},  # 딕셔너리: 어떤 DB에 넣을지 지정
        properties={  # 딕셔너리: DB 컬럼별로 넣을 값 지정
            "날짜": {"date": {"start": date}},  # 중첩 딕셔너리: Notion date 타입 형식
            "종목": {"title": [{"text": {"content": ticker_name}}]},  # title: DB의 메인 컬럼 타입
            "가격": {"number": price},  # number 타입
            "변동률": {"number": change},  # number 타입
        }
    )

today = datetime.today().strftime("%Y-%m-%d")  # datetime.today(): 현재 시각 객체 생성. strftime(): 날짜를 "2026-06-21" 문자열 형식으로 변환

for name, ticker in TICKERS.items():  # for문: TICKERS 딕셔너리를 순회. .items(): key,value 쌍으로 꺼냄
    price, change = get_price(ticker)  # 함수 호출 후 반환값을 두 변수에 언패킹
    add_to_notion(today, name, price, change)  # 함수 호출: 노션에 데이터 입력
    print(f"{name}: {price} ({change}%)")  # f-string: 변수를 문자열 안에 삽입해서 출력