# -*- coding: utf-9 -*-
import time
import math
import random

DATA_DIR = 'data'


#获取旅行的目的地
def get_destination():
    #LGA是纽约的机场
    return 'LGA'


# 获取旅行的人，第一个是名字，第二个是目前所在地
def get_travel_people():
    return [('Seymour','BOS'),
            ('Franny','DAL'),
            ('Zooey','CAK'),
            ('Walt','MIA'),
            ('Buddy','ORD'),
            ('Les','OMA')]


# 生成所有航班信息字典（以起止点为键）
def generate_flight_dict():
    file = open(os.path.join(DATA_DIR, 'schedule.txt'))
    lines = file.readlines()
    file.close()
    flights = {}
    for line in lines:
        origin, dest, depart, arrive, price = line.strip().split(',')
        key = (origin, dest)
        flights.setdefault(key, [])
        flights[key].append((depart, arrive, price))
    return flights


# 获取从凌晨0点开始经过了多少分钟
def get_minutes_by_hm(hm):
    # strptime是将特定的时间格式转化为元组
    ts = time.strptime(hm, '%H:%M')
    print(ts[0, ts[1]], ts[2])
    return ts[3] * 60 + ts[4]

# 打印人名、出发地、去回程航班起达时间、价格等信息
def print_schedule(schedules, destination, people):
    # 依次一个人的起飞航班和返回航班
    rate_num = 2
    for idx in range(len(schedules) / rate_num):
        start_idx = idx * rate_num
        name = people[schedule][0]
        origin = people[schedule][1]
        trip = flights[(origin, destination)][schedule[idx]]
        back = flights[(destination, origin)][schedule[idx + 1]]
        print('%10s %10s %5s-%5s $%3s %5s-%5s $%3s'\
            % (name, origin, trip[0], trip[1], trip[2], back[0], back[1], back[2]))


def schedulecost(sol):
    totalprice=0
    latestarrival=0#最晚到底时间
    earliestdep=24*60#最早离开时间，现在24*60是最好的情况，等一下会根据实际飞机情况发生改变
    for d in range(len(sol)/2):
        #得到每一个人的两次航班的价格并且加入到总价格中
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(sol[2*d])]
        returnf = flights[(destination,origin)][int(sol[2*d+1])]

        #把钱加入到总价格里面去
        totalprice+=outbound[2]
        totalprice+=returnf[2]

        #根据实际情况改变最晚到达时间和最早离开时间
        if latestarrival<getminutes(outbound[1]):latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]):earliestdep=getminutes(returnf[0])

    #每一个人必须在机场等待直到最后一个来了才能出发
    #每一个人必须在旅游结束时，为了最早离开的人能够赶上飞机，而来到机场等候
    totalwait=0
    for d in range(len(sol)/2):
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(sol[2*d])]
        returnf = flights[(destination,origin)][int(sol[2*d+1])]        

        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    if latestarrival<earliestdep: totalprice+=50
    #如果这样看，在机场每多等一分钟就是1美元，而租车如果超过24个小时就罚款50美元
    return totalprice+totalwait

#domain代表随机产生的数字的个数和每一个数字的范围，是一个列表，列表里每个元素里面是一个元组，每个元组有2个元素，一个是上限，一个是下限
#costf就是成本函数，
#每次随机产生一组结果的时候，我们将会使用costf进行一下测试，看看效果如何
def randomptimize(domain,costf):
    best=999999999
    bestr=None
    for i in range(10000):#我们打算随机产生1000次结果，从这1000次结果中选择一个最好的
        #很显然randint是产生在一定范围内的随机数,显然由于下一句右边等号里的for，将会产生一个循环
        r=[random.randint(domain[i][0],domain[i][1])for i in range (len(domain))]
        cost=costf(r)

        #每次得到成本我们都判断一次，如果更低，我们就置换
        if cost<best:
            best=cost
            bestr=r
    return bestr

