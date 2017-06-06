# 安装python2.7

# pip install scrapy

# 修改spider_start.sh配置文件

    nohup scrapy crawl myspider -a term='hotel' -a location='los angeles ca' > ./logs/my.log 2>&1 &

    其中term参数是搜索内容，location参数是位置；

    爬取多个内容时，可修改爬虫参数，启动多个爬虫并行处理。

# 爬取搜索结果页面以下四个信息

    name, address, phone, categories

# <path>/yellowpage/data目录存放爬取数据
  文件夹名称是location参数值，数据文件名称是term参数值
  数据文件csv格式，可直接excel打开

# 如何启动

    cd <path>/yellowpage
    sh -x spider_start.sh