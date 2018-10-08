#!/usr/bin/python3
# coding: utf-8

import smtplib
from email import encoders 
from email.header import Header 
from email.mime.text import MIMEText 
from email.utils import parseaddr 
from email.utils import formataddr 

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))

def sendEmail(phy_exp,to_email):
    from_email = "邮箱帐号"
    from_email_pwd = "邮箱密码"
    smtp_server = "smtp.126.com"

    f=open(phy_exp,'a+')
    f.write(phy_exp+'\n')
    f.close()

    f=open(phy_exp,'r')
    text=f.read()
    f.close()

    msg = MIMEText(text, "plain", "utf-8")
    msg["From"] = format_addr("%s" %(from_email))
    msg["To"] = format_addr("%s" %(to_email))
    msg["Subject"] = Header("物理实验选课提醒", "utf-8").encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_email, from_email_pwd)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()
