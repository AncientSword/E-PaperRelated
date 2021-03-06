# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 22:03:45 2021

@author: Fred Hu
"""
import random

#the list of poems
poemsList = [
        "疏影横斜水清浅",
        "暗香浮动月黄昏",
        "曾经沧海难为水",
        "除却巫山不是云",
        "心似双丝网",
        "中有千千结",
        "此情可待成追忆",
        "只是当时已惘然",
        "十年生死两茫茫",
        "不思量，自难忘",
        "身无彩凤双飞翼",
        "心有灵犀一点通",
        "人生自是有情痴",
        "此恨不关风与月",
        "落花人独立",
        "微雨燕双飞",
        "愿我如星君如月",
        "夜夜流光相皎洁",
        "多情只有春庭月",
        "犹为离人照落花",
        "从别后，忆相逢",
        "几回魂梦与君同",
        "明月不谙离恨苦",
        "斜光到晓穿朱户",
        "欲寄彩笺兼尺素",
        "山长水阔知何处",
        "伏清白以死直兮",
        "固前圣之所厚",
        "文章千古事",
        "得失寸心知",
        "羁鸟恋旧林",
        "池鱼思故渊",
        "暖暖远人村",
        "依依墟里烟",
        "天若有情天亦老",
        "人间正道是沧桑",
        "雄关漫道真如铁",
        "而今迈步从头越",
        "沾衣欲湿杏花雨",
        "吹面不寒杨柳风",
        "采菊东篱下",
        "悠然现南山",
        "我欲因之梦吴越",
        "一夜飞渡镜湖月",
        "舟遥遥以轻飏",
        "风飘飘而吹衣",
        "度尽劫波兄弟在",
        "相逢一笑泯恩仇",
        "大行不顾细谨",
        "大礼不辞小让",
        "其人虽已没",
        "千载有余情",
        "出师未捷身先死",
        "常使英雄泪满襟",
        "昆山玉碎凤凰叫",
        "芙蓉泣露香兰笑",
        "三顾频烦天下计",
        "两朝开济老臣心",
        "我自横刀向天笑",
        "去留肝胆两昆仑",
        "忧劳可以兴国",
        "逸豫可以亡身",
        "清水出芙蓉",
        "天然去雕饰",
        "东边日出西边雨",
        "道是无晴却有晴",
        "盈盈一水间",
        "脉脉不得语",
        "观古今于须臾",
        "抚四海于一瞬",
        "吞二周而亡诸侯",
        "履至尊而制六合",
        "两情若是久长时",
        "又岂在朝朝暮暮",
        "九死南荒吾不恨",
        "兹游奇绝冠平生",
        "盈盈荷瓣风前落",
        "片片桃花雨后娇",
        "缺月挂疏桐",
        "漏断人初静",
        "心事浩茫连广宇",
        "于无声处听惊雷",
        "但愿苍生俱饱暖",
        "不辞辛苦出山林",
        "死去何所道",
        "托体同山阿",
        "可堪孤馆闭春寒",
        "杜鹃声里斜阳暮",
        "临晚镜，伤流景",
        "往事后期空记省",
        "沙上并禽池上暝",
        "云破月来花弄影",
        "山随平野尽",
        "江入大荒流",
        "凭君莫话封侯事",
        "一将功成万骨枯",
        "行到水穷处",
        "坐看云起时",
        "今朝有酒今朝醉",
        "明日愁来明日愁",
        "楼上黄昏欲望休",
        "玉梯横绝月如钩",
        "溪云初起日沉阁",
        "山雨欲来风满楼",
        "盘龙随镜隐",
        "彩凤逐帷低",
        "穷则独善其身",
        "达则兼济天下",
        "仓廪实而知礼节",
        "衣食足而知荣辱",
        "非学无以广才",
        "非志无以成学",
        "非淡泊无以明志",
        "非宁静无以致远",
        "余霞散成绮",
        "澄江静如练",
        "草枯鹰眼疾",
        "雪尽马蹄轻",
        "念天地之悠悠",
        "独怆然而涕下",
        "海内存知己",
        "天涯若比邻",
        "落霞与孤鹜齐飞",
        "秋水共长天一色",
        "海上生明月",
        "天涯共此时",
        "野旷天低树",
        "江清月近人",
        "黄沙百战穿金甲",
        "不破楼兰终不还",
        "大鹏一日同风起",
        "扶摇直上九万里",
        "仰天大笑出门去",
        "我辈岂是蓬蒿人",
        "兴酣落笔摇五岳",
        "诗成笑傲凌沧海",
        "天意怜幽草",
        "人间重晚晴",
        "博观而约取",
        "厚积而薄发",
        "江山代有才人出",
        "各领风骚数百年",
        "云想衣裳花想容",
        "春风拂槛露华浓",
        "纵使晴明无雨色",
        "入云深处亦沾衣",
        "春风得意马蹄疾",
        "一日看尽长安花",
        "别有幽愁暗恨生",
        "此时无声胜有声",
        "同是天涯沦落人",
        "相逢何必曾相识",
        "天阶夜色凉如水",
        "卧看牵牛织女星",
        "不畏浮云遮望眼",
        "只缘身在最高层",
        "天接云涛连晓雾",
        "星河欲转千帆舞",
        "操千曲而后晓声",
        "观千剑而后识器",
        "登山则情满于山",
        "观海则意溢于海",
        "无情未必真豪杰",
        "怜子如何不丈夫",
        "书痴者文必工",
        "艺痴者技必良",
        "假作真时真亦假",
        "无为有处有还无",
        "春心莫共花争发",
        "一寸相思一寸灰",
        "梨花院落溶溶月",
        "柳絮池塘淡淡风"]

poemsListLength = len(poemsList) / 2 - 1

lengthIndexDict = { 7 : 200,
                   6 : 210,
                   5 : 225}

#get random poem
def getRandomPoem():
    poemIndex = random.randint(0, poemsListLength)
    poemFirst = poemsList[poemIndex * 2]
    poemSecond = poemsList[poemIndex * 2 + 1]
    return poemFirst, poemSecond

#get index of X for poem
def getPoemX(length):
    return lengthIndexDict[length]