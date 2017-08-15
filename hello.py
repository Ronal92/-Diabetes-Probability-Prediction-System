# -*- coding: utf-8 -*- 

from flask import Flask, render_template, request, redirect, flash, url_for, session
# from flaskext.mysql import MySQL
import csv, math
import json

diabeteList1 = list()
diabeteList2 = list()
hyperList1 = list()
hyperList2 = list()
calWeightList = list()

isManager =''

column = ['체질량지수', '수축기혈압', '이완기혈압', '식전혈당', '총콜레스테롤' , '혈색소', \
			'AST', 'ALT', '감마지티피', '과거병력코드1 ', '과거병력코드2', '과거병력코드3', \
			'간장질환유무 ', '고혈압유무 ', '뇌졸중유무', '심장병유무', '당뇨병유무', '암유무', '흡연상태', '흡연기간', '하루흡연량', \
			'음주습관', '1회 음주량 ', '1주 운동횟수 ' ]

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

	print(len(calWeightList))

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

	del calWeightList[:]
	print(" d1 = "+str(diab1_result)+" d2 = "+str(diab2_result)+" h1 = "+str(hyper1_result)+" h1 = "+str(hyper2_result))
	del calWeightList[:]
	return [hyper1_result,hyper2_result,diab1_result,diab2_result]
	


def insertLineIntoList(list, line):
	for column in line :
		if column :
			list.append(float(column))

def readCSVweight():
	f= open('calculateWeight.csv', 'r')
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

def	getIndexOfList(key):
	for i in column :
		if i == key:
			return i

def updateWeightList(key, value):
	#TODO : Key값을 column에서 비교하여 순서대로 List를 업뎃한다.
	idx = getIndexOfList(key)


	pass



def	changeCSV():
	#TOdo : 모두 바껴진 값을 csv에 다 떄려박는다
	pass

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
	errors = ''
	return render_template('measure.html', errors = errors)

# 계산 결과 
@app.route("/measure/result", methods=['POST'])
def measureDiabetsResult():

	famLIVER 		= request.form.get('famLIVER', '')
	famHPRTS 		= request.form.get('famHPRTS', '')
	famAPOP 		= request.form.get('famAPOP', '')
	famHDISE 		= request.form.get('famHDISE', '')
	famDIABML 		= request.form.get('famDIABML', '')
	famCANCER 		= request.form.get('famCANCER', '')

	# validation check (유효성 검사)

	# if not famLIVER or not famHPRTS or not famAPOP \
	# 	or not famHDISE or not famDIABML or not famCANCER \
	# 	or not [v for v in request.form.getlist('attributes[]')] :

	# 	errors = "Please enter all the fields."

	# 	return render_template('measure.html', errors = errors)

	return render_template('result.html') # 임시로 최종 결과를 메인페이지 볼수 있게 처리함.


	# # sorting 문제 때문에 그냥 하드코딩스럽게 박아두겠습니다.

	# calWeightList.append(int(request.form['height']))
	# calWeightList.append(int(request.form['weight']))
	# calWeightList.append(int(request.form['waist']))
	# calWeightList.append(int(request.form['age']))
	# calWeightList.append(stringToValue(request.form['pastHB']))
	# calWeightList.append(stringToValue(request.form['pastDB']))
	# calWeightList.append(stringToValue(request.form['famHB']))
	# calWeightList.append(stringToValue(request.form['famDB']))
	# calWeightList.append(int(request.form['smoke']))
	# calWeightList.append(int(request.form['drink']))
	# calWeightList.append(int(request.form['exercise']))
	# calWeightList.append(float(request.form['hdp']))
	# calWeightList.append(float(request.form['ldp']))
	# calWeightList.append(float(request.form['bc']))
	# calWeightList.append(float(request.form['bs']))
	# calWeightList.append(float(request.form['col']))
	# calWeightList.append(float(request.form['tg']))
	# calWeightList.append(float(request.form['hdl']))
	# calWeightList.append(float(request.form['ldl']))
	# calWeightList.append(float(request.form['creatine']))
	# calWeightList.append(float(request.form['got']))
	# calWeightList.append(float(request.form['gpt']))
	# calWeightList.append(float(request.form['ggt']))

	# resultList = list()
	# resultList = calculateResult()

	# # hyper1_result,hyper2_result,diab1_result,diab2_result
	
	# print(resultList)

	# return render_template('result.html', resultList=resultList) #, result = calculateResult() )

# 계산 모델
@app.route("/setting")
def valueSet():

	return render_template('setting.html', column=column, diabeteList1=diabeteList1, diabeteList2=diabeteList2, hyperList1=hyperList1, hyperList2=hyperList2)

	
# 수정완료
@app.route("/setting/changed" , methods=['POST','GET'])
def	changeWeightFactor():	

	for key in request.form.keys() :
		for v in request.form.getlist(key) :
			if not v :
				errors = "Please enter all the fields."
				return render_template('setting.html', errors = errors, column=column, diabeteList1=diabeteList1, diabeteList2=diabeteList2, hyperList1=hyperList1, hyperList2=hyperList2)
		print(key,v)

	# 브라우저에서 변경된 값을 불러올 때, 아래처럼 가져오면 됩니다. 
	# for v in request.form.getlist('changedDL1[]'):

	# for v in request.form.getlist('changedDL2[]'):

	# for v in request.form.getlist('changedHL1[]'):

	# for v in request.form.getlist('changedHL2[]'):



	return render_template('changed.html', msg = "Be saved completely", column=column, diabeteList1=diabeteList1, diabeteList2=diabeteList2, hyperList1=hyperList1, hyperList2=hyperList2)

# CSV 업로드하기
@app.route("/upload")
def uploadBefore():
	return render_template('uploadCSV.html')

# 업로드된 파일 처리하기
@app.route("/upload/result", methods=['POST'])
def saveUploadedFile():
	return redirect(url_for('showMainPage'))




if __name__=="__main__":
	app.run(debug=True, host = '127.0.0.1', port= 5000)
	#app.run(host='163.152.184.176', port= 5000, debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

