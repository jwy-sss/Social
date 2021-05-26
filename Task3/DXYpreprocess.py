# %%
import pandas as pd
import datetime
data = pd.read_csv("DXYvisualize/DXYArea.csv")
# %%
data = data[data["countryName"] == "中国"]
data = data[data["provinceName"] != "中国"]
data = data[["provinceName", "province_confirmedCount", "province_curedCount" ,"province_deadCount", "province_suspectedCount", "updateTime"]]
data["updateTime"] = data["updateTime"].apply(
    lambda x: datetime.datetime.strptime(x.split()[0], "%Y-%m-%d"))
data = data.drop_duplicates()
# %%
provinceSet = set(data["provinceName"])
timeLine = list(set(data["updateTime"]))
timeLine.sort()
dateStart, dateEnd = timeLine[0], timeLine[-1]
timeLine = []
while dateStart <= dateEnd:
    timeLine.append(dateStart)
    dateStart += datetime.timedelta(days=1)

# %%
confirmedData = pd.DataFrame(data=timeLine, columns=["updateTime"])
curedData = pd.DataFrame(data=timeLine, columns=["updateTime"])
deadData = pd.DataFrame(data=timeLine, columns=["updateTime"])
# suspectedData = pd.DataFrame(data=timeLine, columns=["updateTime"])

for provinceName in provinceSet:
    provinceData = data[data["provinceName"] == provinceName].copy()
    provinceData = provinceData.drop(columns=["provinceName"])
    pyechartsProvinceName = \
        provinceName[:3] \
        if (provinceName[:3]=="黑龙江"or provinceName[:3]=="内蒙古") \
        else provinceName[:2]
    provinceData.drop_duplicates(["updateTime"], keep="first", inplace=True)

    confirmedCol = provinceData[["updateTime", "province_confirmedCount"]].rename(columns={"province_confirmedCount":pyechartsProvinceName})
    curedCol = provinceData[["updateTime", "province_curedCount"]].rename(columns={"province_curedCount":pyechartsProvinceName})
    deadCol = provinceData[["updateTime", "province_deadCount"]].rename(columns={"province_deadCount":pyechartsProvinceName})
    # suspectedCol = provinceData[["updateTime", "province_suspectedCount"]].rename(columns={"province_suspectedCount":pyechartsProvinceName})

    confirmedData = pd.merge(confirmedData, confirmedCol, on="updateTime", how="left")
    curedData = pd.merge(curedData, curedCol, on="updateTime", how="left")
    deadData = pd.merge(deadData, deadCol, on="updateTime", how="left")
    # suspectedData = pd.merge(suspectedData, suspectedCol, on="updateTime", how="left")
# %%
def fillna(data: pd.DataFrame)->pd.DataFrame:
    data = data.fillna(method="pad")
    data = data.fillna(value="0")
    data = data.set_index('updateTime')
    data = data.astype('int')
    return data

confirmedData = fillna(confirmedData)
curedData = fillna(curedData)
deadData = fillna(deadData)
# suspectedData = fillna(suspectedData)
# %%
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
import matplotlib.pyplot as plt
def isIncrease(data: pd.DataFrame)->pd.DataFrame:
    un_incr = list(filter(None,[
        key if value == False else None \
            for key,value in \
                data.apply(lambda x: x.is_monotonic).to_dict().items()]))
    un_incr.remove("湖北")
    un_incr.remove("香港")
    data[un_incr].plot(figsize=(10,5))
    plt.savefig("pic.png")

isIncrease(curedData)
# %%
confirmedData.to_csv("DXYvisualize/confirmedData.csv")
curedData.to_csv("DXYvisualize/curedData.csv")
deadData.to_csv("DXYvisualize/deadData.csv")
# suspectedData.to_csv("DXYvisualize/suspectedData.csv")
# %%
