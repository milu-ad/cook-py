




import os, json
import numpy as np

path_allData = "data_combine.json"
path_Data_before = "data04.json"

taste_refer = {'sweet': ['甜辣', '酸甜', '甜味', '咸甜', '甜香', '果味', '奶香', '鱼香'],
               'salty': ['酱香', '咸香', '麻香'],
               'sour': ['酸辣', '酸咸'],
               'spicy': ['微辣', '中辣', '超辣', '麻辣', '香辣'],
               'fresh': ['咸鲜', '清淡', '原味'],
               'other': ['其他', '苦味', '葱香', '蒜香', '糟香', '咖喱', '孜然', '香草', '怪味', '五香']
               }
level = ['easy', 'normal', 'hard', 'pretty hard']
cuisine = ['C', 'H', 'X', 'L', 'M', 'S', 'Y', 'Z']


def get_counts(k, v, title, count):
    if k == title:
        count = len(v)
    return count


# 获取做菜难度数据
def get_level_datas():
    with open(path_allData, 'r', encoding='utf-8') as f_all:
        data = json.load(f_all)

        res_s = []  # 分数数值
        res_l = []  # 分数等级
        for line in data:  # 一个菜品的数据
            url = line['url']
            count_m = 0
            count_f = 0
            count_p = 0
            count_t = 0
            for k, v in line.items():
                if k == 'taste':
                    for label, taste in taste_refer.items():
                        if v in taste:
                            cate = label

                count_m = get_counts(k, v, 'main_ingre', count_m)
                count_f = get_counts(k, v, 'f_ingre', count_f)
                count_p = get_counts(k, v, 'p_ingre', count_p)
                count_t = get_counts(k, v, 'step', count_t)
                if k == 'level':
                    if v == '简单':
                        tmp = 20
                    elif v == '普通':
                        tmp = 40
                    elif v == '高级':
                        tmp = 60
                    else:
                        tmp = 80

            count = count_m + count_f + count_p + count_t
            score = count * 0.5 + tmp * 0.5  # 每道菜的复杂程度得分
            if score < 20:
                level = 'easy'
            elif score < 40:
                level = 'normal'
            elif score < 60:
                level = 'hard'
            else:
                level = 'pretty hard'

            res_s.append(score)
            res_l.append(level)
        # print(len(res_s))
        res = [res_s, res_l]
        return res


# 获取口味数据
def get_taste_datas():
    with open('data05.json', 'r', encoding='utf8') as f_all:
        data = json.load(f_all)
        res = []
        for cuisine, dishLists in data.items():  # 键 值对
            for dish in dishLists:  # 一个菜的数据

                url = dish['url']
                taste_pre = dish['口味']
                for label, taste in taste_refer.items():
                    if taste_pre in taste:
                        if cuisine != '湘菜' and taste_pre != '清淡' and '腊肠' in dish['name']:
                            taste_type = 'salty'
                        else:
                            taste_type = label
                res.append(taste_type)  # 存入菜品的唯一url和口味
        return res


# 整合所有数据
c = ['c', 'h', 'x', 'l', 'm', 's', 'y', 'z']
t = ['sweet', 'salty', 'sour', 'spicy', 'fresh', 'other']
l = ['easy', 'normal', 'hard', 'pretty']
# for i in range(8):
#     for j in range(6):
#         for k in range(4):
#             print('res_' + c[i] + '_' + t[j] + '_' + l[k] + '={"id": "' + c[i].upper() + '_' + t[j] + str(
#                 3-k) + '", "cuisine": "' + str(i) + '", "cate": "' + t[j] + '", "degree": "' + str(
#                 3-k) + '", "nums": 0, "dishes": []}')
#

