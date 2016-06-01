#coding:utf-8
import json
import requests
import datetime
import time
import pdb
import os
import argparse

import multiprocessing


def format_params(_params):
        params = {}
        try:
            kv_params = _params.split(",")
            if kv_params:
                for kv_param in kv_params:
                    kv = kv_param.split("=")
                    if len(kv) == 2:
                        key = kv[0]
                        value = kv[1]
                        params[key] = value
            else:
                print "_params is empty"
        except Exception as e:
            print "func format_params exception...."
            print e

        return params

def compose_request(_is_post, _url, _params):

        try:
            params = format_params(_params)

            if _is_post:
                resp = requests.post(_url, params)
            else:
                get_url = _url
                if _params:
                    get_url = get_url + "?"
                    for param in _params:
                        get_url += key + "=" + param[key] + "&"

                resp = requests.get(get_url)

        except Exception as e:
            print "func: compose_request exception..."
            print e
	
        return resp

def main(name,words):
        print "Hello world" + name + words


if __name__ == "__main__":
        _is_post = False
        _is_test = False
	_is_latency = False

        _url = ""
        _trans_total = 0
        _paral_num = 0
        _params = ""


        parser = argparse.ArgumentParser()

        parser.add_argument("-p", "--post", help="'--post' option indicate this is a post request, if not specified, get method will be used by default",action="store_true")

        parser.add_argument("-t", "--test", help="'--test' option used to test whether url request works, if not specified, will not test url",action="store_true")
	
	parser.add_argument("-l", "--latency", help="'--latency' option indicate this is a latency test, if not specified, will run under qps mode", action="store_true")

        parser.add_argument("url", help="requet url which used to run performance test ")

        parser.add_argument("trans_total", help="total transctions will be executed ")

        parser.add_argument("parallel_num", help="parallel number will be used ")

        parser.add_argument("--params", help="key=value pairs to pass parameters to method ")


        args = parser.parse_args()

        if args.post:
                print "post is active "
                _is_post = True
        if args.test:
                print "test is active "
                _is_test = True
	if args.latency:
		print "latency mode is active"
		_is_latency = True
        if args.url:
                print "url is active "
                _url = args.url
        if args.trans_total:
                print "trans_total is active "
                _trans_total = int(args.trans_total)
        if args.parallel_num:
                print "parallel_num is active "
                _paral_num = int(args.parallel_num)
        if args.params:
                print "params is active "
                _params = args.params
	

        if _is_test:
                print "test run....will output results of current test method"
                print "============================================================================="
                test_resp = compose_request(_is_post, _url, _params)

                if test_resp.status_code != 200:
                    print "return code invalid...please check the url..."
                    exit(-1)
                else:
                    print test_resp.text


	if _is_latency:
		print "Latency mode...."
		print "============================================================================="
		
        	start_time = time.time()
		for j in xrange(10000):
			compose_request(_is_post, _url, _params)		
        	end_time = time.time()

		total_time=(end_time - start_time)
        	print "All process(es) done. used time: {total_time}".format(total_time=total_time)
		print "Average response time is: " + str(total_time/10000) + " s"
	else:	
        	pool = multiprocessing.Pool(processes=_paral_num)
        	start_time = time.time()

	        for i in xrange(_trans_total):
        		pool.apply_async(compose_request, (_is_post, _url, _params ) )

	        pool.close()
        	pool.join()
	        end_time = time.time()
		total_time=(end_time - start_time)
        	print "All process(es) done. used time: {total_time}".format(total_time=total_time)
		print "Total process: " + str(_trans_total)
		print "Parallel number: " + str(_paral_num)
		print "Average QPS is : " + str(_trans_total/total_time)

