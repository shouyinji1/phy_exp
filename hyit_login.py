#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request, parse

#userName=input("Your userName: ")
#pwd=input("Your password: ")
#rememberPwd=input("Whether Remember login status? (1=true,0=false): ")


def hyit_login(userName,pwd,rememberPwd=1)
    #print("登陆淮阴工学院上网认证系统")
    post_url='http://172.16.5.73/portal/login.php'
    post_data={
        'opr':'pwdLogin',
        'userName':userName,
        'pwd':pwd,
        'rememberPwd':rememberPwd
    }

    data = parse.urlencode(post_data).encode('utf-8')
    req=request.Request(post_url,data=data)
    page=request.urlopen(req).read()
    return(page.decode('utf-8'))

