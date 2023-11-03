# This is an open source Genshin Impact avatar judgement system written by a749014
# source link:https://github.com/a749014/TeyvatToolKit
# blog:https://a749014.github.io/
import requests
import os
import json
PATH=os.path.dirname(os.path.abspath(__file__))
CACHE_PATH=PATH+os.sep+'cache'
DATA_PATH=PATH+os.sep+'data'
def getAllInfo(uid:int,isReadCache:bool,isWriteCache:bool,\
               return_player_data=True,return_avatar_data=True):
    ''' get the player data from https://enka.network  
        uid --> Player uid
        isReadCache --> True : Read the cache from ./cache at first . If failed , get data from the internet
                    --> False : Always get data from internet
        isWriteCache --> True : Always write the data into ./cache
                     --> False : Return the data directly
        return_player_data : True , return all of the player data . False , do not return .
        return_avatar_data : True , return all of the avatar data . False , do not return . '''
    if isReadCache:
        data=CacheRead(uid)
    else:
        data=requests.get(f'https://enka.network/api/uid/{uid}').json()
    rd={}
    if 'message' in list(data.keys()):
        return data
    if return_player_data:
        rd['playerInfo']=data['playerInfo']
    if return_avatar_data and 'avatarInfoList' in list(data.keys()):
        rd['avatarInfoList']=data['avatarInfoList']
    elif 'avatarInfoList' not in list(data.keys()):
        rd['avatarInfoList']='This player hid the detailed infomation of avatar'
    if isWriteCache:
        CacheWrite(uid,rd)
    return rd

def update_player_info(uid:int):
    '''update cache'''
    data=requests.get(f'https://enka.network/api/uid/{uid}').json()
    CacheWrite(uid,data)

def CacheWrite(uid,append_data):
    '''write the player data into local cache
       uid --> player uid
       append_data --> the data which you want to append in the cache'''
    f=open(CACHE_PATH+os.sep+'cache.json','r')
    c=json.load(f)
    c[uid]=append_data
    f.close()
    with open(CACHE_PATH+os.sep+'cache.json','w')as f:
        json.dump(c,f,ensure_ascii=False)
    del c
def CacheRead(uid):
    '''read the player data from local cache
       uid -->player uid'''
    cfile=os.listdir(CACHE_PATH)
    if 'cache.json' in cfile:
        try:
            with open(CACHE_PATH+os.sep+'cache.json','r') as f:
                data=json.load(f)[str(uid)]
            del f
        except:
            print('Failed to load data from local cache , getting data from internet......')
            data=requests.get(f'https://enka.network/api/uid/{uid}').json()
    else:
        print('Do not find local cache file , getting data from internet......')
        data=requests.get(f'https://enka.network/api/uid/{uid}').json()
    return data

