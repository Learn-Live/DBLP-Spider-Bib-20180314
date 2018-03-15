import random
import urllib.request

import re

# from http_error_handle import resolve_redirects
from http_error_handle import resolve_redirects
from user_agents import achieve_user_agent


def get_proxy_ip_list(web_url, web_headers):
	req = urllib.request.Request(url=web_url, headers=web_headers)  # 构造请求报头
	# webpage = urllib.request.urlopen(req,timeout=10)  # 发送请求报头
	webpage = resolve_redirects(req)
	# webpage = urllib.request.urlopen(web_url)  # 发送请求报头
	if webpage==-1:
		return -1
	contentBytes = webpage.read()
	webpage.close()

	ip_list = []
	for td_str in re.findall(r'(<td>.*?/>)', str(contentBytes)):
		#print(td_str)
		tmp_arr=td_str.split('\\n')
		tag= tmp_arr[6].strip()[4:-5].lower()
		ip_tmp=tag+' '+tmp_arr[0].strip()[4:-5]+':'+tmp_arr[1].strip()[4:-5]
		#print(ip_tmp)
		ip_list.append(ip_tmp)

	return ip_list
	# for i in range(1, len(ips)):
	# 	ip_info = ips[i]
	# 	tds = ip_info.find_all('td')
	# 	ip_list.append(tds[1].text + ':' + tds[2].text)
	# return ip_list


def get_random_ip(ip_list):
	proxy_list = []
	for ip in ip_list:
		ip=ip.split()
		#proxy_list.append([ip[0],ip[0]+'://' + ip[1]])
		proxy_list.append([ip[0], ip[1]])
	proxy_ip = random.choice(proxy_list)
	proxies = {proxy_ip[0]: proxy_ip[1]}
	return proxies


def initpattern():
	"""
	函数说明:初始化正则表达式
	Parameters:
	    无
	Returns:
	    lose_time - 匹配丢包数
	    waste_time - 匹配平均时间
	Modify:
	    2017-05-27
	"""
	# 匹配丢包数
	lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
	# 匹配平均时间
	waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
	return lose_time, waste_time


import subprocess as sp
def check_ip(ip, lose_time, waste_time):
	"""
	函数说明: 检查代理IP的连通性
	Parameters:
	ip - 代理的ip地址
	lose_time - 匹配丢包数
	waste_time - 匹配平均时间

	我制定的规则是，如果丢包数大于2个，则认为ip不能用。ping通的平均时间大于200ms也抛弃。当然，我这个要求有点严格，可以视情况放宽规则.

	Returns:
	average_time - 代理ip平均耗时
	Modify:
	2017 - 05 - 27
	"""

	# 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
	cmd = "ping -n 3 -w 3 %s"
	# 执行命令
	p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
	# 获得返回结果并解码
	out = p.stdout.read().decode("gbk")
	# 丢包数
	lose_time = lose_time.findall(out)
	# 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
	if len(lose_time) == 0:
		lose = 3
	else:
		lose = int(lose_time[0])
	# 如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
	if lose > 2:
		# 返回False
		return 1000
	# 如果丢包数目小于等于2个,获取平均耗时的时间
	else:
		# 平均时间
		average = waste_time.findall(out)
		# 当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
		if len(average) == 0:
			return 1000
		else:
			#
			average_time = int(average[0])
			# 返回平均耗时
			return average_time

def check_ip_connection(ip_str):
    """
    #### come from: http://blog.csdn.net/c406495762/article/details/72793480
    #### "Python3网络爬虫(十一)：爬虫黑科技之让你的爬虫程序更像人类用户的行为(代理IP池等)"
    """
    #初始化正则表达式
    lose_time, waste_time = initpattern()
    # 检查ip
    average_time = check_ip(ip_str, lose_time, waste_time)
    if average_time > 200:
        print("ip连接超时, 重新获取中!")
        return -1
    else:# if average_time < 200:
        return 1


def achieve_proxy():
	url = 'http://www.xicidaili.com/nn/'  ### 国内高匿代理IP
	# headers = {
	# 	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
	# }
	headers=achieve_user_agent()
	ip_list = get_proxy_ip_list(url, headers)
	if ip_list==-1:
		return -1
	proxies = get_random_ip(ip_list)
	flg = True
	while flg:
		ip_str=list(proxies.values())[0].split(':')[0]          ### proxies is dict type
		key=list(proxies.keys())[0]
		if check_ip_connection(ip_str)==-1:
			print([key,list(proxies.values())[0]])
			ip_list.remove(key+' '+list(proxies.values())[0])  ## romve unconnection ip
			proxies= get_random_ip(ip_list)
		else:
			break
	print(proxies)
	return proxies


if __name__ == '__main__':

	weburl= 'http://dblp.uni-trier.de/db/conf/aaai/aaai2017.html'
	webheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

	#### open proxy support
	#proxies={'http':'http://61.135.217.7:80/'}
	proxies=achieve_proxy()
	# 创建ProxyHandler
	proxy_support = urllib.request.ProxyHandler(proxies)
	# 创建Opener
	opener = urllib.request.build_opener(proxy_support)
	# 添加User Angent
	opener.addheaders = [('User-Agent',
	                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
	# 安装OPener
	urllib.request.install_opener(opener)
	# 使用自己安装好的Opener
	webpage = urllib.request.urlopen(weburl)

	#req = urllib.request.Request(url=weburl, headers=webheaders)  # 构造请求报头
	#webpage = urllib.request.urlopen(req)  # 发送请求报头

	contentBytes = webpage.read()
	webpage.close()
	contentBytes = contentBytes.decode(encoding='UTF-8')
	print(contentBytes)