from weather_service import get_weather
from kakao_sender import send_kakao_message

# 직접 이 파일을 실행했을 때만 아래 코드가 실행됩니다.
if __name__ == "__main__":
    message = get_weather()
    send_kakao_message(message)
    print("카카오톡 전송 완료")