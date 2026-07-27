# 날씨 정보 가져오는 기능 모듈

import requests
import datetime
from dotenv import load_dotenv  # .env 파일 읽어오기 위함
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
SERVICE_KEY = os.getenv("WEATHER_API_KEY")

# 기상청 API 정보
BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

# 안성 3동 격자 좌표
nx = 65     # x 좌표
ny = 120    # y 좌표

def get_weather():
    # 현재 날짜와 시간 계산
    now = datetime.datetime.now()
    base_date = now.strftime("%Y%m%d")  # YYYYMMDD
    base_time = "1500"                  # 기상청 단기예보 기준 시간

    # 요청 parameter setting
    params = {
        "serviceKey" : SERVICE_KEY,     # 인증키
        "pageNo" : 1,                   # 페이지 번호
        "numOfRows" : 1000,               # 가져올 데이터 수
        "dataType" : "JSON",            # 응답 데이터 형식
        "base_date" : base_date,
        "base_time" : base_time,
        "nx" : nx,
        "ny" : ny,
    }

    # API 요청
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:     # 상태 (Error 200)
        data = response.json()  # JSON 데이터 파싱
        print(data)
        items = data["response"]["body"]["items"]["item"]

        # 날씨 정보 출력
        print("안성 3동의 날씨 정보:")
        for item in items:
            category = item["category"]
            value = item["obsrValue"]
            if category == "T1H" :  # 기온
                print(f"기온: {value}°C")
            elif category == "REH": # 습도
                print(f"습도: {value}%")
            elif category == "PTY": # 강수 정보
                precipitation = {
                    "0" : "ㄴㄴ",
                    "1" : "ㅇㅇ",
                    "2" : "비 아니면 눈 옴",
                    "3" : "눈 오던데?",
                    "4" : "ㅈㄴ옴",
                }
                print(f"비 오냐?: {precipitation.get(value, "알 수 없음")}")
    else:   # 예외 처리
        print(f"API 요청 실패: {response.status_code}")


if __name__ == "__main__":
    get_weather()