class Judger():
    '''Avatar judgement tools'''
    def __init__(self):
        '''load some important data 
        self.weight : The weight of reliquary . Format: {'avatar name':<class:list>}
        list index of self.weight: 0:the percentage of HP , 1:The percentage of ATK , 2:The percentage of DEF 3:CRIT rate , 4:CRIT DMG , 5:Elemental mastery , 6:Energy recharge'''
        with open(DATA_PATH+os.sep+'weights.json','r',encoding='utf-8')as wf:
            self.weight=json.load(wf)
    def mainStatJudgement(self,avatar_Chinese_name:str,info:dict,character_element:str):
        '''Because function reliquery_judgement() only support substat judgement , so I write a specially function for main stat judgement.
        max score:20 min score:0
        avatar_Chinese_name:MUST BE THE OFFICAL CHINESE NAME
        info demo : {'mainPropId': 'FIGHT_PROP_CRITICAL_HURT','statValue': 30.5}(from getAllInfo())
        character_element : Wind,Ice,Water,Fire,Grass,Rock,Electric'''
        stat_translation={"FIGHT_PROP_FIRE_ADD_HURT": "火元素伤害加成",
		"FIGHT_PROP_ELEC_ADD_HURT": "雷元素伤害加成",
		"FIGHT_PROP_WATER_ADD_HURT": "水元素伤害加成",
		"FIGHT_PROP_GRASS_ADD_HURT": "草元素伤害加成",
		"FIGHT_PROP_WIND_ADD_HURT": "风元素伤害加成",
		"FIGHT_PROP_ROCK_ADD_HURT": "岩元素伤害加成",
		"FIGHT_PROP_ICE_ADD_HURT": "冰元素伤害加成",
        "FIGHT_PROP_HP": "生命值",
		"FIGHT_PROP_HP_PERCENT": "生命值百分比",
        "FIGHT_PROP_ATTACK": "攻击力",
		"FIGHT_PROP_ATTACK_PERCENT": "攻击力百分比",
        "FIGHT_PROP_DEFENSE": "防御力",
		"FIGHT_PROP_DEFENSE_PERCENT": "防御力百分比",
        "FIGHT_PROP_CRITICAL": "暴击率",
        "FIGHT_PROP_CRITICAL_HURT": "暴击伤害",
		"FIGHT_PROP_CHARGE_EFFICIENCY": "元素充能效率",
        "FIGHT_PROP_ELEMENT_MASTERY": "元素精通",}
        element_target={'FIGHT_PROP_WIND_ADD_HURT':'Wind','FIGHT_PROP_ICE_ADD_HURT':'Ice',\
            'FIGHT_PROP_WATER_ADD_HURT':'Water','FIGHT_PROP_FIRE_ADD_HURT':'Fire',\
                'FIGHT_PROP_GRASS_ADD_HURT':'Grass','FIGHT_PROP_ROCK_ADD_HURT':'Rock',\
                    'FIGHT_PROP_ELEC_ADD_HURT':'Electric'}
        w=self.weight[avatar_Chinese_name]
        if info['mainPropId'] in element_target.keys() and element_target[info['mainPropId']]==character_element:
            return 20
        elif info['mainPropId'] in element_target.keys() and element_target[info['mainPropId']]!=character_element:
            return 0
        else:
            # print('else')
            parameter_demo={'生命值百分比':0,'攻击力百分比':0,'防御力百分比':0,'暴击率':0,'暴击伤害':0,'元素精通':0,'元素充能效率':0,'生命值':0,'攻击力':0,'防御力':0}
            parameter_demo[stat_translation[info['mainPropId']]]=info['statValue']
            return 2*self.reliquery_judgement(avatar_Chinese_name,list(parameter_demo.values()))/5
    def reliquery_judgement(self,avatar_Chinese_name:str,infoList:list):
        '''max score : 50 , min score : 0
        infoList:the reliquery info , must be a list . Normal list index : 0:the percentage of HP , 1:The percentage of ATK , 2:The percentage of DEF
        3:CRIT rate , 4:CRIT DMG , 5:Elemental mastery , 6:Energy recharge 7.HP 8.ATK 9.DEF
            If you input only 2 indexes , list index : 0:CRIT rate 1:CRIT damage
            If there are only two indexes , judge the reliquery by the CRIT rate and DMG
            If there are seven indexes , judge the reliquery by its user
        avatar_Chinese_name:MUST BE THE OFFICAL CHINESE NAME
        return the total score'''
        if len(infoList)==2:
            return infoList[0]*100*2+infoList[1]*100
        else:
            w=self.weight[avatar_Chinese_name]
            CRITRateScore=infoList[3]*2*(w[3]/100)
            CRITDMGScore=infoList[4]*(w[4]/100)
            MasteryScore=infoList[5]*0.33*(w[5]/100)
            ChargeScore=infoList[6]*1.1979*(w[6]/100)/100
            HPPercentageScore=infoList[0]*1.33*(w[0]/100)
            ATKPercentageScore=infoList[1]*1.33*(w[1]/100)
            DEFPercentageScore=infoList[2]*1.06*(w[2]/100)
            HPScore=infoList[7]*0.026*0.66*w[0]/100
            ATKScore=infoList[8]*0.398*0.5*w[1]/100
            DEFScore=infoList[9]*0.335*0.66*w[2]/100
            # print(HPPercentageScore,ATKPercentageScore,DEFPercentageScore,CRITRateScore,CRITDMGScore,MasteryScore,ChargeScore,HPScore,ATKScore,DEFScore)
            return CRITDMGScore+CRITRateScore+MasteryScore+ChargeScore+HPPercentageScore\
            +ATKPercentageScore+DEFPercentageScore+HPScore+ATKScore+DEFScore

# if __name__=='__main__':
#     j=Judger()
#     print(j.reliquery_judgement('胡桃',[0,0,0,0,5,0,0,215,14,31]))
