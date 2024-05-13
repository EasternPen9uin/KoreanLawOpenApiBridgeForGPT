def apiCommonPart(request, oc, target, do):
    # 전체 쿼리 스트링을 가져옴
    full_query_string = request.query_string.decode('utf-8')
    # 고정값
    CONSTANT_STRING :str = f"target={target}&OC={oc}&type=XML"
    
    # 입력받은 쿼리를 사용하여 API 요청 보내고 응답 받기
    url = f"https://www.law.go.kr/DRF/{do}.do?{CONSTANT_STRING}&{full_query_string}"
    response = sendGetRequest(url)
    # 응답 반환
    return response

def sendGetRequest(url):
    """
        GET 요청을 보내고 응답을 (주의)문자열로 받는 함수
    """
    import urllib.request
    with urllib.request.urlopen(url) as response:
        # 응답의 바디를 utf-8로 디코딩하여 출력합니다.
        response_body = response.read().decode('utf-8')
        return response_body

def parseLegalXML(xml_string):
    """
        법 조문(XML)을 dict형태로 바꾸는 함수
    """
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(xml_string)
    
    # 반환할 dict
    ret_dict = {}
    # 반환할 list
    ret_list = []

    # 기본정보 dict에 입력
    basic_info = tree.find("기본정보")
    basic_info_key_list = ["법령명_한글", "시행일자", "공포번호", "공포일자", "소관부처"]
    for key in basic_info_key_list:
        ret_dict[key] = basic_info.find(key).text

    # 조문 내용 입력시 사용하는 재귀함수
    def write_tag_contents(string_io, xml_node):
        '''"내용"이라는 단어가 포함된 태그의 텍스트를 재귀적으로 찾아서 출력하는 함수'''
        if "내용" in xml_node.tag:
            string_io.write(xml_node.text.strip())
            string_io.write('\n')
        # 현재 노드의 모든 자식 노드에 대해서도 같은 작업을 반복
        for child in xml_node:
            write_tag_contents(string_io, child)

    # 리스트에 조문 입력
    articles = tree.find("조문").findall("조문단위")
    for atc in articles:
        if atc.find("조문여부").text == "조문":
            key_name = f'Article {atc.find("조문번호").text}'
            content = atc.find("조문내용").text
            content = content[content.find("("):]
            if atc.find("항") is not None:
                import io
                sio = io.StringIO()
                for hang in atc.findall("항"):
                    write_tag_contents(sio, hang)
                content+=sio.getvalue()
                sio.close()
            ret_list.append((key_name, content))

    return ret_dict, ret_list

def empty_decorator():
    """
        디버그용 빈 데코레이터
    """
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator