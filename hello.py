# -*- coding: utf-8 -*- 

from flask import Flask, render_template, request, redirect, flash, url_for, session
# from flaskext.mysql import MySQL
import csv, math
import json

'''
global diabeteList1
global diabeteList2
global hyperList1
global hyperList2
'''

diabeteList1 = []
diabeteList2 = []
hyperList1 = []
hyperList2 = []
calWeightList = []

isManager =''


app = Flask(__name__)
app.secret_key = 'secret'


# mysql = MySQL()

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
# app.config['MYSQL_DATABASE_DB'] = 'test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)


def calculateResult():
	i =0
	diab1 =0.0
	diab2 =0.0
	hyper1 =0.0
	hyper2 =0.0

	for i in range(len(calWeightList)):
		if i ==0:
			diab1 += calWeightList[i]
			diab2 += calWeightList[i]
			hyper1 += calWeightList[i]
			hyper2 += calWeightList[i]
		else:
			diab1 += calWeightList[i] * diabeteList1[i-1]
			diab2 += calWeightList[i] * diabeteList2[i-1]
			hyper1 += calWeightList[i] * hyperList1[i-1]
			hyper2 += calWeightList[i] * hyperList2[i-1]
		i=+1

	diab1_result = round( 1 / (math.exp(-1*diab1)+1) , 6)
	diab2_result = round( 1 / (math.exp(-1*diab2)+1) , 6)
	hyper1_result = round( 1 / (math.exp(-1*hyper1)+1) , 6)
	hyper2_result = round( 1 / (math.exp(-1*hyper2)+1) , 6)

	print(" d1 = "+str(diab1_result)+" d2 = "+str(diab2_result)+" h1 = "+str(hyper1_result)+" h1 = "+str(hyper2_result))
	return [hyper1_result,hyper2_result,diab1_result,diab2_result]

def insertLineIntoList(list, line):
	for column in line :
		if column :
			list.append(float(column))

def readCSVweight():
	f= open('calculateWeight.csv', 'r')
	print('file opened')
	csvReader = csv.reader(f)
	lineNum=0

	for line in csvReader:
		lineNum +=1

		if lineNum == 3:
			insertLineIntoList(diabeteList1, line[1:])
		elif lineNum == 4:
			 insertLineIntoList(diabeteList2, line[1:])
		elif lineNum == 5:
			insertLineIntoList(hyperList1, line[1:])
		elif lineNum ==6:
			insertLineIntoList(hyperList2, line[1:])

	#print(len(diabeteList1))
	#print(diabeteList2)
	#print(len(hyperList1))
	#print(hyperList2)
	f.close()
	print("file closed")


def stringToValue(str):
	if str == 'yes':
		return 1
	elif str == 'no':
		return 0

readCSVweight() # Read csv before app start

#로그인 화면
@app.route("/")
def showLoginPage():
	return render_template("login.html")

#로그인 화면 처리
@app.route("/", methods=['POST'])
def processLogin():

	global isManager

	name=request.form['id']

	# con=mysql.connect()
	# cursor =con.cursor()

	# ## 검색
	# cursor.execute("SELECT * FROM my_user WHERE name='"+request.form['id']+"' AND pwd='"+request.form['pwd']+"';")
	# data = cursor.fetchone()
	# if data is None:
	# 	return redirect('/')
		
	# else:

		# if data[3] == 'manager' : ## 관리자인지 구분한다 ##
	if name == 'koreauniv' :
		isManager = 'true'
		flash('관리자')
	else :
		isManager = 'false'

	return render_template("main.html", cur_name = name);



# 메인 화면
@app.route("/main")
def showMainPage():
	global isManager
	if isManager == 'true' :
		flash('관리자')

	return render_template("main.html")

''' # TODO : 로긴처리
def tryLogin():
	if request.method == 'POST':
		if(request.form['user'] == 'ku'
		   and request.form['password'] == '1234'):
			session['login']=True
			session['username']= request.form['user']
		else:
			return  'invalid LOGIN'
t	return render_template("hello.html", cur_name = request.args.get('cur_name'))
'''


# 사용자 등록 페이지
@app.route("/signUp", methods=['GET'])
def showSignUp():
	return render_template('signup.html')



# 사용자 등록 요청
@app.route("/signUps", methods=['POST'])
def saveSignUp():
	name=request.form['inputID']
	pwd=request.form['inputPWD']

	# con=mysql.connect()
	# cursor =con.cursor()

	# ## 검색
	# cursor.execute("SELECT * FROM my_user WHERE name='"+name+"' AND pwd='"+pwd+"';")
	# data = cursor.fetchone()
	# if data is None:
	# 	query="INSERT INTO my_user(name, pwd) VALUES ('" + name +"','" + pwd +"');"
	# 	cursor.execute(query)
	# 	con.commit()
	# 	return redirect(url_for('showMainPage'))

		
	# else:
	# 	print ('이미 존재')
	# 	return render_template("signup.html", isUser='true')

	return redirect(url_for('showMainPage'))

# 계산 실행 
@app.route("/measure", methods=['GET'])
def measureDiabets():
	return render_template('measure.html')

# 계산 결과 
@app.route("/measure/result", methods=['POST'])
def measureDiabetsResult():
	# sorting 문제 때문에 그냥 하드코딩스럽게 박아두겠습니다.
	calWeightList.append(int(request.form['height']))
	calWeightList.append(int(request.form['weight']))
	calWeightList.append(int(request.form['waist']))
	calWeightList.append(int(request.form['age']))
	calWeightList.append(stringToValue(request.form['pastHB']))
	calWeightList.append(stringToValue(request.form['pastDB']))
	calWeightList.append(stringToValue(request.form['famHB']))
	calWeightList.append(stringToValue(request.form['famDB']))
	calWeightList.append(int(request.form['smoke']))
	calWeightList.append(int(request.form['drink']))
	calWeightList.append(int(request.form['exercise']))
	calWeightList.append(float(request.form['hdp']))
	calWeightList.append(float(request.form['ldp']))
	calWeightList.append(float(request.form['bc']))
	calWeightList.append(float(request.form['bs']))
	calWeightList.append(float(request.form['col']))
	calWeightList.append(float(request.form['tg']))
	calWeightList.append(float(request.form['hdl']))
	calWeightList.append(float(request.form['ldl']))
	calWeightList.append(float(request.form['creatine']))
	calWeightList.append(float(request.form['got']))
	calWeightList.append(float(request.form['gpt']))
	calWeightList.append(float(request.form['ggt']))

	print(calWeightList)
	calculateResult()
	return render_template('result.html') #, result = calculateResult() )

# 계산 모델
@app.route("/setting")
def valueSet():
	return render_template('setting.html')


if __name__=="__main__":
	app.run(debug=True, host = '127.0.0.1', port= 5000)
	# app.run(host='163.152.184.176', debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

