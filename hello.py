from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


# 메이 화면
@app.route("/")
def hello(name=None):
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * FROM my_user")
	result = []

	for row in cursor:
		result.append(row)

	print (result)

	return render_template("hello.html")

# 사용자 등록 페이지
@app.route("/signUp", methods=['GET'])
def showSignUp():
		return render_template('signup.html')



# 사용자 등록 요청
@app.route("/signUps", methods=['POST'])
def saveSignUp():
	name=request.form['inputName']
	email=request.form['inputEmail']

	con=mysql.connect()
	cursor =con.cursor()
	query="INSERT INTO my_user(name, email) VALUES ('" + name +"','" + email +"');"
	print(query)
	cursor.execute(query)
	con.commit()

	return redirect("/")

if __name__=="__main__":
	app.run(debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

