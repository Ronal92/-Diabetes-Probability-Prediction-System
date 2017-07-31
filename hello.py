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

	height 		= request.form['height'].strip()
	weight 		= request.form['weight'].strip()
	waist 		= request.form['waist'].strip()
	age 		= request.form['age'].strip()
	pastHB 		= request.form.get('pastHB', '')
	pastDB 		= request.form.get('pastDB', '')
	famHB 		= request.form.get('famHB', '')
	famDB 		= request.form.get('famDB', '')
	smoke 		= request.form['smoke'].strip()
	drink 		= request.form['drink'].strip()
	exercise 	= request.form['exercise'].strip()
	hdp 		= request.form['hdp'].strip()
	ldp 		= request.form['ldp'].strip()
	bc			= request.form['bc'].strip()
	bs 			= request.form['bs'].strip()
	col 		= request.form['col'].strip()
	tg 			= request.form['tg'].strip()
	hdl 		= request.form['hdl'].strip()
	ldl 		= request.form['ldl'].strip()
	creatine 	= request.form['creatine'].strip()
	got 		= request.form['got'].strip()
	gpt 		= request.form['gpt'].strip()
	ggt 		= request.form['ggt'].strip()

	# validation check (유효성 검사)
	if not height or not weight or not waist \
		or not age or not pastHB or not pastDB \
		or not famHB or not famDB or not smoke \
		or not drink or not exercise or not hdp \
		or not ldp or not bc or not bs or not col \
		or not tg or not hdl or not ldl or not creatine \
		or not got or not gpt or not ggt :

		errors = "Please enter all the fields."

		return render_template('measure.html', errors = errors)

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

	resultList = list()
	resultList = calculateResult()

	# hyper1_result,hyper2_result,diab1_result,diab2_result
	
	print(resultList)

	return render_template('result.html', resultList=resultList) #, result = calculateResult() )

# 계산 모델
@app.route("/setting")
def valueSet():
	return render_template('setting.html',
						   intercept_d1=diabeteList1[0],intercept_d2=diabeteList2[0],intercept_h1=hyperList1[0],intercept_h2=hyperList2[0],
						   height_d1 = diabeteList1[1], height_d2 = diabeteList2[1],height_h1 = hyperList1[1],height_h2 = hyperList2[1],
						   weight_d1 = diabeteList1[2], weight_d2 = diabeteList2[2],weight_h1 = hyperList1[2],weight_h2 = hyperList2[2],
						   waist_d1 = diabeteList1[3], waist_d2 = diabeteList2[3], waist_h1 = hyperList1[3], waist_h2 = hyperList2[3],
						   age_d1 = diabeteList1[4], age_d2 = diabeteList2[4], age_h1 = hyperList1[4], age_h2 = hyperList2[4],
						   pastHB_d1 = diabeteList1[5], pastHB_d2 = diabeteList2[5], pastHB_h1 = hyperList1[5], pastHB_h2 = hyperList2[5],
						   pastDB_d1 = diabeteList1[6], pastDB_d2 = diabeteList2[6], pastDB_h1 = hyperList1[6], pastDB_h2 = hyperList2[6],
						   famHB_d1 = diabeteList1[7], famHB_d2 = diabeteList2[7], famHB_h1 = hyperList1[7], famHB_h2 = hyperList2[7],
						   famDB_d1 = diabeteList1[8], famDB_d2 = diabeteList2[8], famDB_h1 = hyperList1[8], famDB_h2 = hyperList2[8],
						   smoke_d1 = diabeteList1[9], smoke_d2 = diabeteList2[9], smoke_h1 = hyperList1[9], smoke_h2 = hyperList2[9],
						   drink_d1 = diabeteList1[10], drink_d2 = diabeteList2[10], drink_h1 = hyperList1[10], drink_h2 = hyperList2[10],
						   exercise_d1 = diabeteList1[11], exercise_d2 = diabeteList2[11], exercise_h1 = hyperList1[11], exercise_h2 = hyperList2[11],
						   hdp_d1 = diabeteList1[12], hdp_d2 = diabeteList2[12], hdp_h1 = hyperList1[12], hdp_h2 = hyperList2[12],
						   ldp_d1 = diabeteList1[13], ldp_d2 = diabeteList2[13], ldp_h1 = hyperList1[13], ldp_h2 = hyperList2[13],
						   bc_d1  = diabeteList1[14], bc_d2  = diabeteList2[14], bc_h1  = hyperList1[14], bc_h2  = hyperList2[14],
						   bs_d1  = diabeteList1[15], bs_d2  = diabeteList2[15], bs_h1  = hyperList1[15], bs_h2  = hyperList2[15],
						   col_d1 = diabeteList1[16], col_d2 = diabeteList2[16], col_h1 = hyperList1[16], col_h2 = hyperList2[16],
						   tg_d1  = diabeteList1[17], tg_d2  = diabeteList2[17], tg_h1  = hyperList1[17], tg_h2  = hyperList2[17],
						   hdl_d1 = diabeteList1[18], hdl_d2 = diabeteList2[18], hdl_h1 = hyperList1[18], hdl_h2 = hyperList2[18],
						   ldl_d1 = diabeteList1[19], ldl_d2 = diabeteList2[19], ldl_h1 = hyperList1[19], ldl_h2 = hyperList2[19],
						   creatine_d1 = diabeteList1[20], creatine_d2 = diabeteList2[20], creatine_h1 = hyperList1[20], creatine_h2 = hyperList2[20],
						   got_d1 = diabeteList1[21], got_d2 = diabeteList2[21], got_h1 = hyperList1[21], got_h2 = hyperList2[21],
						   gpt_d1 = diabeteList1[22], gpt_d2 = diabeteList2[22], gpt_h1 = hyperList1[22], gpt_h2 = hyperList2[22],
						   ggt_d1 = diabeteList1[23], ggt_d2 = diabeteList2[23], ggt_h1 = hyperList1[23], ggt_h2 = hyperList2[23])

# 수정완료
@app.route("/chagned" , methods=['POST','GET'])
def	changeWeightFactor():
	


	return render_template('changed.html')



if __name__=="__main__":
	app.run(debug=True, host = '127.0.0.1', port= 5000)
	#app.run(host='163.152.184.176', port= 5000, debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

