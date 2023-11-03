# name:Teyvat Tool Kit
# developer:a749014
# introduction:This is an open source Genshin Impact avatar judgement system
# source link:https://github.com/a749014/TeyvatToolKit
# blog:https://a749014.github.io/
import AvatarJudgement as aj
from pprint import pprint
import GachaAnalyze as ga
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from TeyvatUI import Ui_TeyvatUI
from reliqueryResult import Ui_reliqueryResult
import os,json,sys
path=os.path.dirname(os.path.abspath(__file__))
#stat translation
stattranslate={"FIGHT_PROP_BASE_HP": "基础生命值",
		"FIGHT_PROP_HP": "生命值",
		"FIGHT_PROP_HP_PERCENT": "生命值百分比",
		"FIGHT_PROP_BASE_ATTACK": "基础攻击力",
		"FIGHT_PROP_ATTACK": "攻击力",
		"FIGHT_PROP_ATTACK_PERCENT": "攻击力百分比",
		"FIGHT_PROP_BASE_DEFENSE": "基础防御力",
		"FIGHT_PROP_DEFENSE": "防御力",
		"FIGHT_PROP_DEFENSE_PERCENT": "防御力百分比",
		"FIGHT_PROP_BASE_SPEED": "移动速度",
		"FIGHT_PROP_SPEED_PERCENT": "移动速度百分比",
		"FIGHT_PROP_CRITICAL": "暴击率",
		"FIGHT_PROP_ANTI_CRITICAL": "暴击抗性",
		"FIGHT_PROP_CRITICAL_HURT": "暴击伤害",
		"FIGHT_PROP_CHARGE_EFFICIENCY": "元素充能效率",
		"FIGHT_PROP_ADD_HURT": "伤害增加",
		"FIGHT_PROP_SUB_HURT": "受伤减免",
		"FIGHT_PROP_HEAL_ADD": "治疗加成",
		"FIGHT_PROP_HEALED_ADD": "受治疗加成",
		"FIGHT_PROP_ELEMENT_MASTERY": "元素精通",
		"FIGHT_PROP_PHYSICAL_SUB_HURT": "物理抗性",
		"FIGHT_PROP_PHYSICAL_ADD_HURT": "物理伤害加成",
		"FIGHT_PROP_FIRE_ADD_HURT": "火元素伤害加成",
		"FIGHT_PROP_ELEC_ADD_HURT": "雷元素伤害加成",
		"FIGHT_PROP_WATER_ADD_HURT": "水元素伤害加成",
		"FIGHT_PROP_GRASS_ADD_HURT": "草元素伤害加成",
		"FIGHT_PROP_WIND_ADD_HURT": "风元素伤害加成",
		"FIGHT_PROP_ROCK_ADD_HURT": "岩元素伤害加成",
		"FIGHT_PROP_ICE_ADD_HURT": "冰元素伤害加成",
		"FIGHT_PROP_FIRE_SUB_HURT": "火元素抗性",
		"FIGHT_PROP_ELEC_SUB_HURT": "雷元素抗性",
		"FIGHT_PROP_WATER_SUB_HURT": "水元素抗性",
		"FIGHT_PROP_GRASS_SUB_HURT": "草元素抗性",
		"FIGHT_PROP_WIND_SUB_HURT": "风元素抗性",
		"FIGHT_PROP_ROCK_SUB_HURT": "岩元素抗性",
		"FIGHT_PROP_ICE_SUB_HURT": "冰元素抗性",
		"FIGHT_PROP_EFFECT_HIT": "效果命中",
		"FIGHT_PROP_EFFECT_RESIST": "效果抵抗",
		"FIGHT_PROP_FREEZE_SHORTEN": "冻结时间缩短",
		"FIGHT_PROP_DIZZY_SHORTEN": "眩晕时间缩短",
		"FIGHT_PROP_SKILL_CD_MINUS_RATIO": "冷却缩减",
		"FIGHT_PROP_SHIELD_COST_MINUS_RATIO": "护盾强效",
		"FIGHT_PROP_CUR_HP": "生命值",
		"FIGHT_PROP_MAX_HP": "生命值上限",
		"FIGHT_PROP_CUR_ATTACK": "攻击力",
		"FIGHT_PROP_CUR_DEFENSE": "防御力",
		"FIGHT_PROP_CUR_SPEED": "移动速度"}#stat translate into Chinese
