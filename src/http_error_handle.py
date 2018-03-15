import random
import urllib.request

import time
#
# #from ip_proxy import achieve_proxy
# from user_agents import achieve_user_agent


def resolve_redirects(url,cnt=3):
    try:
        # headers = achieve_user_agent()
        # proxy = achieve_proxy()
        # proxy_support = urllib.request.ProxyHandler(proxy)
        # opener = urllib.request.build_opener(proxy_support)
        # # 添加User Angent
        # # opener.addheaders = [('User-Agent',
        # #                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
        # opener.addheaders = [('User-Agent', headers['User-Agent'])]
        # urllib.request.install_opener(opener)
        return urllib.request.urlopen(url)  # 发送请求报头
    except urllib.error.HTTPError as e:
        if e.code == 429:
           time.sleep(10)
        time.sleep(10)
        cnt = cnt -1
        if cnt > 0:
            print('re-acess cnt:',cnt)
            return resolve_redirects(url,cnt)
        else:
            return -1
        #return resolve_redirects(url,cnt)

        #raise


# 重复尝试打开网页链接
def openlink(self, link,maxTryNum):
    maxNum = 10
    for tries in range(maxTryNum):
        try:
            req = urllib.request.Request(link, headers=self.headers)
            response = urllib.request.urlopen(link)
            return response
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print("Has tried %d times to access url %s, all failed!", maxNum, link)
                break