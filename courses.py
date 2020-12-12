import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def get():
    
    params = request.args
    student_id = params.get("studentId")
    instructor_id = params.get("instructorId")
    conn = None
    cursor = None
    result = None
        
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if student_id != None:
            cursor.execute("SELECT c.* FROM users u INNER JOIN student_register sr INNER JOIN courses c ON sr.student_id = u.id AND sr.course_id = c.id  WHERE u.id =?",[student_id,])
        elif instructor_id !=None:
            cursor.execute("SELECT c.* FROM users u INNER JOIN instructor_teaches it INNER JOIN courses c ON it.instructor_id=u.id AND c.id = it.course_id WHERE u.id =?",[instructor_id])
        else:
            cursor.execute("SELECT * FROM courses" )
        result = cursor.fetchall()
    except mariadb.OperationalError as e:
        message = "connection error" 
    except Exception as e:
        print(e)
        message ="somthing went wrong, probably bad params " 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (result != None or result==[]):
            courses=[]
            for row in result:
                course={
                    "id":row[0],
                    "name":row[1],
                    "credits":row[2],
                    "department":row[3]
                }
                courses.append(course)
            return Response(json.dumps(courses,default=str) ,mimetype="application/json",status=200)
        else:
            return Response(message ,mimetype="html/text",status=400)


def post():
    data=request.json
    loginToken = data.get("loginToken")
    course = data.get("courseName")
    credit = data.get("credits")
    department = data.get("department")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM users WHERE id =? AND role = ?",[user_id,"admin"])
        user = cursor.fetchall()
        if len(user)==1:
            if course !=None and course !="" and credit != None and department!=None and department !="": 
                cursor.execute("INSERT INTO courses (course_name,credits,department) VALUES (?,?,?) ",[course,credit,department])
                conn.commit()
                course_id = cursor.lastrowid
                rows=cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error" 
    except Exception as e:
        print(e)
        message ="somthing went wrong, probably bad params " 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (rows == 1):
            
            course={
                "id":course_id,
                "name":course,
                "credits":credit,
                "department":department
            }
            return Response(json.dumps(course,default=str) ,mimetype="application/json",status=200)
        else:
            return Response(message ,mimetype="html/text",status=400)




    
def update():
    data=request.json
    course_id = data.get("courseId")
    loginToken = data.get("loginToken")
    course = data.get("courseName")
    credit = data.get("credits")
    department = data.get("department")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM users WHERE id =? AND role = ?",[user_id,"admin"])
        user = cursor.fetchall()
        if len(user)==1:
            if course != None and course !="":
                cursor.execute("UPDATE courses SET course_name = ? WHERE id = ?",[course,course_id])
            if credit != None and credit !="":
                cursor.execute("UPDATE courses SET credits = ? WHERE id = ?",[credit,course_id])
            if department != None and department !="":
                cursor.execute("UPDATE courses SET department = ? WHERE id = ?",[department,course_id])
            conn.commit()
            rows=cursor.rowcount
            cursor.execute("SELECT * FROM courses WHERE id =?",[course_id])
            row = cursor.fetchone()
    except mariadb.OperationalError as e:
        message = "connection error"
        print(e) 
    except Exception as e:
        print(e)
        message ="somthing went wrong, probably bad params " 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (rows == 1):
            
            course={
                "id":row[0],
                "name":row[1],
                "credits":row[2],
                "department":row[3]
            }
            return Response(json.dumps(course,default=str) ,mimetype="application/json",status=200)
        else:
            return Response(message ,mimetype="html/text",status=400)
def delete():

    data=request.json
    course_id = data.get("courseId")
    loginToken = data.get("loginToken")
    cursor =None
    conn = None
    rows =None
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM users WHERE id =? AND role = ?",[user_id,"admin"])
        user = cursor.fetchall()
        if len(user)==1:
            cursor.execute("DELETE FROM courses WHERE id =?",[course_id])
            conn.commit()
            rows = cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error" 
    except Exception as e:
        print(e)
        message ="somthing went wrong, probably bad params " 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (rows==1):
            return Response("success" ,mimetype="html/text",status=204)
        else:
            return Response(message ,mimetype="html/text",status=400)