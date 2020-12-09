import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def post():
    data = request.json
    name = data.get("name")
    birthdate= data.get("birthdate")
    password=data.get("password")
    username = data.get("username")
    email =data.get("email")
    role = data.get("role")
    conn = None
    cursor = None
    user_id=None
    
        
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if name != None and name!="" and birthdate!=None and birthdate!="" and password!=None and password!="" and username!=None and username!="" and email != None and email !="" and role !="" and role !=None :
            cursor.execute("INSERT INTO users (name, birthdate,password,username,email,role) VALUES (?,?,?,?,?,?)",[name,birthdate,password,username,email,role])
            conn.commit()
            user_id = cursor.lastrowid
     
    except mariadb.OperationalError as e:
        message = "connection error" 
        print(e)
    except Exception as e:
        message ="somthing went wrong, probably bad params " 
        print(e)
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (user_id != None ):
            
            user={
                    "id":user_id,
                    "name":name,
                    "username":username,
                    "email":email,
                    "birthdate":birthdate,
                    "role":role
                }
        
            return Response(json.dumps(user,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)

def update():
    data = request.json
    name = data.get("name")
    birthdate= data.get("birthdate")
    password=data.get("password")
    username = data.get("username")
    email =data.get("email")
    role = data.get("role")
    loginToken=data.get("loginToken")
    conn = None
    cursor = None
    rows=None
    user = None
        
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session WHERE token = ?",[loginToken])
        user_id = cursor.fecthone()[0]
        if name != None and name!="" and user_id != None:
            cursor.execute("UPDATE users SET name =? WHERE id =?",[name,user_id])
        if birthdate != None and birthdate!="" and user_id != None:
            cursor.execute("UPDATE users SET birthdate =? WHERE id =?",[birthdate,user_id])
        if password != None and password!="" and user_id != None:
            cursor.execute("UPDATE users SET password =? WHERE id =?",[password,user_id])
        if username != None and username!="" and user_id != None:
            cursor.execute("UPDATE users SET username =? WHERE id =?",[username,user_id])
        if email != None and email!="" and user_id != None:
            cursor.execute("UPDATE users SET email =? WHERE id =?",[email,user_id])
        if role != None and role!="" and user_id != None:
            cursor.execute("UPDATE users SET role =? WHERE id =?",[role,user_id]) 
            
        conn.commit()
        rows = cursor.rowcount
        cursor.execute("SELECT * FROM users WHERE id = ? ",[user_id])
        user= cursor.fetchone()
     
    except mariadb.OperationalError as e:
        message = "connection error" 
        print(e)
    except Exception as e:
        message ="somthing went wrong, probably bad params " 
        print(e)
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (rows== 1 ):
            
            user_updated={
                    "id":user[0],
                    "name":user[1],
                    "username":user[4],
                    "email":user[5],
                    "birthdate":user[2],
                    "role":user[3]
                }
        
            return Response(json.dumps(user_updated,default=str) ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)


def delete():
    data = request.json
    loginToken = data.get("loginToken")
    conn = None
    cursor = None
    rows=None
    
    

    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session WHERE token = ?",[loginToken])
        user_id = cursor.fecthone()[0]
        cursor.execute("DELETE FROM users WHERE id=?",[user_id])
        conn.commit()
        rows = cursor.rowcount
     
    except mariadb.OperationalError as e:
        message = "connection error" 
        print(e)
    except Exception as e:
        message ="somthing went wrong, probably bad params " 
        print(e)
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if (rows == 1 ):
    
            return Response("deleted success" ,mimetype="application/json",status=200)
        else:
            return Response("failed" ,mimetype="html/text",status=400)