#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午2:10
# @Author  : Shark
# @Site    : 
# @File    : data_initialize.py
# @Software: PyCharm
from os import path

import codecs

from config import PATH, FILE_PATH, JSON_PATH
from utlis.db_query import project_address_id_query
from utlis.utils import get_Lat_lon, address_json, insert_json, project_md5


class ProjectInfo(object):
    def __init__(self):
        self.project_info_dict = dict()

    @classmethod
    def project_read(cls, filename):
        project_info_dict = dict()
        data = codecs.open(filename=filename)
        for info in data:
            info = info.split(',')
            project_info_dict[info[0]] = {
                'project_province': info[1],
                'project_city': info[2],
                'project_country': info[3],
                'project_address': info[4]
            }
        return project_info_dict

    @classmethod
    def project_info_format(cls):
        data = cls.project_read(FILE_PATH)
        for k, v in data.items():
            project_name_md5 = project_md5(k + v['project_province'])
            address_jsons = address_json(JSON_PATH)

            if project_name_md5 in address_jsons.keys():
                v['ln_la'] = address_jsons[project_name_md5]

            else:
                v['ln_la'] = get_Lat_lon(v['project_city'] + v['project_address'])
                address_jsons[project_name_md5] = v['ln_la']

                if not v['ln_la']:
                    v['ln_la'] = get_Lat_lon(k)
                    address_jsons[project_name_md5] = v['ln_la']

                insert_json(address_jsons, JSON_PATH)
            v = project_address_id_query(v)
        return data

    def info_return(self):
        self.project_info_dict = self.project_info_format()


class Lift(object):
    def __init__(self):
        self.lift_info_dict = dict()

    @classmethod
    def lift_info_read(cls, filename):
        lift_info_dict = dict()
        data = codecs.open(filename=filename)
        for info in data:
            info = info.split(',')
            lift_info_dict[info[0]] = {
                'evOrder': info[1],
                'brandId': info[2],
                'useFor': info[3],
                'regCode': info[4],
                'deviceNumber': info[5],
                'manufacturer': info[6],
                'productionDate': info[7],
                'productionNumber': info[8],
                'modelNumber': info[9],
                'actuationForm': info[10],
                
                'lastAnnualDate': info[16],

            }
        # print(lift_info_dict)
        # return lift_info_dict


if __name__ == '__main__':
    Lift.lift_info_read(FILE_PATH)
    # A = ProjectInfo()
    # A.info_return()
    # print(A.project_info_dict)