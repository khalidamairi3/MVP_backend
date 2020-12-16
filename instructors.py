import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb

def get():
    result = None
    params = request.args
    user_id = params.get("userId")
    course_id = params.get("courseId")
    conn = None
    cursor = None
    result = None
        
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if course_id != None:
            cursor.execute("SELECT * FROM users u INNER JOIN instructor_teaches it INNER JOIN courses c ON it.instructor_id = u.id AND it.course_id = c.id  WHERE u.role= ? AND c.id =?",["instructor",course_id])
        else:
            cursor.execute("SELECT * FROM users WHERE role = ?",["instructor",])
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
            instructors=[]
            for row in result:
                instructor={
                    "id":row[0],
                    "name":row[1],
                    "username":row[4],
                    "email":row[5],
                    "birthdate":row[2],
                    "role":row[6]
                }
                instructors.append(instructor)
            return Response(json.dumps(instructors,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)



            