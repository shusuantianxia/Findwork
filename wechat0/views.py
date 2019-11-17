#coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
# Create your views here.
def weixin_main(request, companyone, companytwo, companythree, companyfour, personone, persontwo, percent1, percent2, percent3, percent4):
    #第一部分
    #工作因素
    suitability1 = int(percent1)
    #买房因素
    data1 = pd.read_csv('E:/work/wechat0/houseprice.csv')
    data = np.array(data1).reshape(-1, 3)
    e = len(data)
    for i in range(e):
        data[i, 1] = data[i, 1] + '市'
    data = data[:, 1:]
    min0 = min(data[:, 1])
    max0 = max(data[:, 1])
    a = len(data)
    for i in range(a):
        if companytwo == str(data[i, 0]) or companytwo + '市' == str(data[i, 0]):
            companytwo0 = int(data[i, 1])
    housep = float((companytwo0 - int(min0))/(int(max0) - int(min0)))
    suitability2 = 100 - int(percent2) * housep
    #本地异地
    data2 = pd.read_csv('E:/work/wechat0/city_province.csv')
    data2 = np.array(data2).reshape((-1, 3))

    b = len(data2)
    for i in range(b):
        data2[i, 2] = data2[i, 2].strip('\t')
        data2[i, 1] = data2[i, 1].strip('\t')
    if companytwo == persontwo:
        suitability3 = 1
        if int(percent1) < 50 and int(percent3) > 50:
            area = '在自己的城市生根发芽，不追求轰轰烈烈，只愿生活快乐平凡。'
        elif int(percent1) < 50 and int(percent3) < 50:
            area = '随遇而安。'
        elif int(percent1) > 50 and int(percent3) < 50:
            area = '幸运的你，无须去往远方，就能拥有美好的工作前景。'
        elif int(percent1) > 50 and int(percent3) > 50:
            area = '在自己的地盘拥有美好明天。'
        else:
            area = '同省同市'

    else:
        for i in range(b):
            if companytwo == data2[i, 2]:
                companytwo1 = data2[i, 1]
        for j in range(b):
            if persontwo == data2[j, 2]:
                persontwo1 = data2[j, 1]
        if companytwo1 == persontwo1:
            suitability3 = 0.5
            if int(percent1) < 50 and int(percent3) > 50:
                area = '生活不易，远离自己的城市是你的底线，但是坚决不出省。'
            elif int(percent1) < 50 and int(percent3) < 50:
                area = '哎呦，工作的地方离家不远哦。'
            elif int(percent1) > 50 and int(percent3) < 50:
                area = '在自己的省闯出属于自己的一片天。'
            elif int(percent1) > 50 and int(percent3) > 50:
                area = '鱼和熊掌不可兼得，那就同时拿到虾和熊掌。'
            else:
                area = '同省异市'

        else:
            suitability3 = 0.2
            if int(percent1) < 50 and int(percent3) > 50:
                area = '远走他乡的人心底都有一个召唤自己回去的故土。'
            elif int(percent1) < 50 and int(percent3) < 50:
                area = '工作无所谓，离家无所谓，我只是一名浪子。'
            elif int(percent1) > 50 and int(percent3) < 50:
                area = '衣锦还乡时，才能倾述漂泊的苦楚。'
            elif int(percent1) > 50 and int(percent3) > 50:
                area = '忍一忍，还是先赚钱吧。'
            else:
                area = '异省异市'

    suitability3 = 100 - int(percent3) * suitability3
    #生活质量
    for i in range(b):
        if companytwo == data2[i, 2]:
            companytwo2 = data2[i, 1]
    data3 = pd.read_csv('E:/work/wechat0/province_consume.csv')
    data3 = np.array(data3).reshape(-1, 3)
    c = len(data3)
    for i in range(c):
        if companytwo2 == data3[i, 2]:
            companytwo3 = data3[i, 1]
    if float(companyfour) > float(companytwo3):
        suitability4 = 0.5 + float((float(companyfour) - float(companytwo3)) / float(companytwo3))
    else:
        suitability4 = 0.5 - float((float(companytwo3) - float(companyfour)) / float(companytwo3))
    if suitability4 > 1:
        suitability4 =1
    if suitability4 < 0:
        suitability4 = 0
    suitability4 = 100 - int(percent4) * suitability4
    
    suitability = suitability1 + suitability2 + suitability3 + suitability4
    suitability = 100 * (suitability / (int(percent1) + int(percent4) + int(percent3) + int(percent2)))
    suitability = round(suitability, 2)
    if suitability < 60:
        pj = '请再慎重考虑！！'
    elif 60 < suitability and suitability < 80:
        pj = '可能有更好地选择！！'
    elif suitability > 80 and suitability < 90:
        pj = '这是一个好的工作，恭喜你！'
    else:
        pj = '太棒了，这是一份非常好的工作！祝贺你！'
    suitability = str(suitability) + '%'

    # 第二部分
    #生活质量
    data4 = data3[:, :-1].reshape(-1, 2)
    data5 = data3[:, 1:].reshape(-1, 2)
    data6 = data4[np.lexsort(-data4.T)]
    for i in range(c):
        for j in range(c):
            if float(data6[i, 1]) == float(data5[j, 0]):
                data6[i, 0] = data5[j, 1]
    data7 = np.arange(1, c + 1).reshape(-1, 1)
    data6 = np.concatenate((data6, data7), axis=1)
    for i in range(c):
        if companytwo2 == data6[i, 0]:
            consume0 = data6[i, 0]
            consume1 = data6[i, 1]
            consume2 = data6[i, 2]
    #当地房价

    data8 = pd.read_csv('E:/work/wechat0/houseprice.csv')
    data8 = np.array(data8).reshape(-1, 3)
    d = len(data8)
    for i in range(d):
        data8[i, 1] = data8[i, 1] + '市'
    data9 = np.concatenate((data8[:, 0].reshape(-1, 1), data8[:, 2].reshape(-1, 1)), axis=1)
    data10 = data8[:, 1:].reshape(-1, 2)
    data11 = data9[np.lexsort(-data9.T)]
    for i in range(d):
        for j in range(d):
            if float(data11[i, 1]) == float(data10[j, 1]):
                data11[i, 0] = data10[j, 0]
    data12 = np.arange(1, d + 1).reshape(-1, 1)
    data11 = np.concatenate((data11, data12), axis=1)
    for i in range(d):
        if companytwo == data11[i, 0] or companytwo + '市' == data11[i, 0]:
            house0 = data11[i, 0]
            house1 = data11[i, 1]
            house2 = data11[i, 2]
    print()

    #结果
    return JsonResponse({'data': suitability, 'shdq': consume0, 'xfsp': consume1, 'pm': consume2, 'bdyd': area, 'house0': house0, 'house1': house1, 'house2': house2, 'pj': pj})