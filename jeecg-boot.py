import mitmproxy.http
import re
import csv

class Counter:
    def __init__(self):
        self.num = 0
    def response(self, flow: mitmproxy.http.HTTPFlow):
        text=flow.response.get_content()
        if "VUE_APP_API" in str(text):                        #指纹识别，确定jeecg-boot站点
            index=str(text).find("VUE_APP_API_BASE_URL") 
            pattern=r"VUE_APP_API_BASE_URL:\"(.+)\","         #正则匹配，提取真实jeecg-boot接口
            match=re.search(pattern=pattern,string=str(text)[index:index+100])
            if match:
                api = match.group(1)                          #未授权访问
                sql1=api+"/jmreport/queryFieldBySql"          #sql注入rce1
                sql2=api+"/jmreport/testConnection"           #sql注入rce2
                print(api)
                with open("result.csv", "a+") as csvfile:
                    writer = csv.writer(csvfile)              #拿到接口后写入文件
                    writer.writerow([api])
                    writer.writerow([sql1])
                    writer.writerow([sql2])      
                
addons = [
    Counter()
]