from IP_Spider import IP_Spider

spider = IP_Spider()
ip_pool = spider.generate_ip_pool()
print "Here are a list of free proxies IPs"
print "total number is %d"%(len(ip_pool))
for one_ip in ip_pool:
	print one_ip