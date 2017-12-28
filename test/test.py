
import requests
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
               "&wds=[]" + \
               "&dfwds=[]" + \
               "&k1=" + str(self._t.millisecond_timestamp())
        return data

    def _headers(self, code, sj):
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "JSESSIONID=E8C46D5E57DC44E277C4217BEA9EE862; u=2; _trs_uv=jbptw0bc_6_1eps; experience=show; td_cookie=18446744072380760463",
            "User-Agent": self._ua.ua_generator()['User-Agent'],
            "Host": "data.stats.gov.cn",
            "Referer": "http://data.stats.gov.cn/easyquery.htm?cn=C01&zb=" + code + "&sj=" + sj,
            "X-Requested-With": "XMLHttpRequest"
        }
        print(header)
        return header

    def request(self):
        url = "http://data.stats.gov.cn/easyquery.htm?" + self._post_data()
        req = requests.get(url=url, headers=self._headers(code="A0301", sj="LAST20"))
        # print(json.dumps(req.json(), indent=2).encode('utf-8').decode('unicode_escape'))

        name_list = []
        for name in req.json()['returndata']['wdnodes'][0]['nodes']:
            name_list.append(name['name'])
        print(name_list)


if __name__ == '__main__':
    s = DataSpider(pid='A0301', data_type='hgnd')
    s.request()
