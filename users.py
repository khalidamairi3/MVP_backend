import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb

def get():
    loginToken = request.headers.get("loginToken")
    conn = None
    cursor = None
    user = None
    if loginToken != None and loginToken !="":
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users u INNER JOIN user_session us on u.id = us.user_id WHERE token = ?",[loginToken,])
            user= cursor.fetchall()
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
            if user != None :
                res = {
                   "id":user[0][0],
                    "name":user[0][1],
                    "username":user[0][4],
                    "email":user[0][5],
                    "birthdate":user[0][2],
                    "role":user[0][6],
                    "loginToken": loginToken 
                }
                return Response(json.dumps(res,default=str),mimetype="application/json" , status =201)
            else:
                return Response("failed",mimetype="text/html",status=400)



def post():
    data = request.json
    loginToken = data.get("loginToken")
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
        cursor.execute("SELECT u.id, u.role FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE token =? AND u.role=?",[loginToken,"admin"])
        admin = cursor.fetchall()
        if len(admin)==1 and name != None and name!="" and birthdate!=None and birthdate!="" and password!=None and password!="" and username!=None and username!="" and email != None and email !="" and role !="" and role !=None :
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
    user_id = data.get("userId")
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
        cursor.execute("SELECT u.id, u.role FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE us.token =? AND u.role=?",[loginToken,"admin"])
        admin = cursor.fetchall()
        if len(admin) ==1 and name != None and name!="" and user_id != None:
            cursor.execute("UPDATE users SET name =? WHERE id =?",[name,user_id])
        if len(admin) ==1 and birthdate != None and birthdate!="" and user_id != None:
            cursor.execute("UPDATE users SET birthdate =? WHERE id =?",[birthdate,user_id])
        if len(admin) ==1 and password != None and password!="" and user_id != None:
            cursor.execute("UPDATE users SET password =? WHERE id =?",[password,user_id])
        if len(admin) ==1 and username != None and username!="" and user_id != None:
            cursor.execute("UPDATE users SET username =? WHERE id =?",[username,user_id])
        if len(admin) ==1 and email != None and email!="" and user_id != None:
            cursor.execute("UPDATE users SET email =? WHERE id =?",[email,user_id])           
        conn.commit()
        rows = cursor.rowcount
        cursor.execute("SELECT * FROM users WHERE id = ? ",[user_id])
        user= cursor.fetchone()
        print(rows)
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
    user_id = data.get("userId")
    conn = None
    cursor = None
    rows=None
    
    

    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT u.id, u.role FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE us.token =? AND u.role=?",[loginToken,"admin"])
        admin = cursor.fetchall()
        if len(admin)==1 and user_id!=None:
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