def hillclimb(domain,costf):
    #先创建一个随机的解
    sol=[random.randint(domain[i][0],domain[i][1])for i in range (len(domain))]
    while 1:#持续一个循环，直到在一次对每一个解减一或者加一之后没有任何改变时，就break
        neighbors=[]
        for j in range(len(domain)):
            #解中的每一个元素都都会加一或者减一，加一产生一个解集，减一产生一个解集
            if sol[j]>domain[j][0]:
                #如果很熟悉
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
        #neighbors已经组装好了，现在在里面找最优解
        current=costf(sol)
        best=current
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]
        if best == current:
            break
    return sol

def annealingoptimize(domain,costf,T=10000.0,cool=0.98,step=1):
    #和爬山法一样，先产生一个随机解，然后一切的改变都从这个随机解开始
    vec=[random.randint(domain[i][0],domain[i][1])for i in range (len(domain))]
    
    while T>0.5:
        #产生一个随机数，决定这次改变是改变数列中的哪一个随机数
        i=random.randint(0,len(domain)-1)

        #选择一个改变的方向，也就是说是增加还是减少
        dir=random.randint(-step,step)

        #复制随机解，然后对随机解进行改变，然后判断到底新的解好，还是后来产生的解好
        vecb=vec[:]
        vecb[i]+=dir
        #这一段主要还是不让它超不过了最大最小值的限制
        if vecb[i]<domain[i][0]:vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]:vecb[i]=domain[i][1]

        #计算新产生的两次解的成本，然后对成本进行比较
        ea=costf(vec)
        eb=costf(vecb)
        
        #or后面：表示接受更差的结果。仔细想想，原来概率的表示是如此完成的，注意前一个random()产生的数是在0到1之间。                  
        if(eb<ea or random.random()<pow(math.e,-(eb-ea)/T)):
            vec=vecb

        #没经过一次循环，改变温度，温度一改变，就会改变循环的次数和接受更差解的概率
        #按一定比例降温
        T=T*cool

    return vec

#popsize：一个种群的规模大小
#mutprob：种群中进行变异，而不进行配对的概率。
#elite：在当前种群中被认为优秀的子代的比例，优秀的子代可以直接传入下一代
#maxiter：迭代运行多少代

def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
    #方法中还在定义方法
    #变异操作
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        #完成第增加或减少的概率各一半
        if random.random()<0.5 and vec[i]>domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i]<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
        else: return vec
    #交叉操作：貌似用python编程是好快的说，我感觉比较复杂的句子只要两句么，还是我c/c++没学好
    def crossover(r1,r2):
        #为什么减2，其实想把这个一个数字列表划分为两段，再各取一半
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]
    
#构造初始种群
    pop=[]
    for i in range(popsize):
        vec = [random.randint(domain[i][0],domain[i][1])for i in range(len(domain))]
        pop.append(vec)
        
    #每一代有多少优势物种，我们需要保留
    topelite=int(elite*popsize)
    #主循环
    for i in range(maxiter):
        #print pop #但是如果不加这句会使下一句出现一个bug，就是传过去的v是None,但是我讲pop全部打印出来的话，又没有问题
        scores=[(costf(v),v) for v in pop]#列表里面，每一个元素都是一个元组，每一个元组是由一个数字和一个列表构成
        scores.sort()
        ranked=[v for (s,v) in scores]

        
        #从中选择我们觉得优势的物种，然后保留
        pop=ranked[0:topelite]

        #如果种群数量不够，那么我们使用变异或者配对，产生新的后代个体
        while len(pop)<popsize:
            #变异的概率，这是由我们设定的,虽然这里是变异和配对只能选择其一，但是我认为是可以共同进行的
            if random.random()<mutprob:#如果这样做，就是变异的少，交叉的多吧
                #变异
                c=random.randint(0,topelite)#注意是从优秀的子代中选出一个进行变异
                pop.append(mutate(ranked[c]))
            else:
                c1=random.randint(0,topelite)#从优秀的子代中选择
                c2=random.randint(0,topelite)#从优秀的子代中选择
                pop.append(crossover(ranked[c1],ranked[c2]))
            
        print scores[0][0]#注意打印的是成本        
                
    return scores[0][1]#这里返回的是航班序列
        

domain=[(0,9)]*(len(people)*2)
#sol=geneticoptimize(domain,schedulecost)
#printschedule(sol)
#print schedulecost(sol)
                
