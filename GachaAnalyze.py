# This is an open source Genshin Impact avatar judgement system written by a749014(秋胜春朝)
# source link:https://github.com/a749014/TeyvatToolKit
# blog:https://a749014.github.io/
import os
from urllib import parse
from urllib import request
import json
from pprint import pprint
path=os.path.dirname(os.path.abspath(__file__))
def getlink():
    pass
class GachaAnalyser():
    def __init__(self,url):
        '''load key data to run the program
        url：gacha link from function getlink()'''
        self.url = url
        self.query_dic = parse.parse_qs(parse.urlparse(self.url).query)
        self.query_dic = {key: self.query_dic[key][0] for key in self.query_dic}
        print(self.query_dic)

        self.page = 1
        self.size = 6
        self.end_id = 0

        self.query_dic['gacha_type'] = '301'
        self.query_dic['page'] = str(self.page)
        self.query_dic['size'] = str(self.size)
        self.query_dic['end_id'] = str(self.end_id)

        self.get_url = 'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?' + parse.urlencode(self.query_dic)
        self.calculate_count=0

        self.display_count = 0
        self.all_data=[]
        self.golds={}#format:{avatar name : location from first page}
        
    def getdata(self):
        '''get the data from link and analyze'''
        while True:
            try:
                #get the data from link
                self.res = request.urlopen(self.get_url)
                if self.res.getcode() != 200:
                    print('error')
                    return 
                self.js = json.loads(self.res.read().decode('utf-8'))
                self.data_dict = self.js['data']
                items=int(self.data_dict['size'])
                self.calculate_count += items

                self.gacha_list = self.data_dict['list']
                t=0
                pprint(self.gacha_list)
                #analyze
                for i in self.gacha_list:
                    t+=1
                    self.all_data.append(i)
                    if i['rank_type']=='5':
                        self.golds[i['name']]=self.calculate_count-items+t
                #next page
                self.page += 1
                self.end_id = self.gacha_list[-1]['id']
                self.query_dic['page'] = str(self.page)
                self.query_dic['end_id'] = str(self.end_id)
                self.get_url = 'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?' + parse.urlencode(self.query_dic)
                
            except IndexError:
                #finish
                return self.golds
    def chartGen(self,d:dict):
        '''An echart render function based on pyecharts . d:all of the keys will be the x axis,values will be the y axis'''
        pass

    def create_bar_chart(data_dict, chart_title):
        # 提取字典的键和值
        categories = list(data_dict.keys())
        values = list(data_dict.values())
        
        # 创建柱状图对象
        bar = Bar(chart_title)
        
        # 添加数据到柱状图
        bar.add("", categories, values, mark_line=["average"], is_label_show=True)
        
        # 渲染图表到HTML文件或直接显示在Jupyter Notebook中
        bar.render("bar_chart.html")

if __name__=='__main__':
    g=GachaAnalyser('https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?win_mode=fullscreen&authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=d11a3d00ce31d1b04319cd516bda53ac214b31bc&timestamp=1688515164&lang=zh-cn&device_type=pc&game_version=CNRELWin3.8.0_R16698153_S16388687_D16994144&plat_type=pc&region=cn_gf01&authkey=qAuDXuZPI1xVbvlVh5X0Z%2bBhucejjraLuEqhs0EFi5o3oB%2fQpGKBqwG%2bwsSP1TlTpZ3QS%2felP2DEguZ99NqjCqYTE%2fv5GpsI6YwO1t%2ffpZTrnmEzPDTOBtyFG2FKsUuWMdbIhycYRvyKk1ZUyTRTp8ZyI1ZRqy3GI86LVRvhDsU%2b4RJVRUMxYcgs7zv1bdcx38syd3R0lH1lgMwYWM%2fQrY5%2bZxLFAkfUVeoqcfjpshVgPJSMCvTsxUtXDkVWouDjks1yVuk2U%2f6XQhIMmdwcd6rfdMw7Yd%2b%2fRHslutEaUaJ8sOQ80LTw8RtEuoFQAduIoCb9s4e7zOhCBayW4jGxZc1xXvw%2bw5ChoIq%2f3k1WrKjxdCsJRbsTGE3bwk0VVaoBTbnPDhNDcwsjUE6%2felGkBNxgnOIWkherJ6rkbQnPx%2ffw2nm5fcmjOBjOBGzGMUvyPDIAlBvbYvgg9M0siNrVB%2bdcNvMTgBfqYpHcSn46iv0BiZyQeNSngIoI%2bbtA4FaMX3Pfunt2J8J4fdhbtZBhzX0TEzYLY0JDidSQkDn5DG0%2feC%2ffgQM2SPJOIPvb742JE35xRbCOWC8B0xykcvlTazXEKpCYGWIdGQ%2bAp%2fMENj7DJqZ0oPu5IhY4Kw%2be6ry1n1YbZyOTZ9%2bNgsqgO5MXiAinOpTRmsbSxJrjisJZRSU6rogGTnDxkC8tKC5s6Y%2fx6dFLLbS9RMz2P7J%2fV%2fa3TD%2fMQ0XOLzjSpal6KpX%2fK4%2foyFQVZqdFc8f77nim9SHvVHk%2fZj2HvAZlVyzl%2fb9V6Hmoe9LtUHL49s%2bdr3JBEyAWyXGx00K3mTohe0SO3sb2gBAjVgv37YgWj%2ftYXJllDGMBWZbZCSPR5ifKj%2f%2fsKmwJIch5xyX4ZDBfYOUFVvo8xlhjoAQYaBbLiMLTpIDN9G7s5y9arLJviA4XwZxT62uxZL4BVmTJyJKV6HF481VY1FgOUm%2fUfmNqQHSiwFmrYbYe%2b73XOENt%2bAi%2bA4lm%2bv%2bA84a4OuufYBeJRxGe90FO&game_biz=hk4e_cn')
    g.getdata()
    print(g.calculate_count)
    print(g.golds)