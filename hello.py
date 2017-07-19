from flask import Flask, render_template, request, redirect, flash, url_for, session
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
app.secret_key = 'secret'

mysql = MySQL()
'''
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
'''

#로그인 화면
@app.route("/")
def showLoginPage():
	return render_template("login.html")

# 메인 화면
@app.route("/main")
def showMainPage():
	return render_template("hello.html", cur_name = request.args.get('cur_name'))

''' # TODO : 로긴처리
def tryLogin():
	if request.method == 'POST':
		if(request.form['user'] == 'ku'
		   and request.form['password'] == '1234'):
			session['login']=True
			session['username']= request.form['user']
		else:
			return  'invalid LOGIN'
	return render_template("hello.html", cur_name = request.args.get('cur_name'))
'''


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

	## 검색
	cursor.execute("SELECT * FROM my_user WHERE name='"+name+"' AND email='"+email+"';")
	data = cursor.fetchone()
	if data is None:
		query="INSERT INTO my_user(name, email) VALUES ('" + name +"','" + email +"');"
		cursor.execute(query)
		con.commit()
		flash('사용자가 등록되었습니다.')
		
	else:
		flash('같은 사용자가 존재합니다.')

	return redirect(url_for('hello',cur_name=name))

# 계산 실행 
@app.route("/measure", methods=['GET'])
def measureDiabets():
	return render_template('measure.html')

# 계산 결과 
@app.route("/measure/result", methods=['GET'])
def measureDiabetsResult():
	return render_template('result.html')


if __name__=="__main__":
	app.run(debug=True, host = '127.0.0.1', port= 5000)
	# app.run(host='163.152.184.176', debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

