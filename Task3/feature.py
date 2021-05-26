# %%
import pandas as pd
confirmedData = pd.read_csv("DXYvisualize/confirmedData.csv", index_col=0)
curedData = pd.read_csv("DXYvisualize/curedData.csv", index_col=0)
deadData = pd.read_csv("DXYvisualize/deadData.csv", index_col=0)

def getIncr(data: pd.DataFrame)->pd.DataFrame:
    incr = data.diff()
    incr.iloc[0] = data.iloc[0]
    return incr


confirmedIncr = getIncr(confirmedData)
curedIncr = getIncr(curedData)
deadIncr = getIncr(deadData)

# %%
def getRolling(data: pd.DataFrame)->pd.DataFrame:
    return data.rolling(7, center=True, min_periods=0).mean()

confirmedIncrRolling = getRolling(confirmedIncr)
curedIncrRolling = getRolling(curedIncr)
deadIncrRolling = getRolling(deadIncr)
# %%
totalData = pd.DataFrame(columns=["updateTime","confirmedIncr","curedIncr","deadIncr","provinceName"])
for province in confirmedData.columns.values:
    # if province=="湖北":continue
    provinceData = pd.DataFrame(data = confirmedData.index,columns=["updateTime"])
    # print( confirmedIncrRolling[province])
    provinceData.insert(1, 'provinceName', [province]*len(confirmedData.index))
    provinceData.insert(2, 'confirmedIncr', confirmedIncrRolling[province].values)
    provinceData.insert(3, 'curedIncr', curedIncrRolling[province].values)
    provinceData.insert(4, 'deadIncr', deadIncrRolling[province].values)
    totalData = pd.concat([totalData, provinceData])
totalData = totalData.reset_index(drop=True)
# %%
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.figure(figsize=(20,20))
ax = plt.subplot(projection="3d")
ax.set_title("")
ax.scatter(totalData["confirmedIncr"],totalData["curedIncr"],totalData["deadIncr"],c='r')
ax.set_xlabel("感染")
ax.set_ylabel("治愈")
ax.set_zlabel("死亡")
plt.savefig("3D.png")
plt.show()
# %%
