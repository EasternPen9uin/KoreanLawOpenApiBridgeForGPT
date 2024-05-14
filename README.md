# KoreanLawOpenApiBridgeForGPT

## Description

2024 인문사회통합성과확산센터 아이디어 공모전 출품용 "법률 인공지능 챗봇 구현 가능성 검토(가제)" 아이디어 제안서에 활용할 국가법령정보 공동활용 API (https://open.law.go.kr/) 중계 백엔드 서버 및 Action 코드

## Installation
* [Python](https://www.python.org/downloads/)을 설치해주세요.

* 라이브러리 설치
  ```bash
  git clone https://github.com/username/repository.git
  cd repository
  pip install -r requirements.txt
  ```

* 리포지토리 내 ActionScheme.json 파일은 Action의 Scheme입니다. 

## Run
* API 키 발급 : Action 사용시 인증 유형을 'API 키', 'Bearer'로 설정한 후 아래 명령어 실행 후 나오는 문자열을 API키로 사용하세요.
  ```bash
  py get_api_key.py
  ```

* 실행
  ```bash
  # 주의 : 실사용시에는 아래 코드 대신 gunicorn등의 WSGI를 사용해주시기 바랍니다.
  py flask_app.py
  ```