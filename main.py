#!/usr/bin/python3
# -*- coding: utf-8 -*-

import check
from hyit_login import hyit_login 


if __name__ == '__main__':
    # 淮阴工学院上网认证系统账号密码
    hyit_login('账号',‘密码’)

    # 检测账号信息
    users=[
        {
            'UserName':'帐号',
            'PassWord':'密码',
            'campus':'8',   # 校区
            'email':'接收邮箱',
            'qq':'QQ昵称',
            'qq_type':'QQ类型',
            'to_phone':'+86接收手机号'
        },        
        {
            'UserName':'帐号',
            'PassWord':'密码',
            'campus':'8',   #校区
            'email':'接收邮箱',
            'qq':'QQ昵称',
            'qq_type':'QQ类型',
            'to_phone':None
        },        
    ]

    myBug=False
    for user in users:
        try:
            check.door(user)
        except Exception as ex:
            myBug=True
            f=open('./phy_exp.log','a+')
            f.write('发生异常\n')
            f.write(str(ex)+'\n')
            f.write(str('问题发生帐号：'+user['UserName'])+'\n')
            f.write('\n程序检测时间：'+time.strftime("%Y-%m-%d %H:%M:%S"+'\n', time.localtime()))
            f.write('----------\n')
            f.close()
    sendEmail.sendEmail('./phy_exp.log','邮箱帐号')

