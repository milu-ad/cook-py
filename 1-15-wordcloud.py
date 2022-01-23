import os,json,jieba

import pandas as pd

# !/usr/bin/env python3
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('january_2017_repair')
with open_workbook('ingre_result_01-15-8-1.xlsx') as workbook:
    worksheet = workbook.sheet_by_name('january_2013')
    for row_index in range(worksheet.nrows):
        for col_index in range(worksheet.ncols):
            # 判断单元格里的值是否是日期
            if worksheet.cell_type(row_index, col_index) == 3:
                # 先将单元格里的表示日期数值转换成元组
                date_cell = xldate_as_tuple(worksheet.cell_value(row_index, col_index), workbook.datemode)
                # 使用元组的索引来引用元组的前三个元素并将它们作为参数传递给date函数来转换成date对象，用strftime()函数来将date对象转换成特定格式的字符串
                date_cell = date(*date_cell[:3]).strftime('%Y/%m/%d')
                # 将格式化的日期填充到原来的表示日期的数值的位置
                output_worksheet.write(row_index, col_index, date_cell)
            else:
                # 将sheet中非表示日期的值赋给non_date_celld对象
                non_date_cell = worksheet.cell_value(row_index, col_index)
                # 将sheet中非表示日期的值位置填充到相应位置
                output_worksheet.write(row_index, col_index, non_date_cell)


