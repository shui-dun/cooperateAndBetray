import plotly.graph_objects as go

from person import *


# 绘图
class Draw:

    def __init__(self):
        self.data = {
            "nice": [],
            "ordinary": [],
            "bad": [],
            "evil": [],
        }

    # 每迭代一个项目，添加一次数据
    def appendData(self):
        moneyLst = [person.money for person in People.people]

        dataDict = {
            "nice": 0,
            "ordinary": 0,
            "bad": 0,
            "evil": 0,
        }

        for i in range(len(moneyLst)):
            val = moneyLst[i]
            dataDict[type2str[type(People.people[i])]] += val

        dataDict["nice"] /= sts.nNicePeople
        dataDict["ordinary"] /= sts.nOrdinaryPeople
        dataDict["bad"] /= sts.nBadPeople
        dataDict["evil"] /= sts.nEvilPeople

        for key, val in self.data.items():
            self.data[key].append(dataDict[key])

    # 绘图
    def draw(self):
        fig = go.Figure(layout={
            "xaxis_title": "项目次数",
            "yaxis_title": "金钱",
        })
        for key, value in self.data.items():
            fig.add_trace(go.Scatter(
                name=key,
                x=[i for i in range(len(value))],
                y=value,
            ))
        fig.show()
