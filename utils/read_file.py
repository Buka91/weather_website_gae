#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

city_list = list()
city_ids = list()
not_append = [u"Mestna", u"Občina", u"Republ"]

def read_data():
    if len(city_list) == 0:
        path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), "assets/json/cityList.json")
        with open(path) as data_file:
            for line in data_file:
                data_line = json.loads(line)
                if data_line['country'] == 'SI' and data_line['name'][:6] not in not_append:
                    city_list.append(data_line['name'])
                    city_ids.append(str(data_line['_id']))