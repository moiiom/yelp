# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from yelp.constants import MyGlobals

# city_path = "conf/usa_cities.csv"
city_path = "conf/cities.csv"
cflt_path = "conf/categories.csv"


def read_cities():
    city_dict = dict()
    with open(city_path, 'r') as f:
        for line in f:
            info = line.replace('\n', '').split('\t')
            abbr = info[0]
            cities = info[2].split(',')
            city_dict[abbr] = cities
    return city_dict


def read_cflt():
    cflt_dict = dict()
    with open(cflt_path, 'r') as f:
        for line in f:
            info = line.replace('\n', '').split('\t')
            top_cat = info[0]
            sec_cat = info[1].split(',') if len(info) > 1 else []
            cflt_dict[top_cat] = sec_cat
    return cflt_dict


MyGlobals.americian_cities = read_cities()

MyGlobals.find_cflt = read_cflt()
