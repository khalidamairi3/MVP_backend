import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def post():
    data=request.json
    email = data.get("email")
    password=data.get("password")
    conn = None
    cursor = None
    user = None
    rows=None
    if email!="" and email !=None and password !="" and password != None:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? and password =?",[email,password])
            user= cursor.fetchall()
            if len(user)==1 :
                loginToken = secrets.token_urlsafe(16) 
                cursor.execute("INSERT INTO user_session (user_id, token) VALUES (?,?)",[user[0][0],loginToken,])
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
                return Response(message,mimetype="text/html",status=400)
    else:
        return Response("wrong entry",mimetype="text/html",status=400)
            


def delete():
    data =request.json
    loginToken = data.get("loginToken")
    rows=None
    if loginToken!="" and loginToken !=None:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_session WHERE token = ?",[loginToken,])
            conn.commit()
            rows=cursor.rowcount
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data"
        except:
            message =  "somthing went wrong"
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows==1:
            return  Response("Success",mimetype="text/html",status=204)
    return  Response("failed",mimetype="text/html",status=400)
