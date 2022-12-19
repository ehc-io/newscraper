# Newscraper

Script for Cache/CDN tests

## How to use:

`python3 ./newscraper.py -i 10 -r 1000 -x 127.0.0.1:8080 -u "com-cache"`

### Parameters

- -i : Interval between sending requests
- -r : Number of runs 
- -x : proxy [IP:PORT]
- -u : User-Agent string
- -nc : Requests are sent with Cache-Control header "no-cache"
- -sh : Show response headers
- -p : Generates random string and passes it as an url parameter



