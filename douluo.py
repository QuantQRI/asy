import requests, re, os, time
from lxml import etree
import js2py
import aiohttp
import asyncio
from tqdm import tqdm

comic_url = 'http://m.pufei.net/mip/manhua/74/'
index_url = 'http://m.pufei.net'
path = 'F:\\pyData\\斗罗\\'
js = open('test.js','r',encoding= 'utf8').read()

server = 'http://res.img.pufei.net/'

headers = {
	'Host': 'm.pufei.net',
	'Connection': 'keep-alive',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6824.400 QQBrowser/10.3.3137.400',
	}

img_headers = {
	'Host': 'res.img.pufei.net',
	'Connection': 'keep-alive',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
}

def get_url_list(url):
	r = requests.get(url,headers = headers, verify = False)
	r.encoding = r.apparent_encoding
	html = r.text
	s = etree.HTML(html)
	titles = s.xpath('//div[@class="chapter-list"]//a/@title')
	chapter_urls = s.xpath('//div[@class="chapter-list"]//a/@href')
	for i in range(len(titles)):
		if titles[i][0] != '第' and titles[i][:2] != '番外':
			titles[i] = '第' + titles[i]
		titles[i] = re.sub('[\/:*?"<>|]','-', titles[i])

		yield titles[i],chapter_urls[i]

def file_store(path, r):
	with open(path, 'wb') as f:
		f.write(r.content)

def get_imgurls(html):
	a = []
	cp = re.findall('cp="(.*?)"', html)[0]
	base64decode =js2py.eval_js(js)

	results = js2py.eval_js(base64decode(cp))
	for result in results:
		a.append(server + result)
	return a

def comic_download(chapter_url, html, chapter_path):
	img_urls = get_imgurls(html)
	print('正在下载到%s:' % chapter_path)
	for i,img_url in tqdm(enumerate(img_urls)):
		img_name = '%02d.jpg' % i
		img_path = os.path.join(chapter_path, img_name)
		if not os.path.exists(img_path):
			r = requests.get(img_url, headers = img_headers, verify = False)
			file_store(img_path, r)
	print('下载完成！')

async def get_comic(title, chapter_url):
	async with aiohttp.ClientSession() as session:
		async with session.request('GET', chapter_url, headers = headers) as resp:
			html = await resp.text()
			chapter_path = path + title
			if not os.path.exists(chapter_path):
				os.makedirs(chapter_path)
				comic_download(chapter_url, html, chapter_path)

# 调用方
def main():
	loop = asyncio.get_event_loop()
	tasks = [get_comic(title, chapter_url) for title, chapter_url in get_url_list(comic_url)]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()

if __name__ == '__main__':
	start = time.time()
	main()

	print('总耗时：%.5f秒' % float(time.time()-start))