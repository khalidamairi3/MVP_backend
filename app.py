from flask import Flask,request
import dbcreds
import mariadb
import students
import instructors
import users
import courses
import login
import student_registers


from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/api/login",methods=["POST","DELETE"])
def login_api():

    if request.method=="POST":
        return login.post()
    elif request.method == "DELETE":
        return login.delete()

@app.route("/api/students",methods=["GET"])
def students_api():
    if request.method=="GET":
        return students.get()
@app.route("/api/instructors",methods=["GET"])
def instructors_api():
    if request.method=="GET":
        return instructors.get()

@app.route("/api/users",methods=["POST","PATCH","DELETE"])
def users_api():
    if request.method=="POST":
        return users.post()
    elif request.method=="PATCH":
        return users.update()
    elif request.method == "DELETE":
        return users.delete()

@app.route("/api/courses",methods=["GET","POST","PATCH","DELETE"])
def courses_api():
    if request.method == "GET":
        return courses.get()
    elif request.method=="POST":
        return courses.post()
    elif request.method=="PATCH":
        return courses.update()
    elif request.method == "DELETE":
        return courses.delete()

@app.route("/api/student-registers",methods=["POST","DELETE"])
def student_registers_api():

    if request.method=="POST":
        return student_registers.post()
    elif request.method == "DELETE":
        return student_registers.delete()