res_c_sweet_easy={"id": "C_sweet3", "cuisine": "0", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sweet_normal={"id": "C_sweet2", "cuisine": "0", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sweet_hard={"id": "C_sweet1", "cuisine": "0", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sweet_pretty={"id": "C_sweet0", "cuisine": "0", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_c_salty_easy={"id": "C_salty3", "cuisine": "0", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_c_salty_normal={"id": "C_salty2", "cuisine": "0", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_c_salty_hard={"id": "C_salty1", "cuisine": "0", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_c_salty_pretty={"id": "C_salty0", "cuisine": "0", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sour_easy={"id": "C_sour3", "cuisine": "0", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sour_normal={"id": "C_sour2", "cuisine": "0", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sour_hard={"id": "C_sour1", "cuisine": "0", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_c_sour_pretty={"id": "C_sour0", "cuisine": "0", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_c_spicy_easy={"id": "C_spicy3", "cuisine": "0", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_c_spicy_normal={"id": "C_spicy2", "cuisine": "0", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_c_spicy_hard={"id": "C_spicy1", "cuisine": "0", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_c_spicy_pretty={"id": "C_spicy0", "cuisine": "0", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_c_fresh_easy={"id": "C_fresh3", "cuisine": "0", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_c_fresh_normal={"id": "C_fresh2", "cuisine": "0", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_c_fresh_hard={"id": "C_fresh1", "cuisine": "0", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_c_fresh_pretty={"id": "C_fresh0", "cuisine": "0", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_c_other_easy={"id": "C_other3", "cuisine": "0", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_c_other_normal={"id": "C_other2", "cuisine": "0", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_c_other_hard={"id": "C_other1", "cuisine": "0", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_c_other_pretty={"id": "C_other0", "cuisine": "0", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sweet_easy={"id": "H_sweet3", "cuisine": "1", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sweet_normal={"id": "H_sweet2", "cuisine": "1", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sweet_hard={"id": "H_sweet1", "cuisine": "1", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sweet_pretty={"id": "H_sweet0", "cuisine": "1", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_h_salty_easy={"id": "H_salty3", "cuisine": "1", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_h_salty_normal={"id": "H_salty2", "cuisine": "1", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_h_salty_hard={"id": "H_salty1", "cuisine": "1", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_h_salty_pretty={"id": "H_salty0", "cuisine": "1", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sour_easy={"id": "H_sour3", "cuisine": "1", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sour_normal={"id": "H_sour2", "cuisine": "1", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sour_hard={"id": "H_sour1", "cuisine": "1", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_h_sour_pretty={"id": "H_sour0", "cuisine": "1", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_h_spicy_easy={"id": "H_spicy3", "cuisine": "1", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_h_spicy_normal={"id": "H_spicy2", "cuisine": "1", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_h_spicy_hard={"id": "H_spicy1", "cuisine": "1", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_h_spicy_pretty={"id": "H_spicy0", "cuisine": "1", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_h_fresh_easy={"id": "H_fresh3", "cuisine": "1", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_h_fresh_normal={"id": "H_fresh2", "cuisine": "1", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_h_fresh_hard={"id": "H_fresh1", "cuisine": "1", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_h_fresh_pretty={"id": "H_fresh0", "cuisine": "1", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_h_other_easy={"id": "H_other3", "cuisine": "1", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_h_other_normal={"id": "H_other2", "cuisine": "1", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_h_other_hard={"id": "H_other1", "cuisine": "1", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_h_other_pretty={"id": "H_other0", "cuisine": "1", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sweet_easy={"id": "X_sweet3", "cuisine": "2", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sweet_normal={"id": "X_sweet2", "cuisine": "2", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sweet_hard={"id": "X_sweet1", "cuisine": "2", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sweet_pretty={"id": "X_sweet0", "cuisine": "2", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_x_salty_easy={"id": "X_salty3", "cuisine": "2", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_x_salty_normal={"id": "X_salty2", "cuisine": "2", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_x_salty_hard={"id": "X_salty1", "cuisine": "2", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_x_salty_pretty={"id": "X_salty0", "cuisine": "2", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sour_easy={"id": "X_sour3", "cuisine": "2", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sour_normal={"id": "X_sour2", "cuisine": "2", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sour_hard={"id": "X_sour1", "cuisine": "2", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_x_sour_pretty={"id": "X_sour0", "cuisine": "2", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_x_spicy_easy={"id": "X_spicy3", "cuisine": "2", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_x_spicy_normal={"id": "X_spicy2", "cuisine": "2", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_x_spicy_hard={"id": "X_spicy1", "cuisine": "2", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_x_spicy_pretty={"id": "X_spicy0", "cuisine": "2", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_x_fresh_easy={"id": "X_fresh3", "cuisine": "2", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_x_fresh_normal={"id": "X_fresh2", "cuisine": "2", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_x_fresh_hard={"id": "X_fresh1", "cuisine": "2", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_x_fresh_pretty={"id": "X_fresh0", "cuisine": "2", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_x_other_easy={"id": "X_other3", "cuisine": "2", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_x_other_normal={"id": "X_other2", "cuisine": "2", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_x_other_hard={"id": "X_other1", "cuisine": "2", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_x_other_pretty={"id": "X_other0", "cuisine": "2", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sweet_easy={"id": "L_sweet3", "cuisine": "3", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sweet_normal={"id": "L_sweet2", "cuisine": "3", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sweet_hard={"id": "L_sweet1", "cuisine": "3", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sweet_pretty={"id": "L_sweet0", "cuisine": "3", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_l_salty_easy={"id": "L_salty3", "cuisine": "3", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_l_salty_normal={"id": "L_salty2", "cuisine": "3", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_l_salty_hard={"id": "L_salty1", "cuisine": "3", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_l_salty_pretty={"id": "L_salty0", "cuisine": "3", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sour_easy={"id": "L_sour3", "cuisine": "3", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sour_normal={"id": "L_sour2", "cuisine": "3", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sour_hard={"id": "L_sour1", "cuisine": "3", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_l_sour_pretty={"id": "L_sour0", "cuisine": "3", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_l_spicy_easy={"id": "L_spicy3", "cuisine": "3", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_l_spicy_normal={"id": "L_spicy2", "cuisine": "3", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_l_spicy_hard={"id": "L_spicy1", "cuisine": "3", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_l_spicy_pretty={"id": "L_spicy0", "cuisine": "3", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_l_fresh_easy={"id": "L_fresh3", "cuisine": "3", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_l_fresh_normal={"id": "L_fresh2", "cuisine": "3", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_l_fresh_hard={"id": "L_fresh1", "cuisine": "3", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_l_fresh_pretty={"id": "L_fresh0", "cuisine": "3", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_l_other_easy={"id": "L_other3", "cuisine": "3", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_l_other_normal={"id": "L_other2", "cuisine": "3", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_l_other_hard={"id": "L_other1", "cuisine": "3", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_l_other_pretty={"id": "L_other0", "cuisine": "3", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sweet_easy={"id": "M_sweet3", "cuisine": "4", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sweet_normal={"id": "M_sweet2", "cuisine": "4", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sweet_hard={"id": "M_sweet1", "cuisine": "4", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sweet_pretty={"id": "M_sweet0", "cuisine": "4", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_m_salty_easy={"id": "M_salty3", "cuisine": "4", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_m_salty_normal={"id": "M_salty2", "cuisine": "4", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_m_salty_hard={"id": "M_salty1", "cuisine": "4", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_m_salty_pretty={"id": "M_salty0", "cuisine": "4", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sour_easy={"id": "M_sour3", "cuisine": "4", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sour_normal={"id": "M_sour2", "cuisine": "4", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sour_hard={"id": "M_sour1", "cuisine": "4", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_m_sour_pretty={"id": "M_sour0", "cuisine": "4", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_m_spicy_easy={"id": "M_spicy3", "cuisine": "4", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_m_spicy_normal={"id": "M_spicy2", "cuisine": "4", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_m_spicy_hard={"id": "M_spicy1", "cuisine": "4", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_m_spicy_pretty={"id": "M_spicy0", "cuisine": "4", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_m_fresh_easy={"id": "M_fresh3", "cuisine": "4", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_m_fresh_normal={"id": "M_fresh2", "cuisine": "4", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_m_fresh_hard={"id": "M_fresh1", "cuisine": "4", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_m_fresh_pretty={"id": "M_fresh0", "cuisine": "4", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_m_other_easy={"id": "M_other3", "cuisine": "4", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_m_other_normal={"id": "M_other2", "cuisine": "4", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_m_other_hard={"id": "M_other1", "cuisine": "4", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_m_other_pretty={"id": "M_other0", "cuisine": "4", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sweet_easy={"id": "S_sweet3", "cuisine": "5", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sweet_normal={"id": "S_sweet2", "cuisine": "5", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sweet_hard={"id": "S_sweet1", "cuisine": "5", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sweet_pretty={"id": "S_sweet0", "cuisine": "5", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_s_salty_easy={"id": "S_salty3", "cuisine": "5", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_s_salty_normal={"id": "S_salty2", "cuisine": "5", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_s_salty_hard={"id": "S_salty1", "cuisine": "5", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_s_salty_pretty={"id": "S_salty0", "cuisine": "5", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sour_easy={"id": "S_sour3", "cuisine": "5", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sour_normal={"id": "S_sour2", "cuisine": "5", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sour_hard={"id": "S_sour1", "cuisine": "5", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_s_sour_pretty={"id": "S_sour0", "cuisine": "5", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_s_spicy_easy={"id": "S_spicy3", "cuisine": "5", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_s_spicy_normal={"id": "S_spicy2", "cuisine": "5", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_s_spicy_hard={"id": "S_spicy1", "cuisine": "5", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_s_spicy_pretty={"id": "S_spicy0", "cuisine": "5", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_s_fresh_easy={"id": "S_fresh3", "cuisine": "5", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_s_fresh_normal={"id": "S_fresh2", "cuisine": "5", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_s_fresh_hard={"id": "S_fresh1", "cuisine": "5", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_s_fresh_pretty={"id": "S_fresh0", "cuisine": "5", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_s_other_easy={"id": "S_other3", "cuisine": "5", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_s_other_normal={"id": "S_other2", "cuisine": "5", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_s_other_hard={"id": "S_other1", "cuisine": "5", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_s_other_pretty={"id": "S_other0", "cuisine": "5", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sweet_easy={"id": "Y_sweet3", "cuisine": "6", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sweet_normal={"id": "Y_sweet2", "cuisine": "6", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sweet_hard={"id": "Y_sweet1", "cuisine": "6", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sweet_pretty={"id": "Y_sweet0", "cuisine": "6", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_y_salty_easy={"id": "Y_salty3", "cuisine": "6", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_y_salty_normal={"id": "Y_salty2", "cuisine": "6", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_y_salty_hard={"id": "Y_salty1", "cuisine": "6", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_y_salty_pretty={"id": "Y_salty0", "cuisine": "6", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sour_easy={"id": "Y_sour3", "cuisine": "6", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sour_normal={"id": "Y_sour2", "cuisine": "6", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sour_hard={"id": "Y_sour1", "cuisine": "6", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_y_sour_pretty={"id": "Y_sour0", "cuisine": "6", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_y_spicy_easy={"id": "Y_spicy3", "cuisine": "6", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_y_spicy_normal={"id": "Y_spicy2", "cuisine": "6", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_y_spicy_hard={"id": "Y_spicy1", "cuisine": "6", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_y_spicy_pretty={"id": "Y_spicy0", "cuisine": "6", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_y_fresh_easy={"id": "Y_fresh3", "cuisine": "6", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_y_fresh_normal={"id": "Y_fresh2", "cuisine": "6", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_y_fresh_hard={"id": "Y_fresh1", "cuisine": "6", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_y_fresh_pretty={"id": "Y_fresh0", "cuisine": "6", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_y_other_easy={"id": "Y_other3", "cuisine": "6", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_y_other_normal={"id": "Y_other2", "cuisine": "6", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_y_other_hard={"id": "Y_other1", "cuisine": "6", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_y_other_pretty={"id": "Y_other0", "cuisine": "6", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sweet_easy={"id": "Z_sweet3", "cuisine": "7", "cate": "sweet", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sweet_normal={"id": "Z_sweet2", "cuisine": "7", "cate": "sweet", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sweet_hard={"id": "Z_sweet1", "cuisine": "7", "cate": "sweet", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sweet_pretty={"id": "Z_sweet0", "cuisine": "7", "cate": "sweet", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_z_salty_easy={"id": "Z_salty3", "cuisine": "7", "cate": "salty", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_z_salty_normal={"id": "Z_salty2", "cuisine": "7", "cate": "salty", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_z_salty_hard={"id": "Z_salty1", "cuisine": "7", "cate": "salty", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_z_salty_pretty={"id": "Z_salty0", "cuisine": "7", "cate": "salty", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sour_easy={"id": "Z_sour3", "cuisine": "7", "cate": "sour", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sour_normal={"id": "Z_sour2", "cuisine": "7", "cate": "sour", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sour_hard={"id": "Z_sour1", "cuisine": "7", "cate": "sour", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_z_sour_pretty={"id": "Z_sour0", "cuisine": "7", "cate": "sour", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_z_spicy_easy={"id": "Z_spicy3", "cuisine": "7", "cate": "spicy", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_z_spicy_normal={"id": "Z_spicy2", "cuisine": "7", "cate": "spicy", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_z_spicy_hard={"id": "Z_spicy1", "cuisine": "7", "cate": "spicy", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_z_spicy_pretty={"id": "Z_spicy0", "cuisine": "7", "cate": "spicy", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_z_fresh_easy={"id": "Z_fresh3", "cuisine": "7", "cate": "fresh", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_z_fresh_normal={"id": "Z_fresh2", "cuisine": "7", "cate": "fresh", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_z_fresh_hard={"id": "Z_fresh1", "cuisine": "7", "cate": "fresh", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_z_fresh_pretty={"id": "Z_fresh0", "cuisine": "7", "cate": "fresh", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}
res_z_other_easy={"id": "Z_other3", "cuisine": "7", "cate": "other", "degree": "3", "nums": 0, "dishes": [],"indexlists":[]}
res_z_other_normal={"id": "Z_other2", "cuisine": "7", "cate": "other", "degree": "2", "nums": 0, "dishes": [],"indexlists":[]}
res_z_other_hard={"id": "Z_other1", "cuisine": "7", "cate": "other", "degree": "1", "nums": 0, "dishes": [],"indexlists":[]}
res_z_other_pretty={"id": "Z_other0", "cuisine": "7", "cate": "other", "degree": "0", "nums": 0, "dishes": [],"indexlists":[]}

def get_datas():
    taste_type = get_taste_datas()  # 所有口味数据
    score = get_level_datas()  # 所有难度数据
    count = 0
    arr = []

    with open(path_allData, 'r', encoding='utf-8') as f_all:
        data = json.load(f_all)
        for index, dish in enumerate(data):  # index: 数组索引；dish：一道菜
            level_num = 3-level.index(score[1][index])  # 难度对应的数值编号
            id_ = dish["id"][0] + '_' + taste_type[index] + str(level_num)
            cuisine_num = cuisine.index(dish['id'][0])  # 所属菜系
            cate = taste_type[index]

            res_type = 'res_' + dish["id"][0].lower() + '_' + cate + '_' + score[1][index].split(' ')[0]
            res_type = eval(res_type)  # str convert to variable
            res_type['id'] = id_

            res_type['cuisine'] = str(cuisine_num)
            res_type['degree'] = level_num
            res_type['cate'] = cate
            res_type['nums'] += 1
            res_type['dishes'].append(dish['id'])
            res_type['indexlists'].append(dish['gid'])

    # 打印出最终结果
    for i in range(8):
        for j in range(6):
            for k in range(4):
                arr.append(eval('res_' + c[i] + '_' + t[j] + '_' + l[k]))
                # print(eval('res_' + c[i] + '_' + t[j] + '_' + l[k]), ',')
    f = open('0_4-3-4res.json','a',encoding = 'utf-8')
    f.write(str(arr))
    f.close()

get_datas()
# get_taste_datas()
# get_level_datas()
# getData()
