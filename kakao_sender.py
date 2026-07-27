# 나에게 카카오 메세지 보내주는 모듈
from urllib import response
from wsgiref import headers

import requests
import json
import os
from dotenv import load_dotenv
from weather_service import get_weather

# .env 파일 로드
load_dotenv()

# 환경 변수에서 카카오 API 키 가져오기
KAKAO_ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")
print(KAKAO_ACCESS_TOKEN)

# 카카오톡 메세지 전송 함수
def send_kakao_message(text: str) -> dict:
    # 토큰이 없으면 실행하지 않도록 예외를 발생시킵니다.
    if not KAKAO_ACCESS_TOKEN:
        raise RuntimeError("KAKAO_ACCESS_TOKEN이 설정되지 않았습니다.")

    # 요청
    template_object ={
        "object_type": "text",
        "text": text,
        "link" : {
            "web_url" : "https://developers.kakao.com",
        },
        "button_title": "확인",
    }

    # 인증 헤더를 만듭니다.
    # Bearer 토큰 방식으로 인증합니다.
    headers = {"Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}"}

    # 카카오 API에 전달할 데이터를 JSON 형태로 변환합니다.
    data = {"template_object": json.dumps(template_object)}
    print(data)

    # 카카오 메시지 전송 API에 POST 요청을 보냅니다.
    response = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers,
        data=data,
        timeout=10,
    )

    # 응답이 실패했으면 자세한 이유를 출력한 뒤 예외를 발생시킵니다.
    if response.status_code != 200:
        print(f"카카오 메시지 전송 실패: status={response.status_code}")
        print(response.text)

    response.raise_for_status()

    # 성공한 경우 JSON 응답을 반환합니다.
    return response.json()