import draw
from project import *

if __name__ == '__main__':
    d = draw.Draw()
    People.initPeople()
    for i in range(sts.nProjects):
        project = Project()
        project.initMembers(People.people)
        project.cluster()
        project.work()
        project.print('../export/result.txt')
        d.appendData()
    d.draw()
