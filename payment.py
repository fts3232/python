# 收支
import time
import pandas as pd
import numpy as np


# today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# income = []
# pay = []
data = np.array([['2018-02-08', '支出', 13, 'description'], ['2018-02-09', '支出', 12, 'description'], ['2018-02-09', '收入', 12, 'description'], ['2018-02-09', '支出', 12, 'description']])
df = pd.DataFrame(data, columns=['日期', '支出/收入', '金额', '描述'])
df['金额'] = df['金额'].astype(np.int32)
# # df = df['金额'].astype(np.int32).sum()
# df.groupby(['日期', '支出/收入'])[['金额']].mean()
grouped = df['金额'].groupby([df['日期'], df['支出/收入']])
print(grouped.sum())
# df = pd.DataFrame({'key1':list('aabba'),
#                   'key2': ['one','two','one','two','one'],
#                   'data1': np.random.randn(5),
#                   'data2': np.random.randn(5)})
# grouped=df['data1'].groupby(df['key1'])
# grouped.mean()
# states=np.array(['Ohio','California','California','Ohio','Ohio'])
# years=np.array([2005,2005,2006,2005,2006])
# df['data1'].groupby([states,years]).mean()
# print(df)
