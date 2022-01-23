import os, json

path_allData = "data_combine.json"


def get_datas(data_index):
    with open(path_allData, 'r', encoding='utf-8') as f_all:
        data = json.load(f_all)
        cur_dish = []
        for item in data:
            # print(type(item['gid']))
            if item['gid'] == int(data_index):
                cur_dish.append(item)
        print(cur_dish)
get_datas(1151)