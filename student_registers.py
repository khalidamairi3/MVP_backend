import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def post():
    data=request.json
    loginToken = data.get("loginToken")
    course_id=data.get("courseId")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u ON u.id=us.user_id WHERE us.token = ? AND u.role = ?",[loginToken,"student"])
        user= cursor.fetchall()
        if len(user)==1 and course_id!=None: 
            cursor.execute("INSERT INTO student_register (student_id, course_id) VALUES (?,?)",[user[0][0],course_id,])
            conn.commit()
            rows=cursor.rowcount
        else:
            message="invalid entry"
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data"
    except:
        message =  "somthing went wrong" 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows == 1 :
            return Response("success",mimetype="html/text" , status =201)
        else:
            return Response(message,mimetype="text/html",status=400)
  
            


def delete():
    data=request.json
    loginToken = data.get("loginToken")
    course_id=data.get("courseId")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u ON u.id=us.user_id WHERE us.token = ? AND u.role = ?",[loginToken,"student"])
        user= cursor.fetchall()
        if len(user)==1 and course_id!=None: 
            cursor.execute("DELETE FROM student_register WHERE student_id=? AND course_id=?",[user[0][0],course_id,])
            conn.commit()
            rows=cursor.rowcount
        else:
            message="invalid entry"
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data"
    except:
        message =  "somthing went wrong" 
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows == 1 :
            return Response("success",mimetype="html/text" , status =204)
        else:
            return Response(message,mimetype="text/html",status=400)
