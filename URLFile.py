import re
import os
import sys
import mimetypes
import config


class EchoText:
    def __init__(self, s):
        self.str = s

    def append(self, s):
        self.str += s

    def __add__(self, other):
        self.str += other
        return self     # 仅修改可变对象成员变量，不修改对象ID，使得对象可以引用传递


class URLFile:
    def __init__(self, path, namespace):
        self.file_path = URLFile.get_file_path(path)
        with open(self.file_path, mode="rb") as f:
            self.content = f.read()
        self.dir_path = os.path.dirname(self.file_path)
        self.file_extension = re.search("\.([^.]*)\Z", self.file_path).group(1)
        self.file_type = mimetypes.guess_type(self.file_path)[0]
        self.py_file = re.sub("\.%s\Z" % self.file_extension, ".py", self.file_path, 0)
        if self.file_type != 'text/html' or not os.path.isfile(self.py_file):
            self.py_file = None
        namespace["send_header"]("Content-type", self.file_type)
        self.namespace = dict(namespace)    # 将namespace浅复制，避免杂乱信息混入，因为其中只有session变量为字典，浅复制后仍能有效读写

    @staticmethod
    def get_file_path(path):
        file_path = os.path.abspath(path)
        if not os.path.abspath(file_path).__contains__(config.DEFAULT_ROOT):
            file_path = config.PAGE_403
        elif not os.path.isfile(file_path):
            file_path = config.PAGE_404
        return file_path

    def process(self):
        os.chdir(self.dir_path)
        sys.path.append(self.dir_path)
        try:
            if self.py_file:
                exec("import traceback", self.namespace)
                exec(open(self.py_file, encoding="utf-8").read(), self.namespace)
            self.content = re.sub("<\?python[\s]([\s\S]*?)\?>", self.process_one, self.content.decode(config.ENCODING)).encode(config.ENCODING)
        except Exception as e:
            exec("traceback.print_exc()", self.namespace)
            print(e.args)
        os.chdir(config.DEFAULT_ROOT)
        sys.path.remove(self.dir_path)
        return

    def process_one(self, re_obj):
        echo_text = EchoText("")
        self.namespace["echo"] = echo_text.append
        self.namespace["cur_text"] = echo_text  # python对可变对象默认进行浅复制
        exec(re_obj.group(1), self.namespace)
        return echo_text.str
