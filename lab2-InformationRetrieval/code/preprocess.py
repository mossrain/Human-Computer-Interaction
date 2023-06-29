import os 
pic_tags = {}


# 打开/database/tags文件夹，读取所有的tag文件的每一行
for root, dirs, files in os.walk('./database/tags'):
    for file in files:
        file_name = os.path.join(root, file)
        # 如果file_name中包含README，就跳过
        if 'README' in file_name:
            continue
        
        with open(file_name, 'r') as f:
            # file_name去掉./database/tags/和.txt
            file_name = file_name[14:-4]
            # print(file_name)
            # 如果有_，就只取_前面的部分
            if '_' in file_name:
                file_name = file_name[:file_name.index('_')]
            # 去掉文件名中的s\和s/
            file_name = file_name.replace('s\\', '')
            print(file_name)
            # 如果file_name不在pic_tags中，就把file_name加入pic_tags中
            if file_name not in pic_tags.keys():
                pic_tags[file_name] = []
            for line in f:
                # 把line加入pic_tags[file_name]中
                # line去掉\n
                line = line[:-1]
                pic_tags[file_name].append(line)

# 将pic_tags导出成json文件
import json
with open('pic_tags.json', 'w') as f:
    json.dump(pic_tags, f)
print("saved pic_tags.json")

# 读取pic_tags.json
with open('pic_tags.json', 'r') as f:
    pic_tags = json.load(f)
    print(pic_tags.keys())

