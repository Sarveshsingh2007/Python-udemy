from flask import Flask
import random

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, user"

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello my friend {name}, you are {number} years old."

@app.route("/<student_name>/<college_name>/<course_name>/<sec_name>/<int:roll_no>")
def course_details(student_name, college_name, course_name, sec_name, roll_no):
    return f"""
                Hello {student_name}, your college name is 
                <span style='color:blue; font-weight:bold;'>{college_name}</span> 
                and you are pursuing a degree in {course_name} 
                (Section {sec_name}) with roll number {roll_no}.<br>
                <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXBzYm4yYmNrNnh1dDBnbnJmZnFoNW5nanhzc2U1c2o4cWc1aDRxcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SUshjgObk2YoiSQl6H/giphy.gif">
    """

if __name__ == "__main__":
    app.run(debug=True)
