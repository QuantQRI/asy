import requests, re, os, json
from tqdm import tqdm
import time
import aiohttp
import asyncio
from subprocess import Popen
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 下载所有特效钢琴的音频
# 按av号下载
# 按作者下载
def file_store(path, r):
	with open(path, 'wb') as f:
		f.write(r.content)

def get_headers(play_url, url):
	host = re.findall(r'http://(.*?)/upgcxcode', play_url)[0]
	new_headers = {
		'host' : host,
		'Connection' : 'keep-alive',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6824.400 QQBrowser/10.3.3137.400',
		'Referer' : url,
	}
	return new_headers

def file_download(url, html):
	# response = requests.get(url, headers = headers, verify = False)
	# 标题
	title = re.findall(r'<h1 title="(.*?)" class="video-title">', html)[0]

	# 去除title中可能存在的非法字符
	title = re.sub('[\/:*?"<>|]','-', title)

	
	flv_url = re.findall(r'"url":"(.*?)","backup_url"', html)
	if len(flv_url) !=0:
		# 当视频链接只有一个的时候
		new_headers = get_headers(flv_url[0], url)
		video_path = '%s.flv' % title
		video_f_path = os.path.join(root_path, video_path)
		if not os.path.exists(video_f_path):
			r = requests.get(flv_url[0], headers = new_headers, verify = False)
			file_store(video_f_path, r)
		else:
			print('%s已存在！' % video_path)
	else:
		# 当视频链接有多个的时候提取id:80的纯视频(id:80不存在则选取id:64的视频)和带有280的纯音频
		
		# 30280音频
		audio_url = re.findall(r'"id":30280,"baseUrl":"(.*?)",', html)

		# 当30280音频不存在时
		if len(audio_url) == 0:
			# 30216音频
			audio_url = re.findall(r'"id":30216,"baseUrl":"(.*?)",', html)
		new_headers = get_headers(audio_url[0], url)

		audio_path = '%s.mp3' % title
		audio_f_path = os.path.join(root_path, audio_path)
		if not os.path.exists(audio_f_path):
			r = requests.get(audio_url[0], headers = new_headers, verify = False)
			file_store(audio_f_path, r)
		else:
			print('%s已存在！' % audio_path)
		# 80视频
		mp4_url = re.findall(r'"id":80,"baseUrl":"(.*?)",', html)

		if len(mp4_url) == 0:
			# 64视频
			mp4_url = re.findall(r'"id":64,"baseUrl":"(.*?)",', html)
		# print(mp4_url)
		new_headers = get_headers(mp4_url[0], url)
		mp4_path = '%s.mp4' % title
		mp4_f_url = os.path.join(root_path, mp4_path)
		if not os.path.exists(mp4_f_url):
			r = requests.get(mp4_url[0], headers = new_headers, verify = False)
			file_store(mp4_f_url, r)
		else:
			print('%s已存在！' % mp4_path)
async def get_file(url):
	headers = {
	'host' : 'www.bilibili.com',
	'Connection' : 'keep-alive',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6824.400 QQBrowser/10.3.3137.400',
	}
	global num
	
	# async with是异步上下文管理器
	async with aiohttp.ClientSession() as session:
		async with session.request('GET', url, headers = headers) as resp:
			html = await resp.text()
			try:
				# title = re.findall(r'<h1 title="(.*?)" class="video-title">', html)[0]
				# title = title.encode('GBK','ignore').decode('GBk')
				file_download(url, html)
				num += 1
				print(num)
			except Exception as e:
				print(e)

def aid_iterator():
	offset = 1
	while True:
		base_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=104993302&pagesize=50&tid=0&page=%d&keyword=&order=pubdate' % offset
		html = requests.get(base_url, verify = False)
		data = json.loads(html.text)
		if len(data['data']['vlist']) == 0:
			break
		else:
			for i in data['data']['vlist']:
				yield i['aid']
			offset += 1

# 调用方
def main():
	loop = asyncio.get_event_loop()
	tasks = [get_file('https://www.bilibili.com/video/av%d' % aid) for aid in tqdm(aid_iterator())]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()

# 将所有.flv文件转化为mp3音频
def separate(path):
	files = set(os.listdir(path))
	num = 0
	for file in tqdm(files):
		fname,fename=os.path.splitext(file)
		if fename == '.flv':
			print('正在转换%s' % file)
			fname = fname + '.mp3'
			file_new_name = os.path.join(path, fname)
			if not os.path.exists(file_new_name):
				file_name = os.path.join(path, file)
				# cmd = 'ffmpeg -i %s -f mp3 -vn %s' % (file_name, file_new_name)
				pp = Popen(['ffmpeg', '-i', '%s' % file_name, '-f', 'mp3', '-vn', '%s' % file_new_name])
				t0 = time.time()
				while time.time()-t0 < 100:
					ret = pp.poll()
					if not (ret is None):
						break
					time.sleep(0.1)
				ret = pp.poll()
				if ret is None:
					print('转换失败，强行终止')
					pp.terminate()
				else:
					print('转换成功，所需时间： %ds' % (time.time()-t0))
					num += 1
			else:
				print('%s已存在' % fname)
	print('转换结束，共转换了%d个文件' % num)

# 将所有MP4和MP3格式文件合成
def composite(path):
	files = set(os.listdir(path))
	num = 0
	new_path = 'F:\\pyData\\特效钢琴\\video'
	for file in tqdm(files):
		fname,fename=os.path.splitext(file)
		if fename == '.mp4':
			print('正在合成%s' % fname.encode('GBK','ignore').decode('GBk'))
			mp3_name = fname + '.mp3'
			mp3_f_name = os.path.join(path, mp3_name)
			mp4_f_name = os.path.join(path, file)
			mp4_new_name = os.path.join(new_path, file)
			if not os.path.exists(mp4_new_name):
				# cmd = 'ffmpeg -i %s -f mp3 -vn %s' % (file_name, file_new_name)
				# ffmpeg -i ".mp4" -i ".mp3" -c:v copy -c:a aac -strict experimental C:\Users\Lenovo\Desktop\new.mp4
				pp = Popen(['ffmpeg', '-i', '%s' % mp4_f_name, '-i', '%s' % mp3_f_name, '-c:v', 'copy','-c:a','aac','-strict','experimental', '%s' % mp4_new_name])
				t0 = time.time()
				while time.time()-t0 < 100:
					ret = pp.poll()
					if not (ret is None):
						break
					time.sleep(0.1)
				ret = pp.poll()
				if ret is None:
					print('合成失败，强行终止')
					pp.terminate()
				else:
					print('合成成功，所需时间： %ds' % (time.time()-t0))
					num += 1
			else:
				print('%s已存在' % mp4_new_name.encode('GBK','ignore').decode('GBk'))
	print('合成结束，共合成了%d个文件' % num)
num = 0
if __name__ == '__main__':
	start = time.time()
	root_path = 'F:\\pyData\\特效钢琴'

	main()
	# separate(root_path)
	composite(root_path)
	print('总耗时：%.5f秒' % float(time.time()-start))