import re
import urllib.request

import time

# from http_error_handle import resolve_redirects
# from ip_proxy import achieve_proxy
from http_error_handle import resolve_redirects
from ip_proxy import achieve_proxy
from save_bib_to_ris_file import save_bib_to_ris_file
from user_agents import achieve_user_agent


def parse_bib_from_urls(url_str, output_file):
	# # webpage = urllib.request.urlopen(url_str)  # 发送请求报头
	# headers = {
	# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
	# 	              'Chrome/51.0.2704.63 Safari/537.36'
	# }
	time.sleep(10)
	headers = achieve_user_agent()
	proxy=achieve_proxy()
	#### open proxy support
	# proxies={'http':'http://61.135.217.7:80/'}
	proxy_support = urllib.request.ProxyHandler(proxy)
	opener = urllib.request.build_opener(proxy_support)
	# 添加User Angent
	# opener.addheaders = [('User-Agent',
	#                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
	opener.addheaders=[('User-Agent',headers['User-Agent'])]
	# print(user_agent['User-Agent'])
	# 安装OPener
	urllib.request.install_opener(opener)

	# req = urllib.request.Request(url=url_str, headers=headers)
	#webpage = urllib.request.urlopen(req)
	webpage = resolve_redirects(url_str)
	if webpage == -1:
		return -1
	contentBytes = webpage.read()
	webpage.close()
	contentBytes = contentBytes.decode(encoding='UTF-8')

	# for contents in re.findall(r'(<div id="bibtex-section".*</div>)', str(contentBytes)):  #
	# 	for bib_str in re.findall(r'(>.*</pre>)', str(contents)):  #
	# 		print(bib_str)
	# 		# try:
	# 		# 	urllib.request.urlretrieve(link, destFile(link))  # 下载图片
	# 		# except:
	# 		# 	print('失败')  # 异常抛出
	all_bib_contents = []
	for bib_url in re.findall(r'(a href="http:.*\.bib">)', str(contentBytes)):
		bib_url = bib_url[8:-2]
		print('bib_url', bib_url)
		time.sleep(5)
		# headers1 = {
		# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
		# 	              'Chrome/51.0.2704.63 Safari/537.36'
		# }
		headers1=achieve_user_agent()
		#webpage1 = urllib.request.urlopen(bib_url)  # 发送请求报头
		req1 = urllib.request.Request(url=bib_url, headers=headers1)
		#webpage1 = urllib.request.urlopen(req1)
		webpage1 = resolve_redirects(req1)
		if webpage1 ==-1:
			continue
		contentBytes1 = webpage1.read()
		webpage1.close()

		contentBytes1 = contentBytes1.decode(encoding='UTF-8')
		# print(contentBytes1)
		all_bib_contents.append(contentBytes1)
		print(contentBytes1)

	save_bib_to_ris_file(all_bib_contents, output_file)

