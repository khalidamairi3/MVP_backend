import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb
from datetime import date

def get():
    params=request.args
    course_id = params.get("courseId")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if course_id !=None and course_id !="":
            cursor.execute("SELECT * FROM tasks WHERE course_id=?",[course_id,])
            rows = cursor.fetchall()
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
        if (rows !=None or rows == []):
            tasks=[]
            for row in rows:

                task={
                    "id":row[0],
                    "courseId":row[1],
                    "type":row[2],
                    "published_date":row[3],
                    "due_date": row[4],
                    "description":row[5],
                    "title":row[6]
                }
                tasks.append(task)
            return Response(json.dumps(tasks,default=str) ,mimetype="application/json",status=201)
        else:
            return Response("failed" ,mimetype="html/text",status=400)

def post():
    data=request.json
    loginToken = data.get("loginToken")
    course_id = data.get("courseId")
    task_type = data.get("type")
    due_date = data.get("due-date")
    description = data.get("description")
    title = data.get("title")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        if course_id !=None and course_id !="":
            cursor.execute("SELECT * FROM users u INNER JOIN instructor_teaches it ON u.id=it.instructor_id WHERE u.id =? AND u.role = ? AND it.course_id=?",[user_id,"instructor",course_id])
            user = cursor.fetchall()
        if len(user)==1:
            if course_id !=None and course_id !="" and task_type != None and task_type !="" and due_date!=None and due_date !="" and description != None and description != "" and title !=None and title !="": 
                cursor.execute("INSERT INTO tasks (course_id,task_type,due_date,description,title) VALUES (?,?,?,?,?) ",[course_id,task_type,due_date,description,title])
                conn.commit()
                task_id = cursor.lastrowid
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
            pub_date = date.today()
            task={
                "id":task_id,
                "courseId":course_id,
                "type":task_type,
                "published_date":pub_date,
                "due_date": due_date,
                "description":description,
                "title":title
            }
            return Response(json.dumps(task,default=str) ,mimetype="application/json",status=201)
        else:
            return Response("failed" ,mimetype="html/text",status=400)

def update():
    data=request.json
    loginToken = data.get("loginToken")
    task_id = data.get("taskId")
    task_type = data.get("type")
    due_date = data.get("due-date")
    description = data.get("description")
    title = data.get("title")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        if task_id !=None and task_id !="":
            cursor.execute("SELECT * FROM users u INNER JOIN instructor_teaches it INNER JOIN tasks t ON u.id=it.instructor_id AND it.course_id=t.course_id WHERE u.id =? AND u.role = ? AND t.id =?",[user_id,"instructor",task_id])
            user = cursor.fetchall()
        if len(user)==1:
            if task_type != None and task_type !="":
                cursor.execute("UPDATE tasks SET task_type=? WHERE id=?",[task_type,task_id])
            if due_date!=None and due_date !="":
                cursor.execute("UPDATE tasks SET due_date=? WHERE id=? ",[due_date,task_id])
            if description != None and description != "": 
                cursor.execute("UPDATE tasks SET description=? WHERE id=?",[description,task_id])
            if title != None and title != "": 
                cursor.execute("UPDATE tasks SET title=? WHERE id=?",[title,task_id])
            conn.commit()
            rows=cursor.rowcount
            cursor.execute("SELECT * FROM tasks WHERE id=?",[task_id,])
            row=cursor.fetchone()
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
            task={
                "id":task_id,
                "courseId":row[1],
                "type":row[2],
                "published_date":row[3],
                "due_date": row[4],
                "description":row[5]
            }
            return Response(json.dumps(task,default=str) ,mimetype="application/json",status=201)
        else:
            return Response("failed" ,mimetype="html/text",status=400)

def delete():
    data=request.json
    loginToken = data.get("loginToken")
    task_id = data.get("taskId")
    conn = None
    cursor = None
    rows = None    
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_session WHERE token = ?",[loginToken])
        user_id = cursor.fetchone()[0]
        if task_id !=None and task_id !="":
            cursor.execute("SELECT * FROM users u INNER JOIN instructor_teaches it INNER JOIN tasks t ON u.id=it.instructor_id AND it.course_id=t.course_id WHERE u.id =? AND u.role = ? AND t.id =?",[user_id,"instructor",task_id])
            user = cursor.fetchall()
        if len(user)==1:
            cursor.execute("DELETE FROM tasks WHERE id=?",[task_id])
            conn.commit()
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
            
            return Response("Success",mimetype="html/text",status=204)
        else:
            return Response("failed" ,mimetype="html/text",status=400)


    
