import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb

def get():

    result = None
    params = request.args
    loginToken = request.headers.get("loginToken")
    task_id = params.get("taskId")
    conn = None
    cursor = None
    result = None
    user_id = None
        
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("SELECT role FROM users WHERE id =?",[user_id])
            role = cursor.fetchone()
            if role[0] == "student":
                cursor.execute("SELECT * FROM student_submit ss INNER JOIN users u ON ss.student_id=u.id WHERE ss.student_id =? AND ss.task_id=?",[user_id,task_id])
            elif role[0] == "instructor":
                cursor.execute("SELECT * FROM student_submit ss INNER JOIN users u INNER JOIN tasks t INNER JOIN instructor_teaches it ON ss.student_id=u.id  and ss.task_id =t.id and t.course_id = it.course_id WHERE ss.task_id=? AND it.instructor_id=?",[task_id,user_id])
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
            submissions=[]
            for row in result:
                submission={
                    "studentId":row[1],
                    "taskId":row[2],
                    "date":row[3],
                    "grade":row[4],
                    "content":row[5],
                    "comment":row[6],
                    "name":row[8]
                }
                submissions.append(submission)
            return Response(json.dumps(submissions,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)
    


def post():
    data=request.json
    loginToken = data.get("loginToken")
    task_id=data.get("taskId")
    content=data.get("content")
    comment=data.get("comment")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u INNER JOIN student_register sr INNER JOIN tasks t ON u.id=us.user_id AND u.id = sr.student_id AND sr.course_id = t.course_id WHERE us.token = ? AND u.role = ? AND t.id=?",[loginToken,"student",task_id])
        user= cursor.fetchall()
        if len(user)==1 and task_id!=None and task_id!="" and content !=None and content !="" and comment != None and comment != "": 
            cursor.execute("INSERT INTO student_submit (student_id, task_id,content,comment) VALUES (?,?,?,?)",[user[0][0],task_id,content,comment])
            conn.commit()
            rows=cursor.rowcount
            cursor.execute("SELECT * FROM student_submit ss INNER JOIN users u ON ss.student_id=u.id WHERE ss.student_id =? AND ss.task_id=?",[user[0][0],task_id])
            result = cursor.fetchone()
        elif len(user)==1 and task_id!=None and task_id!="" and content !=None and content !="": 
            cursor.execute("INSERT INTO student_submit (student_id, task_id,content) VALUES (?,?,?)",[user[0][0],task_id,content])
            conn.commit()
            cursor.execute("SELECT * FROM student_submit ss INNER JOIN users u ON ss.student_id=u.id WHERE ss.student_id =? AND ss.task_id=?",[user[0][0],task_id])
            result = cursor.fetchone()
            rows=cursor.rowcount

        else:
            message="invalid entry"
        
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data"
    except Exception as e:
        print(e)
        message =  "somthing went wrong" 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows == 1 :
            submission={
                "studentId":result[1],
                "taskId":result[2],
                "date":result[3],
                "grade":result[4],
                "content":result[5],
                "comment":result[6],
                "name":result[8]
            }
            return Response(json.dumps(submission,default=str),mimetype="application/json" , status =201)
        else:
            return Response("failed",mimetype="text/html",status=400)


def update():
    data=request.json
    loginToken = data.get("loginToken")
    task_id=data.get("taskId")
    content=data.get("content")
    comment=data.get("comment")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u  ON u.id=us.user_id  WHERE us.token = ? ",[loginToken,])
        user= cursor.fetchall()
        if len(user)==1 and task_id!=None and task_id!="" and content !=None and content !="": 
            cursor.execute("UPDATE student_submit SET content = ? WHERE task_id=? and student_id=?",[content,task_id,user[0][0]])
        if len(user)==1 and task_id!=None and task_id!="" and comment !=None and comment !="": 
            cursor.execute("UPDATE student_submit SET comment = ? WHERE task_id=? and student_id=?",[comment,task_id,user[0][0]])
        conn.commit()
        rows=cursor.rowcount
        cursor.execute("SELECT * FROM student_submit ss INNER JOIN users u ON ss.student_id=u.id WHERE ss.student_id =? AND ss.task_id=?",[user[0][0],task_id])
        result = cursor.fetchone()
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data"
    except Exception as e:
        print(e)
        message =  "somthing went wrong" 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows == 1 :
            submission={
                 "studentId":result[1],
                "taskId":result[2],
                "date":result[3],
                "grade":result[4],
                "content":result[5],
                "comment":result[6],
                "name":result[8]
            }
            return Response(json.dumps(submission,default=str),mimetype="application/json" , status =201)
        else:
            return Response("failed",mimetype="text/html",status=400)
  
            


def delete():
    data=request.json
    loginToken = data.get("loginToken")
    task_id=data.get("taskId")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u  ON u.id=us.user_id  WHERE us.token = ? ",[loginToken,])
        user= cursor.fetchall()
        if len(user)==1 and task_id!=None and task_id!="" : 
            cursor.execute("DELETE FROM student_submit WHERE task_id=? and student_id=?",[task_id,user[0][0]])
            conn.commit()
            rows=cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data"
    except Exception as e:
        print(e)
        message =  "somthing went wrong" 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows == 1 :
    
            return Response("SUCCESS",mimetype="text/html" , status =201)
        else:
            return Response("failed",mimetype="text/html",status=400)
