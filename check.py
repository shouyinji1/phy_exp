#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time
import os 
from bs4 import BeautifulSoup

import sendEmail
import sendqq
import sendSMS

class Sjjx_Form_Data:
    login_url='http://sjjx.hyit.edu.cn/syjx'
    Form_Data={
        '__VIEWSTATE':'',
        '__EVENTVALIDATION':'',
        'Login1$UserName':'',
        'Login1$PassWord':'',
        'Login1$ImageButton1.x':'',
        'Login1$ImageButton1.y':'',
        'Link':''
    }

    def __init__(self,UserName,PassWord):
        self.Form_Data['__VIEWSTATE']=self.get_VIEWSTATE() 
        self.Form_Data['__EVENTVALIDATION']=self.get_EVENTVALIDATION()
        self.Form_Data['Login1$UserName']=UserName 
        self.Form_Data['Login1$PassWord']=PassWord
        self.Form_Data['Login1$ImageButton1.x']=19
        self.Form_Data['Login1$ImageButton1.y']=15
        self.Form_Data['Link']='http://www.baidu.com'

    def get_content(self):
        re=requests.get(self.login_url)
        return(BeautifulSoup(re.text, "html.parser"))

    def get_VIEWSTATE(self):
        return(self.get_content().find(id='__VIEWSTATE').get('value'))

    def get_EVENTVALIDATION(self):
        return(self.get_content().find(id='__EVENTVALIDATION').get('value'))


class Sjjx_login(Sjjx_Form_Data):
    login_headers={
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    open_headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'sjjx.hyit.edu.cn',
        'Referer': 'http://sjjx.hyit.edu.cn/syjx/student/xs_left.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    query_data={
        'sid':'',
        'screen':''
    }
    table_request_headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'sjjx.hyit.edu.cn',
        'Origin': 'http://sjjx.hyit.edu.cn',
        'Referer': 'http://sjjx.hyit.edu.cn/syjx/student/kblist.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    table_form_data={
        '__EVENTTARGET': 'ddlCurrentPage',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS':'', 
        '__VIEWSTATE':'',
        '__VIEWSTATEENCRYPTED':'', 
        'ddlCurrentPage': '2' 
    }
    login_url='http://sjjx.hyit.edu.cn/syjx/index.aspx'
    index_url='http://sjjx.hyit.edu.cn/syjx/student/kblist.aspx'
    buff=None
    session=requests.Session()

    def __init__(self,UserName,PassWord):
        super(Sjjx_login,self).__init__(UserName,PassWord)
        self.buff=self.login().text
        self.query_data['sid']=self.get_sid()
        self.query_data['screen']=self.get_screen() 

    def login(self):
        return self.session.post(self.login_url, data=super().Form_Data, headers=self.login_headers)

    def get_index(self):
        return self.session.get(self.index_url, data=self.query_data,headers=self.open_headers)

    def get_sid(self):
        pat=re.compile('sid='+'(.*?)'+'&',re.S)
        return pat.findall(self.buff)[0]

    def get_screen(self):
        pat=re.compile('screen'+'(.*?)'+'">',re.S)
        return pat.findall(self.buff)[0]

    def get_tables(self):
        tables=[]
        soup=BeautifulSoup(self.get_index().text, 'html.parser')
        tables.append(str(soup.find(class_='gridview_m')))

        self.table_form_data['__VIEWSTATE']=soup.find(id='__VIEWSTATE').get('value')
        self.table_form_data.update(self.query_data)
        table_option=soup.find(id='ddlCurrentPage').find_all('option')
        for i in range(1,len(table_option)):
            self.table_form_data['ddlCurrentPage']=table_option[i]['value']
            table_temp=str(self.session.post(self.index_url,data=self.table_form_data,headers=self.table_request_headers).text)
            soup_temp=BeautifulSoup(table_temp,'html.parser')
            table_temp=str(soup_temp.find(class_='gridview_m'))
            tables.append(table_temp)
        return tables


class Html_Table:
    soup=None
    line_count=None
    column_count=None
    def __init__(self,table):
        self.soup=BeautifulSoup(table, 'html.parser')
        self.line_count=len(self.table())
        self.column_count=len(self.line(1))

    def table(self):
        return self.soup.find_all('tr')

    def line(self,table_index):
        return self.table()[table_index].find_all('td')

    def element(self,table_index,line_index):
        return self.line(table_index)[line_index]

    def element_text(self,table_index,line_index):
        return self.line(table_index)[line_index].text

    def title(self):
        return self.table()[0].find_all('th')

    def title_text(self,index):
        return self.title()[index].text

    def get_element_URL(self,line_index,column_index):
        temp=self.element(line_index,column_index).a
        if temp == None:
            return False
        else:
            return temp['href']


