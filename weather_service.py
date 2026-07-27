# 날씨 정보 가져오는 기능 모듈

import datetime
import os
import  requests
from dotenv import load_dotenv
# .env 파일 로드
load_dotenv()

# 환경 변수에서 날씨 API 키 가져오기
SERVICE_KEY = os.getenv("WEATHER_API_KEY")

# 기상청 API 정보
BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

# 지역 격좌 좌표
NX = 65     # x 좌표
NY = 120    # y 좌표

# 날씨 정보 가져오는 함수
def get_weather_payload():
    now = datetime.datetime.now()
    base_date = now.strftime("%Y%m%d")

    # 매시각 10분마다 날씨가 갱신되기 때문에 시간 맞추기
    if now.minute < 10:
        base_time = (now - datetime.timedelta(hours=1)).strftime("%H") + "00"
    else:
        base_time = now.strftime("%H") + "00"

    # 요청 parameter setting
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": NX,
        "ny": NY,
    }

    # API 요청
    response = requests.get(BASE_URL, params=params, timeout=10)
    if response.status_code != 200:     # HTTP 요청 실패 시 예외 처리
        raise RuntimeError(f"API 요청 실패: {response.status_code}")

    data = response.json()  # JSON 응답을 파이썬 딕셔너리로 변환
    items = data["response"]["body"]["items"]["item"]

    # 날씨 정보 추출
    weather = {}
    for item in items:
        category = item["category"]
        value = item["obsrValue"]
        if category == "T1H":   # 기온
            weather["temp"] = float(value)
        elif category == "REH": # 습도
            weather["humidity"] = int(float(value))
        elif category == "PTY": # 강수형태
            weather["precipitation_type"] = value

    return {"time": now, "base_time": base_time, "weather": weather}

# 날씨 정보를 메시지 형식으로 변환
def format_weather_message(payload):
    weather = payload["weather"]                        # 날씨 정보 딕셔너리
    temp = weather.get("temp", "알 수 없음")             # 기온
    humidity = weather.get("humidity", "알 수 없음")     # 습도
    pty = weather.get("precipitation_type", "0")        # 강수형태(0~4)

    precipitation = {
        "0": "☀️",
        "1": "🌧️",
        "2": "🌨️",
        "3": "❄️",
        "4": "⛈️",
    }

    return (
        f"=={payload['time'].strftime('%H')}시 안성 3동 날씨==\n"
        f"기온: {temp}°C \n습도: {humidity}% \n강수상태: {precipitation.get(pty, '알 수 없음')}"
    )

# 날씨 정보를 가져와서 메시지로 반환하는 함수
def get_weather():
    payload = get_weather_payload()
    message = format_weather_message(payload)
    print(message)
    return message

if __name__ == "__main__":
    get_weather()
