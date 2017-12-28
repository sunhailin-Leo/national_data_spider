
import json
import http.cookiejar
import requests
import urllib.request as ur
from utils.time_util import TimeUtil
from utils.UserAgentMiddleware import UserAgentRotate


class DataSpider:
    def __init__(self, pid: str, data_type):
        """
        :param pid: pid是爬取的表的id
        """
        self._pid = pid

        # 对应数据长度选项表(目前都选最后一个)
        self._year = ['LAST5', 'LAST10', 'LAST20']
        self._season = ['LAST6', 'LAST12', 'LAST18']
        self._month = ['LAST13', 'LAST24', 'LAST36']

        # 需要知道链接所对应数据是年度、季度、月度
        self._data_type = data_type

        # 时间类
        self._t = TimeUtil()
        # UA
        self._ua = UserAgentRotate()

    def _post_data(self):
        data = "m=QueryData" \
               "&dbcode=" + self._data_type + \
               "&rowcode=zb" + \
               "&colcode=sj" + \
               "&wds=%5B%5D" + \
               "&dfwds=%5B%5D" + \
               "&k1=" + str(self._t.millisecond_timestamp())
        return data

    def _headers(self, code, sj):
        header = {
            # "Cookie": "JSESSIONID=" + "93D5EF6A590E6C88484541C713421744" + "; u=1; _trs_uv=jbq43j3c_6_jy4b;",
            "Cookie": "u=1; _trs_uv=jbq43j3c_6_jy4b; acmrAutoLoginUser=\"379978424@qq.com\"; acmrAutoSessionId=D63B7EAE94D941A4207DC1140B7DCA47; JSESSIONID=D63B7EAE94D941A4207DC1140B7DCA47",
            "User-Agent": self._ua.ua_generator()['User-Agent'],
            "Host": "data.stats.gov.cn",
            "Referer": "http://data.stats.gov.cn/easyquery.htm?cn=C01&zb=" + code + "&sj=" + sj
        }
        print(header)
        return header

    def request(self):
        cookie = http.cookiejar.CookieJar()
        handler = ur.HTTPCookieProcessor(cookie)
        opener = ur.build_opener(handler)

        # page_url = "http://data.stats.gov.cn/easyquery.htm"
        # req = ur.Request(method="POST", url=page_url, headers={'User_Agent': self._ua.ua_generator()['User-Agent']})
        # html = ur.urlopen(req)
        # session_id = html.getheader('Set-Cookie').split(";")[0].replace("JSESSIONID=", "")
        # print(session_id)

        data_url = "http://data.stats.gov.cn/easyquery.htm?" + self._post_data()
        print(data_url)
        req = ur.Request(method="POST", url=data_url, headers=self._headers(code="A0301", sj="LAST20"))
        req.set_proxy(host="219.235.129.199:80", type="http")

        # print(json.dumps(req.json(), indent=2).encode('utf-8').decode('unicode_escape'))
        response = opener.open(req, timeout=10)
        json_res = response.read().decode("UTF-8")

        name_list = []
        for name in json.loads(json_res)['returndata']['wdnodes'][0]['nodes']:
            name_list.append(name['name'])
        print(name_list)


if __name__ == '__main__':
    s = DataSpider(pid='A0301', data_type='hgnd')
    s.request()
