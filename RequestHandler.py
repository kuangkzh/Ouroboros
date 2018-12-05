from http.server import BaseHTTPRequestHandler
import urllib.parse
import URLFile
import random


sessions = {}
global_variables = {}


class ResponseCode:
    def __init__(self, x):
        self.code = x

    def assign(self, x):
        self.code = x


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        gets = {}
        if '?' in self.path:
            gets = urllib.parse.parse_qs(urllib.parse.unquote(self.path.split('?', 1)[1]))
        request_headers = self.parse_headers(self.headers)
        cookies = self.parse_cookie(request_headers)
        response_headers = {}
        session = self.get_session(cookies, response_headers.__setitem__)
        response = ResponseCode(200)
        namespace = {"gets": gets, "posts": {}, "headers": request_headers,  # 请求参数
                     "session": session, "global_variables": global_variables,  # 用户变量和全局变量
                     "send_response": response.assign, "send_header": response_headers.__setitem__}  # 响应控制
        page = URLFile.URLFile(self.path.split('?')[0][1:], namespace)
        if page.file_type == 'text/html':
            page.process()
        self.send_response(response.code)
        for i in response_headers.keys():
            self.send_header(i, response_headers[i])
        self.end_headers()
        self.wfile.write(page.content)

    def do_POST(self):
        gets = {}
        if '?' in self.path:
            gets = urllib.parse.parse_qs(urllib.parse.unquote(self.path.split('?', 1)[1]))
        request_headers = self.parse_headers(self.headers)
        posts = urllib.parse.parse_qs(self.rfile.read(int(request_headers['content-length'])).decode())
        cookies = self.parse_cookie(request_headers)
        response_headers = {}
        session = self.get_session(cookies, response_headers.__setitem__)
        response = ResponseCode(200)
        namespace = {"gets": gets, "posts": posts, "headers": request_headers,  # 请求参数
                     "session": session, "global_variables": global_variables,  # 用户变量和全局变量
                     "send_response": response.assign, "send_header": response_headers.__setitem__}  # 响应控制
        page = URLFile.URLFile(self.path.split('?')[0][1:], namespace)
        if page.file_type == 'text/html':
            page.process()
        self.send_response(response.code)
        for i in response_headers.keys():
            self.send_header(i, response_headers[i])
        self.end_headers()
        self.wfile.write(page.content)

    @staticmethod
    def get_session(cookies, send_header):
        if cookies.__contains__("ssid") and sessions.__contains__(cookies["ssid"]):
            return sessions[cookies["ssid"]]
        else:
            ssid = str(random.randint(10000000, 100000000))
            while sessions.__contains__(ssid):
                ssid = str(random.randint(10000000, 100000000))
            sessions[ssid] = {}
            send_header("Set-Cookie", "ssid=%s" % ssid)
            return sessions[ssid]

    @staticmethod
    def parse_headers(request_headers):
        headers = {}
        for header in str(request_headers).split("\n"):
            key_value = header.split(": ")
            if len(key_value) > 1:
                headers[key_value[0].lower()] = key_value[1]    # 根据HTTP协议，headers不分大小写，故全部转换为小写
        return headers

    @staticmethod
    def parse_cookie(headers):
        cookies = {}
        if headers.__contains__("cookie"):
            for cookie in headers["cookie"].split("; "):
                key_value = cookie.split("=")
                cookies[key_value[0]] = key_value[1]
        return cookies
