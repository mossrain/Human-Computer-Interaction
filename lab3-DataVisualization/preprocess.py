import pandas as pd
import numpy as np

df = pd.read_csv('./dataset/google-play-store-apps/googleplaystore.csv')

# 如果有App重复，保留第一个，不然bar的高度会变成两倍
df = df.drop_duplicates(subset='App', keep='first')

# 将Installs中的+号和逗号去掉
df['Installs'] = df['Installs'].replace('+', '')
df['Installs'] = df['Installs'].replace(',', '')
df['Installs'] = df['Installs'].astype(int)

# 更新时间改为时间戳
df['Last Updated'] = pd.to_datetime(df['Last Updated'])

# 如果price不是0，将price的第一个符号去掉，然后转为float
df['Price'] = df['Price'].apply(lambda x: x[1:] if x[0] == '$' else x)
df['Price'] = df['Price'].astype(float)

# 将Rating列中的缺失值全部转为0，然后转为float
df['Rating'] = df['Rating'].fillna(0)
df['Rating'] = df['Rating'].astype(float)

# 将Reviews列中的缺失值全部转为0，然后转为int
df['Reviews'] = df['Reviews'].fillna(0)
df['Reviews'] = df['Reviews'].astype(int)


# 显示列名
# print(df.columns)
# Index(['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type',
#        'Price', 'Content Rating', 'Genres', 'Last Updated', 'Current Ver',
#        'Android Ver'],
#       dtype='object')

'''
category、Type（只有收费和不收费两种）、ContentRating(离散化)、size(离散化，KM分开)可以画饼状图
rating、reviews、installs、price(对于收费的)可以画直方图(下拉框选择某一category或全部，只显示前k名)

用一张五颜六色的图表示四维数据

大小表示安装数
颜色表示价格
x坐标表示更新时间
y坐标表示评分
z坐标表示类别
'''

# 统计每个category的数量
def category_count():
    category_count = df['Category'].value_counts()
    # 打印类名
    # print(category_count.index)
    return category_count

# 统计每个Type的数量
def type_count():
    type_count = df['Type'].value_counts()
    return type_count

# 统计每个Content Rating的数量
def content_rating_count():
    content_rating_count = df['Content Rating'].value_counts()
    return content_rating_count

# 将size分为M结尾、K结尾、Varies with device这三类
def size_count():
    m_count = df[df['Size'].str.contains('M')]['Size'].count()
    k_count = df[df['Size'].str.contains('k')]['Size'].count()
    varies_count = df[df['Size'].str.contains('Varies with device')]['Size'].count()

    size_count = pd.Series([m_count, k_count, varies_count], index=['More than 1M', 'Less than 1M', 'Varies with device'])
    return size_count

# 将评分划分为0-2, 2-3, 3-4, 4-5, 尚未评分这5类
def rating_count():
    low_count =  df[(df['Rating'] >= 0) & (df['Rating'] < 2)]['Rating'].count()
    mid_low_count = df[(df['Rating'] >= 2) & (df['Rating'] < 3)]['Rating'].count()
    mid_high_count = df[(df['Rating'] >= 3) & (df['Rating'] < 4)]['Rating'].count()
    high_count =  df[(df['Rating'] >= 4) & (df['Rating'] <= 5)]['Rating'].count()
    nan_count = len(df)-low_count-mid_low_count-mid_high_count-high_count

    rating_count = pd.Series([nan_count, low_count, mid_low_count, mid_high_count, high_count], index=['No rating', '0-2', '2-3', '3-4', '4-5'])
    return rating_count

# 对每一类选取前20个rating最高的app
def topk(str:str, k:int=20):
    df_ret = pd.DataFrame(columns=['App', 'Category', 'Number'])

    for cat in df['Category'].unique():
        df_cat = df[df['Category'] == cat]
        df_cat = df_cat.sort_values(by=str, ascending=False) # 降序
        if str == 'Price':
            df_cat = df_cat[df_cat['Price'] != 0]
        # 如果不足k个，就取全部
        if len(df_cat) > k:
            df_cat = df_cat[:k]
        # 修改Rating列名为Number
        df_cat.rename(columns={str: 'Number'}, inplace=True)
        df_ret = df_ret.append(df_cat[['App', 'Category', 'Number']])
    return df_ret

def update_time_data():
    # 返回一个dataframe，包括年份、类别和该年份该类别的数量
    df_ret = pd.DataFrame(columns=['Year', 'Category', 'Number'])
    for year in df['Last Updated'].dt.year.unique():
        for cat in df['Category'].unique():
            df_cat = df[df['Category'] == cat]
            df_cat = df_cat[df_cat['Last Updated'].dt.year == year]
            df_ret = df_ret.append(pd.DataFrame([[year, cat, len(df_cat)]], columns=['Year', 'Category', 'Number']))
    
    # 返回一个dataframe，包括年份和该年份所有app的数量
    df_all = pd.DataFrame(columns=['Year', 'Category', 'Number'])
    
    for year in df['Last Updated'].dt.year.unique():
        df_year = df[df['Last Updated'].dt.year == year]
        df_all = df_all.append(pd.DataFrame([[year, 'ALL', len(df_year)]], columns=['Year', 'Category', 'Number']))
    df_ret = df_ret.append(df_all)

    # Year和Number都转为int
    df_ret['Year'] = df_ret['Year'].astype(int)
    df_ret['Number'] = df_ret['Number'].astype(int)

    
    return df_ret


# 画散点图用
def get_data():
    global df
    # # 删除所有Rating为0的行
    # df = df[df['Rating'] != 0]
    # 筛选列
    df = df[['App', 'Installs', 'Price', 'Last Updated', 'Rating', 'Category', 'Reviews']]
    return df

# if __name__ == '__main__':
#     print(update_time_data())

