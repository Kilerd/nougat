class Context(object):

    def __init__(self, path):

        # base
        self.path = path  # e.g. /hello?a=1
        self.__version = None  # http version
        self.url = None  # e.g. /hello

        # request
        self.method = None
        self.cookies = None
        self.headers = {}
        self.ip = None
        self.req_body = {}

        self.query = None
        self.query_string = None

        # params
        self.params = None

        # response
        self.res = None
        self.status = None


    @property
    def type(self):
        """
        the content type for request
        """
        return self.headers.get('CONTENT_TYPE', '').lower()

    def set_cookies(self, value):
        # TODO set cookies
        pass

    def set_secret_cookies(self, value):
        # TODO set secret cookies
        pass

    def set(self, key, value):
        """
        set response header
        :param key: the key of header
        :param value: the value of header
        """

        # TODO set function for header
        pass

    def url_for(self, name):
        """
        get the url according to the section name and handler name
        :param name: a string like section_name.handler_name
        :return: the url string
        """
        # TODO url for function
        pass

    def redirect(self, url, forever=False):
        """
        redirect to another page
        :param url: the page need to go
        :param forever: return 302 status code if False , otherwise return 301 status code
        """
        # TODO redirect function
        pass

    def __init__cookies(self):
        """
        从 self.heanders 中读取 Cookies 并且格式化进入 self.cookies
        """
        cookies = self.headers.get("Cookie", None) or self.headers.get("cookie", None)
        if cookies:
            cookies = cookies.split("; ")
            for one_cookies in cookies:
                if one_cookies != "":
                    one_cookies = one_cookies.split("=")
                    self.cookies[one_cookies[0]] = "=".join(one_cookies[1:])

    def __init_query(self, query):
        """
        格式化 query 的内容
        :param query:
        :return:
        """
        if query:

            querys = query.decode("utf-8").split("&")
            for each_query in querys:
                query_path = each_query.split("=")
                if len(query_path) >= 2:
                    self.__set_query(query_path[0], "=".join(query_path[1:]))

    def __set_query(self, key, value):
        if key in self.query:
            if not isinstance(self.query[key], list):
                temp = list()
                temp.append(self.query[key])
                self.query[key] = temp
            self.query[key].append(value)

        else:
            self.query[key] = value

    def init_body(self, body):
        """
        format body into different type
        :param body:
        :return:
        """
        # parse body as json
        if self.content_type == 'application/json':
            self.json = json.loads(body.decode())
            return

        if not self.content_type.startswith('multipart/'):
            pairs = parse_qsl(body.decode())
            for key, value in pairs:
                self.__set_body(key, value)
            return

        # TODO: from-data and file

    def __set_body(self, key, value):

        if key in self.body:
            if not isinstance(self.body[key], list):
                temp = list()
                temp.append(self.body[key])
                self.body[key] = temp
            self.body[key].append(value)

        else:
            self.body[key] = value

    def __get_msg(self, from_where, key, append=False):
        ret = None
        if from_where == 'cookie':
            return self.cookies.get(key, None)

        elif from_where == "query":
            ret = self.query.get(key, None)

        elif from_where == "form":
            ret = self.body.get(key, None)

        elif from_where == "header":
            return self.headers.get(key, None)

        if isinstance(ret, list):
            return ret if append else ret[-1]

        return ret

    def generate_params(self, route):
        """
        格式化参数
        :param route:
        :return:
        """
        for param in route.params:

            if param.name in route.url_params_dict:
                self.params.__setattr__(param.name, route.url_params_dict[param.name])
                continue

            for location in param.location:
                # pprint("{} {} {}", location, param.name, param.append)
                param_name = param.action or param.name
                param_content = self.__get_msg(location, param.name, param.append) or param.default

                self.params.__setattr__(param_name, param_content)
