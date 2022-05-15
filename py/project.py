from person import *
from utils import *

# 项目
class Project:
    def __init__(self):
        # 项目成员
        self.members = []
        # 选择合作的组员
        self.cluster1 = []
        # 选择背叛的组员
        self.cluster2 = []

    # 选出组员
    def initMembers(self, people):
        nMembers = int(random.uniform(sts.nGroupFloor, sts.nGroupCeiling))
        voteCnt = [0 for _ in range(len(people))]
        for person in people:
            if not isinstance(person, NicePerson) and not isinstance(person, OrdinaryPerson):
                continue
            voteCnt[person.vote()] += 1
        while True:
            newMember = rouletteWheelSelection(voteCnt)
            if isinstance(newMember, OrdinaryPerson) and not newMember.acceptJoinProject(self.members):
                continue
            self.members.append(people[newMember])
            if len(self.members) == nMembers:
                break

    # 分成“合作”和“背叛”的两个醋
    def cluster(self):
        for member in self.members:
            if isinstance(member, NicePerson) or isinstance(member, OrdinaryPerson):
                self.cluster1.append(member)
            elif isinstance(member, BadPerson):
                if member.betray(self.members):
                    self.cluster2.append(member)
                else:
                    self.cluster1.append(member)
            else:
                self.cluster2.append(member)

    # 开展工作
    def work(self):
        # 全都选择背叛
        if len(self.cluster1) == 0:
            for member in self.members:
                member.money -= sts.lossBetray
        # 全都选择合作
        elif len(self.cluster2) == 0:
            for member in self.members:
                member.money += sts.profitCooperate
            friendSet = People.friendsOfPeople(self.members)
            for friend in friendSet:
                for person in self.members:
                    if friend == person:
                        continue
                    friend.incFavor(person.id, person.ability / 2)
        # 既有选择背叛的人，也有选择合作的人
        else:
            # 背叛导致的金钱变化
            for member in self.cluster1:
                member.money -= sts.lossCooperate
            for member in self.cluster2:
                member.money += sts.profitBetray

            # 添加各自黑名单、白名单等操作
            for member in self.cluster1:
                if isinstance(member, OrdinaryPerson):
                    for betray in self.cluster2:
                        member.beBetrayedBy(betray)
                        if isinstance(betray, BadPerson):
                            betray.restrain(member)

            # 投诉导致的金钱变化
            complaintMoney = 0
            for member in self.cluster1:
                if isinstance(member, OrdinaryPerson):
                    member.money -= sts.lossAskForComplaint
                    complaintMoney += sts.lossComplaint * len(self.cluster2)
            for member in self.cluster2:
                member.money -= complaintMoney / len(self.cluster2)
            for member in self.cluster1:
                member.money += complaintMoney / len(self.cluster1)

            # 好感度变化
            friendSet = People.friendsOfPeople(self.cluster1)
            avgAbility = 0
            for person in self.cluster1:
                avgAbility += person.ability
            avgAbility /= len(self.cluster1)
            for friend in friendSet:
                for person in self.cluster1:
                    friend.incFavor(person.id, person.ability / 2)
                for person in self.cluster2:
                    friend.decFavor(person.id, avgAbility)
        for member in self.members:
            if isinstance(member, BadPerson):
                member.probe(self.members)

    # 打印信息
    def print(self, file):
        s = 'begin project:\n'
        for member in self.members:
            dt = {
                "id": member.id,
                "money": member.money,
                "ability": member.ability,
                "type": type2str[type(member)],
                "favor": member.favorLst
            }
            s = '{}{}\n'.format(s, dt)
        # print(s)
        with open(file, 'a') as f:
            f.write(s)
