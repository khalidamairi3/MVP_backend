import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def get():
    headers=request.headers
    params = request.args

    loginToken = headers.get("loginToken")
    course_id = params.get("courseId")
    task_id = params.get("taskId")
    conn = None
    cursor = None
    result = None
        
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id,u.role FROM user_session us INNER JOIN users u ON u.id =us.user_id  WHERE token = ?",[loginToken])
        user = cursor.fetchone()
        if user[1]=="student" and course_id !=None:
            cursor.execute("SELECT * FROM student_submit ss INNER JOIN tasks t INNER JOIN users u ON ss.task_id=t.id and ss.student_id = u.id WHERE t.course_id=? AND ss.student_id=? ",[course_id,user[0]])
        if user[1]=="instructor" and course_id !=None and task_id !=None:
            cursor.execute("SELECT * FROM student_submit ss INNER JOIN tasks t INNER JOIN users u ON ss.task_id=t.id and ss.student_id = u.id WHERE t.course_id=? AND ss.task_id=? ",[course_id,task_id])
        result = cursor.fetchall()
    except mariadb.OperationalError as e:
        message = "connection error" 
    except:
        message ="somthing went wrong, probably bad params " 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (result != None or result==[]):
            grades=[]
            for row in result:
                grade={
                    "taskId":row[2],
                    "studentId":row[1],
                    "name" : row[15],
                    "grade":row[4],
                    "date":row[3],
                    "published-date":row[10],
                    "title":row[13]
                }
                grades.append(grade)
            return Response(json.dumps(grades,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)

def post():
    data = request.json
    loginToken = data.get("loginToken")
    student_id = data.get("studentId")
    task_id =data.get("taskId")
    grade = data.get("grade")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id,u.role FROM user_session us INNER JOIN users u INNER JOIN instructor_teaches it INNER JOIN tasks t ON u.id =us.user_id AND u.id = it.instructor_id AND it.course_id = t.course_id  WHERE us.token = ? AND t.id=?",[loginToken,task_id])
        user = cursor.fetchone()
        if user[1]=="instructor" and student_id !=None and task_id !=None and grade != None:
            cursor.execute("UPDATE student_submit SET grade = ? WHERE student_id=? AND task_id=? ",[grade,student_id,task_id])
            conn.commit()
            rows = cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error" 
    except:
        message ="somthing went wrong, probably bad params " 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (rows==1):
            grade={
                "taskId":task_id,
                "studentId":student_id,
                "grade":grade
            }
                
            return Response(json.dumps(grade,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)