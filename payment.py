# 收支
import pandas as pd
import numpy as np
from pylab import *
# 添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)


# today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# income = []
# pay = []
data = np.array([
    ['2018-02-08', '支出', 13, 'description'],
    ['2018-02-09', '支出', 12, 'description1'],
    ['2018-02-09', '收入', 12, 'description2'],
    ['2018-02-09', '支出', 12, 'description3'],
    ['2018-02-09', '支出', 12, 'description3'],
    ['2018-02-09', '收入', 12, 'description3'],
    ['2018-02-09', '收入', 12, 'description3'],
    ['2018-02-09', '支出', 12, 'description3'],
    ['2018-02-09', '支出', 12, 'description3'],
    ['2018-02-09', '支出', 12, 'description3'],
    ['2018-02-09', '支出', 12, 'description3'],
    ['2018-02-10', '收入', 12, 'description3'],
    ['2018-02-10', '支出', 12, 'description3'],
    ['2018-02-10', '支出', 12, 'description3'],
    ['2018-02-10', '收入', 12, 'description3'],
    ['2018-02-10', '支出', 12, 'description3'],
    ['2018-02-10', '支出', 12, 'description3'],
])
df = pd.DataFrame(data, columns=['日期', '支出/收入', '金额', '描述'])
df['金额'] = df['金额'].astype(np.int32)
# # df = df['金额'].astype(np.int32).sum()
# df.groupby(['日期', '支出/收入'])[['金额']].mean()
grouped = df.groupby([df['日期'], df['支出/收入']])
groupedSum = grouped.sum()
print(groupedSum)
for x in groupedSum:
    for j in groupedSum[x]:
        print(j)
# figure()
# for x in groupSum.head():
#     print(groupSum.head()[x])
#show()
