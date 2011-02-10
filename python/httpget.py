#! /usr/bin/env python
#coding=utf-8
import httplib
import redis
#import MySQLdb

report_host = "rya-lib.rockyouasia.jp"
report_method = "/infra/stats/index.php"

app = "treasure"

def send_report(data):
	conn = httplib.HTTPConnection(report_host)
	
	for k in data:
		print "%s?app=%s&event=%s&count=%s" % (report_method,app,k,data[k])
	    #conn.request("GET", "%s?app=%s&event=%s&count=%s" % (report_method,app,k,data[k]))
	    #r1 = conn.getresponse()
	    #print r1.status, r1.reason
	    #data1 = r1.read()
	    #print data1

def get_report():
	data = {'a': 0, 'b': 0}
	
	r = redis.Redis(host='192.168.8.202', port=6379, db=1)
	r.get('czw')
	for k in data:
	    data[k] = r.get(k)
	r.quit()
	   



	return data
	
def main():
	data = get_report()
	send_report(data)
if  __name__  ==  "__main__":
    main()