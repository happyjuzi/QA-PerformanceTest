# QA-PerformanceTest
Python based api performance test solution.

usage: perf_test_tool.py [-h] [-p] [-t] [-l] [--params PARAMS]
                         url trans_total parallel_num

positional arguments:
  url              requet url which used to run performance test
  trans_total      total transctions will be executed
  parallel_num     parallel number will be used

optional arguments:
  -h, --help       show this help message and exit
  -p, --post       '--post' option indicate this is a post request, if not
                   specified, get method will be used by default
  -t, --test       '--test' option used to test whether url request works, if
                   not specified, will not test url
  -l, --latency    '--latency' option indicate this is a latency test, if not
                   specified, will run under qps mode
  --params PARAMS  key=value pairs to pass parameters to method

example 1:

to cacluate a get request's QPS, you would like to run the following command:

	python perf_test_tool.py [your url here,like: http://www.google.com] 1000 10

This will simply run a performance test against your specified url with 10 parallel number and 1000 transctions in total.

example 2:

to cacluate a post request's latency(response time), you could simply do this with following command:

	python perf_test_tool.py [your url here] 10 1 --params "uid=10086,d_os=android,ver=2.10,status=0,type=push" -p -l

To run for latency mode, you need "-l" parameter. To pass your params, you need to format them as "key=value" pair combined with ",".


