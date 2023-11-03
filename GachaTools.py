# This is an open source Genshin Impact avatar judgement system written by a749014(秋胜春朝)
# source link:https://github.com/a749014/TeyvatToolKit
# blog:https://a749014.github.io/
import random
class GachaSimulator():
    '''抽卡模拟器'''
    def __init__(self):
        '''加载关键变量，启动模拟器'''
        self.times=0
        self.wai=0
        self.last_purple=0
        self.last_gold=0
        self.weapon_progress=0
        self.config={'avatar':[0.006,0.06,90],'weapon':[0.007,[0.07,0.035],80]}
    def Gacha(self,Type:str):
        """抽卡框架
        Type:抽卡类型。'avatar'：抽角色，'weapon'：抽武器
        返回说明：返回0：三星，返回1：出紫，返回2：出金"""
        #概率判断
        if self.last_purple==10:
            pp=1
        elif self.last_purple==9:
            pp=0.561
        else:
            pp=0.051
        if self.last_gold==self.config[Type][2]:
            pg=1
        elif Type=='avatar' and self.last_gold>=74 and self.last_gold<90:
            pg=0.006+0.06*(self.last_gold-73)
        elif Type=='weapon' and self.last_gold>=63 and self.last_gold<=73:
            
            pg=0.007+0.07*(self.last_gold-62)
        elif Type=='weapon' and self.last_gold>73 and self.last_gold<80:
            pg=0.777+0.035*(self.last_gold-72)
        # elif self.last_gold>=74 and self.last_gold<90:
        #     pg=self.config[Type][0]+0.06*(self.last_gold-73)
        else:
            pg=self.config[Type][0]
        #单抽
        # print(pg)
        r=random.random()
        self.times+=1
        self.last_purple+=1
        self.last_gold+=1
        if r<=pg:
            self.last_gold=0
            return 2                       
        elif r<=pp:
            self.last_purple=0
            return 1
        else:
            return 0
    def GachaUP(self,upNames=list,upName=int):
        '''UP池抽卡,重写

        upNames:当期up角色，两个
        upName:你老公/老婆，填索引'''
        result=self.Gacha(Type='avatar')
        if result==2:
            if self.wai==1:
                self.wai=0
                result=upNames[upName]          
            else:
                r=random.randint(2,3)
                if r==2:
                    self.wai+=1
                    result='歪'
                else:
                    result=upNames[upName]
        return result
    def GachaWeapons(self,weapons:list,target:int):
        '''武器池抽卡
        weapons:本期武器，两个，放在列表里
        target:两个武器要定轨第几个，填索引'''
        # target=weapons[target]
        result=self.Gacha(Type='weapon')
        if result==2:
            if self.weapon_progress==2:
                result=weapons[target]
            else:
                r=random.random()
                print(r)
                if r>0.75 and self.weapon_progress<2:
                    result='歪'
                    self.weapon_progress+=1
                elif r<=0.75 and r >0.75/2 and self.weapon_progress<2:
                    
                    print(weapons)
                    print(target)
                    print(self.weapon_progress)
                    result=weapons[self.opposite(target)]
                    self.weapon_progress+=1
                else:
                    print(weapons)
                    print(target)
                    result=weapons[target]
                    self.weapon_progress=0
        return result
    def opposite(self,index:int):
        if index==0:
            return 1
        elif index==1:
            return 0

        


                
    def Gacha10Times(self,isSort:bool,Type='avatar'):
        '''十连抽，返回一个列表
        isSort:是否对结果进行排序
        Type：'avatar':抽角色，'weapon':抽武器'''
        l=[]
        for i in range(10):
            l.append(self.Gacha(Type))
        if isSort:
            return sorted(l)
        else:
            return l
    def reboot(self):
        self.__init__()
        
g=GachaSimulator()
for i in range(360):
    # print(g.last_purple,g.last_gold,g.GachaWeapons(['a','b'],1))
    g.GachaWeapons(['a','b'],1)