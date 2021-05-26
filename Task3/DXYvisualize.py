from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Bar, Grid, Tab, Line
import pandas as pd
confirmedData = pd.read_csv("DXYvisualize/confirmedData.csv", index_col=0)
curedData = pd.read_csv("DXYvisualize/curedData.csv", index_col=0)
deadData = pd.read_csv("DXYvisualize/deadData.csv", index_col=0)

confirmedMap, curedMap, deadMap = \
    Timeline().add_schema(play_interval=0.2), \
    Timeline().add_schema(play_interval=0.2), \
    Timeline().add_schema(play_interval=0.2)

# confirmed
for i in confirmedData.index:
    dataDict = confirmedData.loc[i].to_dict()
    dataList = list(zip(dataDict.keys(), dataDict.values()))
    map = (
        Map()
        .add("累计确诊", dataList, "china", is_map_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="新冠肺炎累计确诊",
                subtitle="数据来源：丁香医生2019新型冠状病毒疫情时间序列数据仓库\ngithub: https://github.com/BlankerL/DXY-COVID-19-Data",
                pos_right="center",
                pos_top="5%"),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"max": 0X7FFFFFFF,"min": 10000,"label": ">=10000","color": "#B80909"},
                    {"max": 9999,"min": 1000,"label": "1000-9999","color": "#E64546"},
                    {"max": 999,"min": 100,"label": "100-999","color": "#F57567"},
                    {"max": 99,"min": 10,"label": "10-99","color": "#FF9985"},
                    {"max": 9,"min": 1,"label": "1-9","color": "#FFE5DB"},
                    {"max": 0,"min": 0,"label": "0","color": "#FFFFFF"},
                ]
            )
        )
    )
    confirmedMap.add(map, i)

# cured
for i in curedData.index:
    dataDict = curedData.loc[i].to_dict()
    dataList = list(zip(dataDict.keys(), dataDict.values()))
    map = (
        Map()
        .add("累计治愈", dataList, "china", is_map_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="新冠肺炎累计治愈",
                subtitle="数据来源：丁香医生2019新型冠状病毒疫情时间序列数据仓库\ngithub: https://github.com/BlankerL/DXY-COVID-19-Data",
                pos_right="center",
                pos_top="5%"),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"max": 0X7FFFFFFF,"min": 10000,"label": ">=10000","color": "#006400"},
                    {"max": 9999,"min": 1000,"label": "1000-9999","color": "#338333"},
                    {"max": 999,"min": 100,"label": "100-999","color": "#66A266"},
                    {"max": 99,"min": 10,"label": "10-99","color": "#99C199"},
                    {"max": 9,"min": 1,"label": "1-9","color": "#CCE0CC"},
                    {"max": 0,"min": 0,"label": "0","color": "#FFFFFF"},
                ]
            )
        )
    )
    curedMap.add(map, i)

# dead
for i in deadData.index:
    dataDict = deadData.loc[i].to_dict()
    dataList = list(zip(dataDict.keys(), dataDict.values()))
    map = (
        Map()
        .add("累计死亡", dataList, "china", is_map_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="新冠肺炎累计死亡",
                subtitle="数据来源：丁香医生2019新型冠状病毒疫情时间序列数据仓库\ngithub: https://github.com/BlankerL/DXY-COVID-19-Data",
                pos_right="center",
                pos_top="5%"),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"max": 0X7FFFFFFF,"min": 10000,"label": ">=10000","color": "#000000"},
                    {"max": 9999,"min": 1000,"label": "1000-9999","color": "#333333"},
                    {"max": 999,"min": 100,"label": "100-999","color": "#666666"},
                    {"max": 99,"min": 10,"label": "10-99","color": "#999999"},
                    {"max": 9,"min": 1,"label": "1-9","color": "#CCCCCC"},
                    {"max": 0,"min": 0,"label": "0","color": "#FFFFFF"},
                ]
            )
        )
    )
    deadMap.add(map, i)

confirmedData["sum"] = confirmedData.sum(axis=1)
curedData["sum"] = curedData.sum(axis=1)
deadData["sum"] = deadData.sum(axis=1)

line = Line()
line.add_xaxis(list(confirmedData.index))
line.add_yaxis("累计确诊",confirmedData["sum"].tolist())
line.add_yaxis("累计死亡",deadData["sum"].tolist())
line.add_yaxis("累计治愈",curedData["sum"].tolist())
line.render("line.html")


tab = Tab()
tab.add(confirmedMap, "累计确诊")
tab.add(curedMap, "累计治愈")
tab.add(deadMap, "累计死亡")
tab.render("output.html")