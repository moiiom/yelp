# -*- coding: utf-8 -*-

import os
import errno
import codecs


class YelpPipeline(object):
    def process_item(self, item, spider):
        filename = item['filename']
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with codecs.open(filename, 'a', 'utf-8') as f:
            f.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(','.join(item['name']), ','.join(item['address']),
                                                       ','.join(item['phone']),
                                                       ','.join(item['categories']),
                                                       item['img']))
        return item
