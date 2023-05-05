#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
from flask import redirect, Flask, make_response, request, render_template, session, Response, url_for
import MySQLdb
selected_credits = 0
app = Flask(__name__)


conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="dbsys_work")
temp_studentID = ""

@app.route('/')                #根目錄
@app.route('/index')           #首頁
def index():                   #導向Course_Selection.html
    
    return  render_template('Course_Selection.html')

@app.route('/Course_Selection', methods=['POST'])  #當有表單傳送的時候執行
def Course_Selection():
    global selected_credits
    # 取得輸入的文字
    if 'search' in request.form:
        if request.form['search']=='查詢已選課程':
            student_id = request.form.get("student_id")     #輸入學號
            # 建立課程清單 之後可以獨立成function 就不用在del add那邊重複程式碼
            course_info = {
                'course_id' : [],          #存入list傳入html顯示
                'course_name' : [],
                'department_id' : [],
                'grade' : [],
                'course_type' : [],
                'mnos' : [],
                'cnos' : [],
                'cs' : [],
                'credit' : []
            }
            query = "SELECT * FROM enrollment where StudentID = '{}';".format(student_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法



            for (course_id, std_id) in cursor.fetchall():  #使用 fetchall() 查詢結果。
                search_course = "SELECT * FROM course where courseID = '{}';".format(course_id) #查詢指定課程ID的所有課程紀錄
                cursor.execute(search_course)                                                       #查詢語法
                course_data = cursor.fetchone()                                                     #查询了一条记录，其中包含两个字段 course_name 和 course_id，那么cursor.fetchone() 方法将返回一个包含这两个字段值的元组
                for i, keys in enumerate(course_info.keys()):
                    course_info[keys].append(course_data[i])
            resp = make_response('Setting a cookie') #原本要設cookie 但不知道為什麼set不起來 如果有set起來del那邊就不用寫的那麼醜了
            resp.set_cookie('username', student_id)   #暫時無用，也別註解放著就好
            #計算學分總和
            query = "SELECT SUM(Course.CourseCredit) FROM enrollment INNER JOIN Course ON enrollment.CourseID = Course.CourseID WHERE enrollment.StudentID = '{}';".format(student_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法
            selected_credits=cursor.fetchone()
            return render_template("Course_Selection.html", course_info = course_info, len = len(course_info['cs']), student_id = student_id,search_type = 0,selected_credits=selected_credits)  #len是計算有幾筆資料
        elif request.form['search'] == '查詢可選課程':
            
            student_id = request.form.get("student_id")
            course_info = {
                'course_id' : [],          #存入list傳入html顯示
                'course_name' : [],
                'department_id' : [],
                'grade' : [],
                'course_type' : [],
                'mnos' : [],
                'cnos' : [],
                'cs' : [],
                'credit' : []
            }


            query = "SELECT *FROM course WHERE CNOS < MNOS AND CourseID NOT IN (SELECT CourseID FROM enrollment WHERE StudentID = '{}');".format(student_id)    #60人以內的課程條件
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)


            for (course_id, _,_,_,_,_,_,_,_) in cursor.fetchall():  #使用 fetchall() 查詢結果。           #錯誤在這，找到的資料欄位過多，但只有兩個可以放
                search_course = "SELECT * FROM course where courseID = '{}';".format(course_id) #查詢指定課程ID的所有課程紀錄
                cursor.execute(search_course)                                                       #查詢語法
                course_data = cursor.fetchone()                                                     #查询了一条记录，其中包含两个字段 course_name 和 course_id，那么cursor.fetchone() 方法将返回一个包含这两个字段值的元组
                for i, keys in enumerate(course_info.keys()):
                    course_info[keys].append(course_data[i])
            resp = make_response('Setting a cookie') #原本要設cookie 但不知道為什麼set不起來 如果有set起來del那邊就不用寫的那麼醜了
            resp.set_cookie('username', student_id)   #暫時無用，也別註解放著就好
            #計算學分總和
            query = "SELECT SUM(Course.CourseCredit) FROM enrollment INNER JOIN Course ON enrollment.CourseID = Course.CourseID WHERE enrollment.StudentID = '{}';".format(student_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法
            selected_credits=cursor.fetchone()
            return render_template("Course_Selection.html", course_info = course_info, len = len(course_info['cs']), student_id = student_id,search_type = 1,selected_credits=selected_credits)  #len是計算有幾筆資料

            # 與已選課程差不多寫法 只是要加上不要列出來的課程的條件 如已選 衝堂etc
            pass
    elif 'del' in request.form: #退選
        course_status=0
        course_id = request.form.get("course_id")  #抓課程ID
        query = "SELECT CourseType FROM course WHERE CourseID = '{}';".format(course_id)
        cursor = conn.cursor()   #獲取資料庫的資料
        cursor.execute(query)    #查詢語法
        course_status=cursor.fetchone()

        if int(selected_credits[0]) > 9 and int(course_status[0])==1:
            

        # 因為cookie不知道為什麼存不下來 所以先用這個暴力寫法 如果存得下來就直接取cookie
            for k in request.form.keys():
                if "D" in k:
                    student_id = k
            course_id = request.form.get("course_id")  #抓課程ID

        # 從資料庫中刪除
            print("DELETE FROM enrollment where CourseID = '{}' AND StudentID = '{}' ;".format(course_id, student_id))
            query = "DELETE FROM enrollment where CourseID = '{}' AND StudentID = '{}' ;".format(course_id, student_id)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()                      #修改資料庫才會用到
            #cnos-1
            print("UPDATE course SET CNOS = CNOS - 1 WHERE CourseID ='{}';".format(course_id))
            query = "UPDATE course SET CNOS = CNOS - 1 WHERE CourseID ='{}';".format(course_id)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()   

            # 把目前的課程再列出來
            course_info = {
                    'course_id' : [],          #存入list傳入html顯示
                    'course_name' : [],
                    'department_id' : [],
                    'grade' : [],
                    'course_type' : [],
                    'mnos' : [],
                    'cnos' : [],
                    'cs' : [],
                    'credit' : []
                }
            query = "SELECT * FROM enrollment where StudentID = '{}';".format(student_id)
            cursor = conn.cursor()
            cursor.execute(query)
            for (course_id, std_id) in cursor.fetchall():
                search_course = "SELECT * FROM course where courseID = '{}';".format(course_id)
                cursor.execute(search_course)
                course_data = cursor.fetchone()
                for i, keys in enumerate(course_info.keys()):
                    course_info[keys].append(course_data[i])
            print(course_info)
            resp = make_response('Setting a cookie') #暫時無用
            resp.set_cookie('username', student_id)  #暫時無用
            return render_template("Course_Selection.html", course_info = course_info, len = len(course_info['cs']), student_id = student_id,search_type = 0)
        elif int(course_status[0])==1:
            print(selected_credits)
            waring="你不能退，低於學分限制"
            return render_template("Course_Selection.html",waring=waring)
        else:
            print(selected_credits)
            waring="你不能退，此課為必修"
            return render_template("Course_Selection.html",waring=waring)           
    
    elif 'add' in request.form: #加選 同del寫法
        if int(selected_credits[0]) < 30:
            # 因為cookie不知道為什麼存不下來 所以先用這個暴力寫法 如果存得下來就直接取cookie
  


            for k in request.form.keys():
                if "D" in k:
                    student_id = k
            course_id = request.form.get("course_id")  #抓課程ID

            ##不可加選衝堂的課程；

            query = "SELECT CS FROM COURSE where CourseID = '{}';".format(course_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法
            course_time=cursor.fetchone()

            query = "SELECT course.CS FROM course INNER JOIN enrollment ON course.CourseID = enrollment.CourseID WHERE enrollment.StudentID	= '{}';".format(student_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法
            en_course_time=cursor.fetchall()


            for ect in en_course_time:
                if ect == course_time:
                    waring="你不能加，衝堂"
                    return render_template("Course_Selection.html",waring=waring)
                

            query = "SELECT CourseName FROM COURSE where CourseID = '{}';".format(course_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法
            course_name=cursor.fetchone()

            query = "SELECT course.CourseName FROM course INNER JOIN enrollment ON course.CourseID = enrollment.CourseID WHERE enrollment.StudentID	= '{}';".format(student_id)
            cursor = conn.cursor()   #獲取資料庫的資料
            cursor.execute(query)    #查詢語法
            en_course_name=cursor.fetchall()


            for ect in en_course_name:
                if ect == course_name:
                    waring="你不能加，不可加選同名課程"
                    return render_template("Course_Selection.html",waring=waring)     
                





                
            


        # 從資料庫中刪除
            print("INSERT INTO enrollment (CourseID, StudentID) VALUES ('{}', '{}');".format(course_id, student_id))
            query = "INSERT INTO enrollment (CourseID, StudentID) VALUES ('{}', '{}');".format(course_id, student_id)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()                      #修改資料庫才會用到
            #cnos+1
            print("UPDATE course SET CNOS = CNOS + 1 WHERE CourseID ='{}';".format(course_id))
            query = "UPDATE course SET CNOS = CNOS + 1 WHERE CourseID ='{}';".format(course_id)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()         

            # 把目前的課程再列出來
            course_info = {
                    'course_id' : [],          #存入list傳入html顯示
                    'course_name' : [],
                    'department_id' : [],
                    'grade' : [],
                    'course_type' : [],
                    'mnos' : [],
                    'cnos' : [],
                    'cs' : [],
                    'credit' : []
                }
            query = "SELECT * FROM enrollment where StudentID = '{}';".format(student_id)
            cursor = conn.cursor()
            cursor.execute(query)
            for (course_id, std_id) in cursor.fetchall():
                search_course = "SELECT * FROM course where courseID = '{}';".format(course_id)
                cursor.execute(search_course)
                course_data = cursor.fetchone()
                for i, keys in enumerate(course_info.keys()):
                    course_info[keys].append(course_data[i])
            print(course_info)
            resp = make_response('Setting a cookie') #暫時無用
            resp.set_cookie('username', student_id)  #暫時無用
            return render_template("Course_Selection.html", course_info = course_info, len = len(course_info['cs']), student_id = student_id,search_type = 0)
        else:
            print(selected_credits)
            waring="你不能加"
            return render_template("Course_Selection.html",waring=waring)










#html部分可以把它拆開來 用extends 看起來不會這麼大一坨
