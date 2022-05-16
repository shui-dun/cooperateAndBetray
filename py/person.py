from typing import List, Set

import settings as sts
from utils import *


# 人
class Person:
    def __init__(self, personId: int, ability: float, nTotal: int):
        self.id = personId
        self.money = 0
        self.ability = ability
        self.favorLst = [sts.favorInit for i in range(nTotal)]
        self.friends = set([i for i in range(sts.nFriends)])

    # 投票
    def vote(self) -> int:
        return rouletteWheelSelection(self.favorLst)

    # 增加对别人的好感
    def incFavor(self, personId: int, value: float):
        self.favorLst[personId] += value
        minVal = 0
        minInd = -1
        for ind in self.friends:
            if minInd == -1 or self.favorLst[ind] < minVal:
                minInd = ind
                minVal = self.favorLst[ind]
        if self.favorLst[personId] > minVal:
            self.friends.remove(minInd)
            self.friends.add(personId)

    # 减少对别人的好感
    def decFavor(self, personId: int, value: float):
        self.favorLst[personId] -= value
        if self.favorLst[personId] < 0:
            self.favorLst[personId] = 0


# 类别为nice的人
class NicePerson(Person):
    def __init__(self, personId: int, ability: int, nTotal: int):
        super().__init__(personId, ability, nTotal)


# 类别为ordinary的人
class OrdinaryPerson(Person):
    def __init__(self, personId: int, ability: int, nTotal: int, nEndurance: int):
        super().__init__(personId, ability, nTotal)
        self.nEndurance = nEndurance
        self.enduranceLst = [0 for _ in range(nTotal)]
        self.blacklist = set()

    # 是否同意加入某项目
    def acceptJoinProject(self, members: List[Person]) -> bool:
        for member in members:
            if member.id in self.blacklist:
                return False
        return True

    # 被某人背叛后将其加入黑名单
    def beBetrayedBy(self, person: Person):
        personId = person.id
        self.enduranceLst[personId] += 1
        if self.enduranceLst[personId] > self.nEndurance:
            self.blacklist.add(personId)


# 类别为bad的人
class BadPerson(Person):
    def __init__(self, personId, ability, nTotal, nCooperates):
        super().__init__(personId, ability, nTotal)
        self.nCooperates = nCooperates
        self.cooperatesLst = [0 for _ in range(nTotal)]
        self.whitelist = set()

    # 是否背叛组员
    def betray(self, members: List[Person]) -> bool:
        for member in members:
            if member == self:
                continue
            if member in self.whitelist:
                return False
        for member in members:
            if member == self:
                continue
            if self.cooperatesLst[member.id] > self.nCooperates:
                return True
        return False

    # 试探组员，变老赖
    def probe(self, members: List[Person]):
        for member in members:
            if member == self:
                continue
            self.cooperatesLst[member.id] += 1

    # 克制自己不背叛某人
    def restrain(self, person: Person):
        self.whitelist.add(person)


# 类别为evil的人
class EvilPerson(Person):
    def __init__(self, personId, ability, nTotal):
        super().__init__(personId, ability, nTotal)


# 所有人口
class People:
    people = []

    # 初始化人口
    @staticmethod
    def initPeople():
        cnt = 0
        for _ in range(sts.nNicePeople):
            People.people.append(NicePerson(cnt, posIntGauss(sts.muAbility, sts.sigmaAbility), sts.nPeople))
            cnt += 1
        for _ in range(sts.nOrdinaryPeople):
            People.people.append(OrdinaryPerson(cnt, posIntGauss(sts.muAbility, sts.sigmaAbility), sts.nPeople,
                                                posIntGauss(sts.muEndurance, sts.sigmaEndurance)))
            cnt += 1
        for _ in range(sts.nBadPeople):
            People.people.append(BadPerson(cnt, posIntGauss(sts.muAbility, sts.sigmaAbility), sts.nPeople,
                                           posIntGauss(sts.mucCooperates, sts.sigmaCooperates)))
            cnt += 1
        for _ in range(sts.nEvilPeople):
            People.people.append(EvilPerson(cnt, posIntGauss(sts.muAbility, sts.sigmaAbility), sts.nPeople))
            cnt += 1

    # 某个集体中的所有人及其邻居
    @staticmethod
    def friendsOfPeople(members: List[Person]) -> Set[Person]:
        friendIds = set()
        friends = set()
        for person in members:
            friendIds.add(person.id)
            friendIds |= person.friends
        for friendId in friendIds:
            friends.add(People.people[friendId])
        return friends


type2str = {
    NicePerson: "nice",
    OrdinaryPerson: "ordinary",
    BadPerson: "bad",
    EvilPerson: "evil"
}
