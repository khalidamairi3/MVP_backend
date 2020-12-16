import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def post():
    data=request.json
    loginToken = data.get("loginToken")
    course_id=data.get("courseId")
    instructor_id = data.get("instructorId")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u ON u.id=us.user_id WHERE us.token = ? AND u.role = ?",[loginToken,"admin"])
        user= cursor.fetchall()
        if len(user)==1 and course_id!=None and instructor_id !=None: 
            cursor.execute("INSERT INTO instructor_teaches (instructor_id, course_id) VALUES (?,?)",[instructor_id,course_id,])
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
            return Response("failed",mimetype="text/html",status=400)
  
            


def delete():
    data=request.json
    loginToken = data.get("loginToken")
    course_id=data.get("courseId")
    instructor_id = data.get("instructorId")
    conn = None
    cursor = None
    user = None
    rows=None
    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id FROM user_session us INNER JOIN users u ON u.id=us.user_id WHERE us.token = ? AND u.role = ?",[loginToken,"admin"])
        user= cursor.fetchall()
        if len(user)==1 and course_id!=None: 
            cursor.execute("DELETE FROM instructor_teaches WHERE instructor_id=? AND course_id=?",[instructor_id ,course_id,])
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
            return Response("failed",mimetype="text/html",status=400)
