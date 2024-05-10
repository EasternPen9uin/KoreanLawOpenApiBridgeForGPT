from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv; load_dotenv()
from utils import *
import os

application = Flask(import_name = __name__)

# env파일에서 OC 획득
OC = os.environ.get("OC")
# 제대로 설정되지 않았을 경우 경고용 메시지 출력
if OC == "test" or OC == None:
    print(".env파일 내 OC가 제대로 설정되지 않았습니다!\nThe OC in the .env file is not properly set up!")

# 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
application.config.update(
	DEBUG = False,
	JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
)

# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(application)

# (디버그) 주석 해제시 jwt 인증을 해제함
#jwt_required = empty_decorator

@application.route("/")
@jwt_required()
def test_test():
    return "<h1>Flask is running!</h1>"

@application.route("/searchLaws")
@jwt_required()
def searchLaws():
    """
    법령 목록 검색
    """
    return apiCommonPart(request, OC, "law", "lawSearch")

@application.route("/getLawDetail")
@jwt_required()
def getLawDetail():
    """
    법률 내용 확인
    """
    # XML형식으로 반환할 경우 ResponseTooLarge오류가 발생할 수 있음. 
    # 따라서 형식 제거 후 반환
    return parseLegalXML(apiCommonPart(request, OC, "law", "lawService"))

@application.route("/searchPrecedent")
@application.route("/searchPrecedentByCaseNumber") #사건번호로 검색
@jwt_required()
def searchPrecedent():
    """
    판례 목록 검색
    """
    return apiCommonPart(request, OC, "prec", "lawSearch")

@application.route("/getPrecedentDetail")
@jwt_required()
def getPrecedentDetail():
    """
    판례 내용 확인
    """
    return apiCommonPart(request, OC, "prec", "lawService")

@application.route("/getLegalTerm")
#@jwt_required()
def getLegalTerm():
    """
    법령용어 확인
    """
    return apiCommonPart(request, OC, "lstrm", "lawService")

if __name__ == '__main__':
	application.run(host = '0.0.0.0', port = 5000, debug = True)