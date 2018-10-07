#!/usr/bin/python3
# -*- coding: utf-8 -*-

import check


if __name__ == '__main__':
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

    for user in users:
        check.door(user)
