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
            cursor.execute("SELECT * FROM users u INNER JOIN student_register sr INNER JOIN courses c ON sr.student_id = u.id AND sr.course_id = c.id  WHERE u.role= ? AND c.id =?",["student",course_id])
        else:
            cursor.execute("SELECT * FROM users WHERE role = ?",["student",])
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
            students=[]
            for row in result:
                student={
                    "id":row[0],
                    "name":row[1],
                    "username":row[4],
                    "email":row[5],
                    "birthdate":row[2],
                    "role":row[6]
                }
                students.append(student)
            return Response(json.dumps(students,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)



            