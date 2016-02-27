# Author: Hao in UT Austin
# Crawle free proxy IPs from http://www2.waselproxy.com/, https://nordvpn.com/free-proxy-list/, https://www.hide-my-ip.com/proxylist.shtml
# Output: list oject, ip_pool
import requests
from bs4 import BeautifulSoup
import json

class IP_Spider(object):
	def __init__(self):
		self.ip_pool = []
		pass
	def generate_ip_pool(self):	
		# Crawl from http://www2.waselproxy.com/
		for page in range(1,3):
			get_url = "http://www2.waselproxy.com/page/" + str(page)
			p = requests.get(get_url)					
			soup = BeautifulSoup(p.content,  "lxml")
			ip_row = soup.find_all("tr")

			for one in ip_row[1:]:
				try:
					x = one.find("progress")
					value = int(x.get('value'))

					if value >= 50:
						content = (one.text).encode('utf-8')
						ip_context = content.strip().split('\n')
						ip = "http://" + ip_context[0] + ":" + ip_context[1]
						self.ip_pool.append(ip)

				except:
					continue
		# Crawl from https://nordvpn.com/free-proxy-list/
		ip_type_convert = {'HTTP':'http', 'HTTPS':'https'}
		for page in range(0,150,25):
			try:
				get_url = "https://nordvpn.com/wp-admin/admin-ajax.php?searchParameters[0][name]=proxy-country&searchParameters[0][value]=&searchParameters[1][name]=proxy-ports&searchParameters[1][value]=&offset=" + str(page)+ "&limit=25&action=getProxies" 
				p = requests.get(get_url)				
				response_json = p.json()
				for i in range(len(response_json)):
					ip_type = (response_json[i]['type']).encode('utf-8')
					if ip_type not in ['HTTP','HTTPS']:
						continue
					ip_port = (response_json[i]['port']).encode('utf-8')
					ip_ip = (response_json[i]['ip']).encode('utf-8')
					ip = ip_type_convert[ip_type] + "://" + ip_ip + ":" + ip_port
					self.ip_pool.append(ip)
			except:
				continue

		# Crawl from https://www.hide-my-ip.com/proxylist.shtml
		while(True):
			try:
				get_url = "https://www.hide-my-ip.com/proxylist.shtml"
				p = requests.get(get_url)				
				soup = BeautifulSoup(p.content,  "lxml")
				ip_script = soup.find_all('script')
				ip_text = ip_script[4].text.encode('utf-8')
				ip_table = (ip_text.split(';<!-- proxylist -->')[0])[13:]
				ip_json = json.loads(ip_table)
				for i in range(len(ip_json)):
					one = ip_json[i]
					speed = one['a']
					time = int(one['t'].encode('utf-8'))
					if speed != 'High' or time > 50:
						continue
					ip_ip = one['i'].encode('utf-8')
					ip_port = one['p'].encode('utf-8')
					ip_type = one['tp'].encode('utf-8')
					ip = ip_type_convert[ip_type] + "://" + ip_ip + ":" + ip_port
					ip_pool.append(ip)
				break
			
			except:
				break
		return self.ip_pool

if __name__ == '__main__':
	foo = IP_spider()
	x = foo.generate_ip_pool()
	print len(x)
	print x
