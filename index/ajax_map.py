import json


# 在这个类里面写你需要的后端function，返回值必须是字符串，同时函数必须用@staticmethod声明为静态
class AjaxMapper:
    @staticmethod
    def test_func():
        return "hello"

    @staticmethod
    def test_json():
        res = {'a': [0, 1, 2, 3], 'b': ['x', 'y']}
        return json.dumps(res)  # json是一种结构化的字符串，注意json.dump是写入到文件，dumps才是写到字符串=_=

    @staticmethod
    def test_params(x, y):  # 需要参数直接定义，需要注意这里的参数在传输过程中经历了json转换，不敢保证数据类型不变=_=
        return str(x*y) # 必须返回字符串