def getCampus(session,url_path):
    request_headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'sjjx.hyit.edu.cn',
        'Referer': 'http://sjjx.hyit.edu.cn/syjx/student/kblist.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    course_url='http://sjjx.hyit.edu.cn/syjx/student/'+str(url_path) 
    return session.get(course_url,headers=request_headers)


class Course:
    session=None 
    soup=None 
    form_data={
        '__EVENTTARGET': 'ddlxq',
        '__EVENTARGUMENT':'', 
        '__LASTFOCUS':'', 
        '__VIEWSTATE': '',
        '__VIEWSTATEENCRYPTED':'', 
        'ddlxq':'8' # 7 北京路
                    # 8 枚乘路
                    # 9 萧湖校区
    }
    request_headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'sjjx.hyit.edu.cn',
        'Origin': 'http://sjjx.hyit.edu.cn',
        'Referer': 'http://sjjx.hyit.edu.cn/syjx/student/yykblist.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    table_form_data={
        '__EVENTTARGET': 'ddlCurrentPage',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS':'', 
        '__VIEWSTATE':'',
        '__VIEWSTATEENCRYPTED':'', 
        'ddlxq':form_data['ddlxq'],
        'ddlCurrentPage': '2' 
    }
    course_url='http://sjjx.hyit.edu.cn/syjx/student/'
    target_content=None

    def __init__(self,session,getCampus,ddlxq,url_path):
        self.session=session 
        self.soup=BeautifulSoup(getCampus,'html.parser')
        self.form_data['__VIEWSTATE']=self.get_VIEWSTATE()
        self.form_data['ddlxq']=ddlxq
        self.course_url=self.course_url+str(url_path)
        self.target_content=self.post().text

    def get_VIEWSTATE(self):
        return self.soup.find(id='__VIEWSTATE').get('value')

    def post(self):
        return self.session.post(self.course_url,data=self.form_data,headers=self.request_headers)

    def get_tables(self):
        tables=[]
        soup=BeautifulSoup(self.target_content,'html.parser')
        tables.append(str(soup.find(class_='gridview_m')))

        self.table_form_data['__VIEWSTATE']=soup.find(id='__VIEWSTATE').get('value')
        table_option=soup.find(id='ddlCurrentPage').find_all('option')
        for i in range(1,len(table_option)):
            self.table_form_data['ddlCurrentPage']=table_option[i]['value']
            table_temp=str(self.session.post(self.course_url,data=self.table_form_data,headers=self.request_headers).text)
            soup_temp=BeautifulSoup(table_temp,'html.parser')
            table_temp=str(soup_temp.find(class_='gridview_m'))
            tables.append(table_temp)
        return tables


def check_class(UserName,PassWord,campus):
    count=0
    phy_exp='./phy_exp_'+str(UserName)+'.txt'
    f=open(phy_exp,'w+')
    s=Sjjx_login(UserName,PassWord)
    tables=s.get_tables()
    for k in tables:
        table=Html_Table(str(k))
        for i in range(1,table.line_count):
            course_URL = table.get_element_URL(i,4)
            if course_URL:
                course=Course(s.session,getCampus(s.session,course_URL).text,campus,course_URL)
                class_tables=course.get_tables()
                for j in class_tables:
                    #print(j)
                    class_table=Html_Table(str(j))
                    for n in range(1,class_table.line_count):
                        result=class_table.element(n,6).input['value']
                        if result != '人数已满':
                            count=count+1
                            for m in range(0,class_table.column_count-1):
                                f.write(str(class_table.title_text(m)).strip()+'：'+str(class_table.element_text(n,m)).strip()+'\n')
                            f.write('程序查询时间：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
                            f.write('----------\n')
    f.write('\n==========\n')
    f.write('可选课程数量：'+str(count)+'\n')
    f.write('程序检测时间：'+time.strftime("%Y-%m-%d %H:%M:%S"+'\n', time.localtime()))
    f.write('=========='+'\n')
    f.close()
    if count>0 :
        return phy_exp
    else:
        return False


def door(user):
    try:
        information=check_class(user['UserName'],user['PassWord'],user['campus'])
        if information:
            if user['email']:
                sendEmail.sendEmail(information,user['email'])
            if user['qq']:
                sendqq.sendqq(information,user['qq'],user['qq_type'])
            if user['to_phone']:
                sendSMS.sendSMS(user['to_phone'])
    except Exception as ex:
        f=open('./phy_exp.log','a+')
        f.write('发生异常\n')
        f.write(str(ex)+'\n')
        f.write(str(user['UserName'])+'\n')
        f.write('\n程序检测时间：'+time.strftime("%Y-%m-%d %H:%M:%S"+'\n', time.localtime()))
        f.write('----------\n')
        f.close()
        sendEmail.sendEmail('./phy_exp.log')

