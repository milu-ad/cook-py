import os,json,re
path = os.getcwd() + "\\wenjian.txt"




f = open(path,'r',encoding='utf8')
ni = []
count = 1
for each_line in f:
    each_line.strip('\n')
    if  '=====' not in each_line:
        res = each_line.split('，',1)
        role = res[0]
        line_spoken = res[1]
        print(role,line_spoken)
        if role == '你是':
            ni.append(line_spoken)
    else :
        file_name_ni = 'ni'+str(count)+'.txt'
        ni_file = open(file_name_ni,'w')
        ni_file.writelines(ni)
        ni_file.close()
        ni = []
        count += 1
file_name_ni = 'ni'+str(count)+'.txt'
# in_file = open(file_name_ni,'w')
# in_file.writelines(ni)
# in_file.close()