#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sqlite3

def storageSQL(subject,teacher,time,locate,progress,UserName,marker):
   c=CourseSQL('course.db') 
   c.insert(subject,teacher,time,locate,progress,UserName,marker)

class CourseSQL:
    db_name=None
    conn=None 
    cursor=None

    def __init__(self,db_name):
        self.__createSQL(db_name)
        self.db_name=db_name 

    def __createSQL(self,db_name):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS course(
                        实验项目 nchar(50),
                        指导老师 nchar(20),
                        实验时间 nchar(50),
                        实验地点 nchar(30),
                        预约进度 nchar(10),
                        UserName nchar(20),
                        marker int,
                        primary key(实验项目,指导老师,实验时间,实验地点,预约进度,UserName)
                )''')
        self.conn.commit()

    def insert(self,subject,teacher,time,locate,progress,UserName,marker):
        try:
            self.cursor.execute('INSERT INTO course VALUES(?,?,?,?,?,?,?)',(subject,teacher,time,locate,progress,UserName,marker))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def __history_exists(self):
        try:
            a=self.cursor.execute('SELECT * FROM course_history')
        except sqlite3.OperationalError :
            return False 
        return True

    def update(self):
        # 比较两个数据表，将重复的内容添加标记
        try:
            if self.__history_exists():
                self.cursor.execute('''update course set marker=0 where (SELECT 实验时间,指导老师,实验时间,实验地点,预约进度,UserName FROM course)=(SELECT 实验时间,指导老师,实验时间,实验地点,预约进度,UserName FROM course_history)''')
                self.conn.commit()
        except:
            return False 
        return True

    def move(self):
        try:
            if self.__history_exists():
                self.cursor.execute('''drop table course_history''')
            self.cursor.execute('''ALTER TABLE course RENAME TO course_history''')
            self.conn.commit()
        except:
            return False
        return True

    def output(self,file_path,UserName):
        count=0
        self.cursor.execute('SELECT * FROM course WHERE UserName=\''+UserName+'\' AND marker=1')
        content=self.cursor.fetchall()
        f=open(file_path,'w+',encoding='utf-8')
        for i in content:
            #if ((i[5]==UserName) and i[6]==1):
            count=count+1
            f.write('[课程]实验项目：'+i[0]+'\n')
            f.write('指导老师：'+i[1]+'\n')
            f.write('实验时间：'+i[2]+'\n')
            f.write('实验地点：'+i[3]+'\n')
            f.write('预约进度：'+i[4]+'\n')
            f.write('----------\n')
        f.close()
        return count

    def close(self):
        self.conn.close()
            

