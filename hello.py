# -*- coding: utf-8 -*- 


from flask import Flask, render_template, request, redirect, flash, url_for, session
# from flaskext.mysql import MySQL
import csv
import json

diabeteList1 = []
diabeteList2 = []
hyperList1 = []
hyperList2 = []

app = Flask(__name__)
app.secret_key = 'secret'



# mysql = MySQL()
# '''
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
# app.config['MYSQL_DATABASE_DB'] = 'test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
# '''

def calculateResult(*args):
	#TODO 해당값들을 받아서 index순서대로 list와 곱해서 4개의 값을 리스트 등으로 전달한다.
	pass


def readCSVweight():
	f= open('calculateWeight.csv', 'r')
	csvReader = csv.reader(f)
	lineNum=0

	for line in csvReader:
		lineNum +=1

		if lineNum == 3:
			diabeteList1 = line[1:]
		elif lineNum == 4:
			diabeteList2 = line[1:]
		elif lineNum == 5:
			hyperList1 = line[1:]
		elif lineNum ==6:
			hyperList2 = line[1:]

	#print(diabeteList1)
	#print(diabeteList2)
	#print(hyperList1)
	#print(hyperList2)
	f.close()
	#print("file closed")

readCSVweight() # Read csv before app start

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

	# con=mysql.connect()
	# cursor =con.cursor()

	# ## 검색
	# cursor.execute("SELECT * FROM my_user WHERE name='"+name+"' AND email='"+email+"';")
	# data = cursor.fetchone()
	# if data is None:
	# 	query="INSERT INTO my_user(name, email) VALUES ('" + name +"','" + email +"');"
	# 	cursor.execute(query)
	# 	con.commit()
	# 	flash('사용자가 등록되었습니다.')
		
	# else:
	# 	flash('같은 사용자가 존재합니다.')

	return redirect(url_for('showMainPage',cur_name=name))

# 계산 실행 
@app.route("/measure", methods=['GET'])
def measureDiabets():
	return render_template('measure.html')

# 계산 결과 
@app.route("/measure/result", methods=['GET', 'POST'])
def measureDiabetsResult():

	# TODO 값을 어떻게 받을지 고민..
	#request.form[]

	return render_template('result.html')


if __name__=="__main__":
	app.run(debug=True, host = '127.0.0.1', port= 5000)
	# app.run(host='163.152.184.176', debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