class main(QMainWindow,Ui_TeyvatUI):
	def __init__(self):
		'''init ui and load key data'''
		super().__init__()
		self.setupUi(self)
		self.reliqueryui=reliqueryResult()
		self.results={}
		#load the translation information and character information
		with open(path+os.sep+'data'+os.sep+'TextMapCHS.json', 'r', encoding='utf-8')as f:
			self.translate = json.load(f)
		with open(path+os.sep+'data'+os.sep+'characters.json', 'r', encoding='utf-8')as f:
			self.characters = json.load(f)
		self.show()
		self.pushButton_reliquery.clicked.connect(self.reliqueryScore)
		# uid=255158340#change
		self.results={}
		self.judger=aj.Judger()
		self.EquipTypeCommit={'EQUIP_BRACER': '生之花', 'EQUIP_NECKLACE': '死之羽', 'EQUIP_SHOES': '时之沙', 'EQUIP_RING': '空之杯', 'EQUIP_DRESS': '理之冠'}#equipe type translation
		# info=aj.getAllInfo(uid,True,True,False,True)["avatarInfoList"]
	def getTravellerElement(self,avatarID:str):
		'''Because traveller have different elements and the stanard of traveller is affect by his/her element, we need to get the element of traveller.
		Return data : f"旅行者{element_name}"'''
		translations={'Wind':'风','Ice':'冰','Water':'水','Fire':'火','Grass':'草','Rock':'岩','Electric':'雷'}
		return '旅行者'+translations[self.characters[avatarID]['Element']]

	def reliqueryScore(self):
		'''Score the reliquery based on aj.reliquery_judgement()
		info : Avatar info from enka.network or local cache , use aj.getAllInfo()'''
		self.pushButton_reliquery.setText('评分中')
		self.pushButton_reliquery.setEnabled(False)#disabeled judge button
		uid = self.lineEdit_reliquery.text()
		self.reliqueryui.label_uid.setText(f'UID：{uid}的评分结果')
		self.reliqueryui.pushButton_update.clicked.connect(lambda:self.update_avatar_info(uid))
		info = aj.getAllInfo(uid, True, True, False, True)[
                    "avatarInfoList"]  # load info
		pprint(info)
		results={}
		for i in info:
			# '''get the key reliquery data and score it'''
			#preparation
			namehash=self.characters[str(i['avatarId'])]['NameTextMapHash']
			print(namehash)
			Chinesename=self.translate[str(namehash)]
			if Chinesename=='旅行者':
				Chinesename=self.getTravellerElement(str(i['avatarId']))
			# if Chinesename
			ft={'生之花':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},'死之羽':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},\
					'时之沙':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},'空之杯':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},\
						'理之冠':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]}}
			for j in i['equipList']:
				if j['flat']['itemType']=='ITEM_RELIQUARY':
					#key code : get the key reliquery data and score it
					parameter_demo={'生命值百分比':0,'攻击力百分比':0,'防御力百分比':0,'暴击率':0,'暴击伤害':0,'元素精通':0,'元素充能效率':0,'生命值':0,'攻击力':0,'防御力':0}
					ft[self.EquipTypeCommit[j['flat']['equipType']]]['星级']=j['flat']['rankLevel']
					ft[self.EquipTypeCommit[j['flat']['equipType']]]['名字']=self.translate[j['flat']['nameTextMapHash']]
					ft[self.EquipTypeCommit[j['flat']['equipType']]]['等级']=j['reliquary']['level']-1#reduce one!
					substat={stattranslate[k['appendPropId']]:k['statValue'] for k in j['flat']['reliquarySubstats']}
					ft[self.EquipTypeCommit[j['flat']['equipType']]]['副词条']=substat
					mainstat={stattranslate[j['flat']['reliquaryMainstat']['mainPropId']]:j['flat']['reliquaryMainstat']['statValue']}
					ft[self.EquipTypeCommit[j['flat']['equipType']]]['主词条']=mainstat
					for stat in substat:
						try:
							parameter_demo[stat]=substat[stat]
						except:
							pass
					# print(parameter_demo)
					scores='主词条：{}\n副词条：{}'.format(round(self.judger.mainStatJudgement(Chinesename,j['flat']['reliquaryMainstat'],self.characters[str(i['avatarId'])]['Element'])),\
						round(self.judger.reliquery_judgement(Chinesename,list(parameter_demo.values())),2))
					ft[self.EquipTypeCommit[j['flat']['equipType']]]['评分']=scores
			# print(ft)
			results[Chinesename]=ft#change
		# print(results)
		self.reliqueryui.comboBox_avatars.clear()
		for i in results:
			self.reliqueryui.comboBox_avatars.addItem(i)#add into combobox
		self.results=results
		self.reliqueryUIGen(self.reliqueryui.comboBox_avatars.currentText())
		self.reliqueryui.show()
		self.pushButton_reliquery.setText('评分')
		self.pushButton_reliquery.setEnabled(True)  # enabeled judge button
		self.reliqueryui.comboBox_avatars.activated.connect(
			lambda: self.reliqueryUIGen(self.reliqueryui.comboBox_avatars.currentText()))
	def update_avatar_info(self,uid):
		aj.update_player_info(uid)
		self.reliqueryScore()

	def reliqueryUIGen(self, avatar: str):
		self.reliqueryUIRender(self.results[avatar])
	def reliqueryUIRender(self,results):
		'''render reliquery result UI from reliqueryResult.py
		results demo:{'生之花':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},'死之羽':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},\
					'时之沙':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},'空之杯':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]},\
						'理之冠':{'星级':0,'名字':'','等级':0,'副词条':[],'评分':0,'主词条':[]}}'''
		#
		controls={'生之花':{'labels':[self.reliqueryui.label_name,self.reliqueryui.label_stat,self.reliqueryui.label_type,self.reliqueryui.label_quality,self.reliqueryui.label_mainstat],\
			'buttons':[self.reliqueryui.pushButton_icon,self.reliqueryui.pushButton_result]\
                   }, '死之羽': {'labels': [self.reliqueryui.label_name_2, self.reliqueryui.label_stat_2, self.reliqueryui.label_type_2, self.reliqueryui.label_quality_2,self.reliqueryui.label_mainstat_2], \
					   'buttons': [self.reliqueryui.pushButton_icon_2, self.reliqueryui.pushButton_result_2]
                              }, '时之沙': {'labels': [self.reliqueryui.label_name_3, self.reliqueryui.label_stat_3, self.reliqueryui.label_type_3, self.reliqueryui.label_quality_3,self.reliqueryui.label_mainstat_3], \
								  'buttons': [self.reliqueryui.pushButton_icon_3, self.reliqueryui.pushButton_result_3]
                                         }, '空之杯': {'labels': [self.reliqueryui.label_name_4, self.reliqueryui.label_stat_4, self.reliqueryui.label_type_4, self.reliqueryui.label_quality_4,self.reliqueryui.label_mainstat_4], \
											 'buttons': [self.reliqueryui.pushButton_icon_4, self.reliqueryui.pushButton_result_4]},\
                    '理之冠': {'labels': [self.reliqueryui.label_name_5, self.reliqueryui.label_stat_5, self.reliqueryui.label_type_5, self.reliqueryui.label_quality_5,self.reliqueryui.label_mainstat_5], \
						'buttons': [self.reliqueryui.pushButton_icon_5, self.reliqueryui.pushButton_result_5]}}
		for i in results:
			if i in controls:
				#change the text of controls
				controls[i]['labels'][0].setText('名字：'+results[i]['名字'])#name
				controls[i]['labels'][1].setText('副词条：\n'+'\n'.join([j+'：'+str(results[i]['副词条'][j]) for j in results[i]['副词条']]))#substats
				controls[i]['labels'][2].setText('圣遗物类型：'+i)#reliquery type
				controls[i]['labels'][3].setText(
					f"星级：{str(results[i]['星级'])} 等级：{str(results[i]['等级'])}")
				controls[i]['labels'][4].setText('主词条：'+list(results[i]['主词条'].keys())[0]+'：'+str(list(results[i]['主词条'].values())[0]))
				# print(results[i]['评分'])
				controls[i]['buttons'][1].setText(results[i]['评分'])


	def gachaResultExport(self,link):
		'''Gacha result to charts , including bar , line , and pie'''
		analyser=ga.GachaAnalyser()
		return analyser.getdata()
class reliqueryResult(QMainWindow,Ui_reliqueryResult):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
if __name__=='__main__':
	app=QApplication(sys.argv)
	m=main()
	sys.exit(app.exec_())