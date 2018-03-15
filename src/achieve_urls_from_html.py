# coding=utf-8
import os
import re
import urllib.request

import time

from parse_bib_from_urls import parse_bib_from_urls
from http_error_handle import resolve_redirects
from user_agents import achieve_user_agent


def achieve_id_content(li_str):
	for i in range(len(li_str)-4):
		if li_str[i]=='i' and li_str[i+1]=='d' and li_str[i+2]=='=':
			return li_str[i+4:].split()[0][:-1]


# def getContant(Weburl):    ### use proxy
#     Webheader= {'Upgrade-Insecure-Requests':'1',
#                 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',}
#     req = urllib.request.Request(url = Weburl,headers=Webheader)
#     respose = urllib.request.urlopen(req)
#     _contant = respose.read()
#     respose.close()
#     return str(_contant)

# def get_html_contents_no_proxy(web_url):
# 	# webheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# 	# req = urllib.request.Request(url=weburl, headers=webheaders)  # 构造请求报头
# 	# webpage = urllib.request.urlopen(req)  # 发送请求报头
# 	webpage = urllib.request.urlopen(web_url)  # 发送请求报头
# 	webpage = resolve_redirects(web_url)
# 	contentBytes = webpage.read()
# 	webpage.close()

def achieve_care_urls_from_index_html(weburl,output_file):
	url_arr=weburl.split('/')
	web_url_domain=url_arr[0]+'//'+url_arr[2]
	#webheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	webheaders=achieve_user_agent()
	req = urllib.request.Request(url=weburl, headers=webheaders)  # 构造请求报头
	#webpage = urllib.request.urlopen(req)  # 发送请求报头
	webpage= resolve_redirects(req)
	if webpage == -1:
		return -1
	contentBytes = webpage.read()
	webpage.close()
	contentBytes = contentBytes.decode(encoding='UTF-8')
	#print(contentBytes)
	#for link, t in set(re.findall(r'(http:[^s]*?(jpg|png|gif))', str(contentBytes))):  # 正则表达式查找所有的图片
	for link in re.findall(r'(<ul class="publ-list".*</ul>)', str(contentBytes)):  #
		for li_str in re.findall(r'(li class="entry.*? id=.*?<link)', str(link)):  #
			id=achieve_id_content(li_str)
			url_str=web_url_domain+'/rec/bibtex/'+id
			print(url_str)
			parse_bib_from_urls(url_str,output_file)
			time.sleep(3)
			# try:
			# 	urllib.request.urlretrieve(link, destFile(link))  # 下载图片
			# except:
			# 	print('失败')  # 异常抛出

def delete_previous_results_file(output_file):
	if os.path.exists(output_file):
		os.remove(output_file)

if __name__ == '__main__':
	search_contents_index_html='http://dblp.uni-trier.de/db/conf/imc/imc2017.html'
	search_contents_index_html = 'http://dblp.uni-trier.de/db/conf/nips/nips2017.html'

	output_file = search_contents_index_html.split('/')[-1].split('.')[0]+'_ris_result.txt'

	delete_previous_results_file(output_file)
	achieve_care_urls_from_index_html(search_contents_index_html,output_file)