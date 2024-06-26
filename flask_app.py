from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv; load_dotenv()
from utils import *
import os

application = Flask(import_name = __name__)
application.json.sort_keys = False

# env파일에서 OC 획득
OC = os.environ.get("OC")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if JWT_SECRET_KEY is None:
    # JWT_SECRET_KEY가 설정되지 않았을 경우
    makeNewJWTSecret()
    load_dotenv()
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# 제대로 설정되지 않았을 경우 경고용 메시지 출력
if OC == "test" or OC == None:
    print(".env파일 내 OC가 제대로 설정되지 않았습니다!\nThe OC in the .env file is not properly set up!")


# 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
application.config.update(
	DEBUG = False,
	JWT_SECRET_KEY = JWT_SECRET_KEY
)

# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(application)

# (디버그) 주석 해제시 jwt 인증을 해제함
#jwt_required = empty_decorator

# API 인증 확인용
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
    # 쿼리에서 idx값을 가져옴 (ResponseTooLarge방지용)
    idx = 0
    if request.args.get('idx') is not None:
        idx = int(request.args.get('idx'))
    
    # XML형식으로 반환할 경우 ResponseTooLarge오류가 발생할 수 있음. 
    # 따라서 형식 제거 후 반환
    basic_info_dict, article_list = parseLegalXML(apiCommonPart(request, OC, "law", "lawService"))
    CONTENT_MAX_LENGTH = 50
    ret_dict = basic_info_dict
    ret_dict["totalidx"] = len(article_list)//CONTENT_MAX_LENGTH
    ret_dict["idx"] = idx
    ret_list = article_list[(idx)*CONTENT_MAX_LENGTH:((idx)*CONTENT_MAX_LENGTH)+CONTENT_MAX_LENGTH]
    for t in ret_list:
        key, txt = t
        ret_dict[key] = txt
    return jsonify(ret_dict)

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