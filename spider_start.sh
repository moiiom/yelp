#!/bin/sh

base=$(cd "$(dirname "$0")"; pwd)
cd $base

# nohup scrapy crawl myspider -a term='hotel' -a location='los angeles ca' > ./logs/my.log 2>&1 &
# 
# nohup scrapy crawl myspider -a term='food' -a location='NY,' > ./logs/my.log 2>&1 &

# nohup scrapy crawl yelpspider -a desc='food' -a loc='los angeles ca' > ./logs/yelp.log 2>&1 &

nohup scrapy crawl yelpspider > ./logs/yelp.log 2>&1 &
