# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, flash, url_for, session
# from flaskext.mysql import MySQL
import csv, math, io, pandas

import json
#from werkzeug.utils import secure_filename

diabeteList1 = list()
diabeteList2 = list()
hyperList1 = list()
hyperList2 = list()

year3List = list()
year5List = list()
year7List = list()
year9List = list()

featList = list()
userInputList = list()

isManager =''

column = ['체질량지수', '수축기혈압', '이완기혈압', '식전혈당', '총콜레스테롤' , '혈색소', \
			'AST', 'ALT', '감마지티피', '과거병력코드1 ', '과거병력코드2', '과거병력코드3', \
			'간장질환유무 ', '고혈압유무 ', '뇌졸중유무', '심장병유무', '당뇨병유무', '암유무', '흡연상태', '흡연기간', '하루흡연량', \
			'음주습관', '1회 음주량 ', '1주 운동횟수 ' ]

# index must be aligned with html info
disease_Cat = ['nothing', 'tuberculosis', 'hepatitis', 'soyDisease', 'hypertension', 'heart', 'stroke', 'diabetes', 'cancer', 'others']
SMK_STAT_Cat = ['never','had_been','be_ing']
SMK_TERM_Cat = ['~5','5~9','10~19','20~29','30~']
DSQTY_Cat = ['0.5','0.5~1','1~2','2~']
DRNK_HABIT_Cat = ['none','monthly','weekly1~2','weekly3~4','daily']
DRNK_QTY_Cat = ['0.5','1','1.5','2']
EXERCI_Cat = ['0','1~2','3~4','5~6','7']



app = Flask(__name__)
app.secret_key = 'secret'

csvColumn = ['features','yearThree','yearFive','yearSeven','yearNine']
# mysql = MySQL()

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
# app.config['MYSQL_DATABASE_DB'] = 'test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)


def calculateResult_Logistic():

	pred_3Year = 0
	pred_5Year = 0
	pred_7Year = 0
	pred_9Year = 0

	i = 0

	for i in range(len(userInputList)):
		pred_3Year += userInputList[i] * year3List[i+1]
		pred_5Year += userInputList[i] * year5List[i+1]
		pred_7Year += userInputList[i] * year7List[i+1]
		pred_9Year += userInputList[i] * year9List[i+1]

	# add bias
	pred_3Year += year3List[0]
	pred_5Year += year5List[0]
	pred_7Year += year7List[0]
	pred_9Year += year9List[0]

	#exp Cacluation
	exp3Year = math.exp(pred_3Year)
	exp5Year = math.exp(pred_5Year)
	exp7Year = math.exp(pred_7Year)
	exp9Year = math.exp(pred_9Year)

	pred_3Year = round(exp3Year/(1+exp3Year),4)
	pred_5Year = round(exp5Year/(1+exp5Year),4)
	pred_7Year = round(exp7Year/(1+exp7Year),4)
	pred_9Year = round(exp9Year/(1+exp9Year),4)


	return [pred_3Year, pred_5Year, pred_7Year, pred_9Year]

	'''
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
'''


def ConvertStringListIntoFloatList(strList, floatList):
	for i in strList :
		if i :
			floatList.append(float(i))


def readCSVweight():
	csvData = pandas.read_csv('LogisticWeight.csv', names=csvColumn)
	year3List_str = csvData.yearThree.tolist()
	year5List_str = csvData.yearFive.tolist()
	year7List_str = csvData.yearSeven.tolist()
	year9List_str = csvData.yearNine.tolist()

	year3List_str.pop(0)
	year5List_str.pop(0)
	year7List_str.pop(0)
	year9List_str.pop(0)

	ConvertStringListIntoFloatList(year3List_str,year3List)
	ConvertStringListIntoFloatList(year5List_str,year5List)
	ConvertStringListIntoFloatList(year7List_str,year7List)
	ConvertStringListIntoFloatList(year9List_str,year9List)




def	changeCSV():
	#TOdo : 모두 바껴진 값을 csv에 다 떄려박는다
	pass

def yesNoToInt(str):
	if str == 'yes':
		return 0
	elif str == 'no':
		return 1     # no면 weight 값이 곱해지고, yes면 NA

def checkNone(value):
	if value == None:
		return 0
	else:
		return value

def diseaseCheckNone(value):
	if value == None:
		return "nothing"
	else:
		return value

def pushIndexInfoToList(value, totalLen):
	#value를 확인하고 해당 밸류를 제외한 앞뒤로 0을 밀어넣는다.
	if value == 0:
		userInputList.append(1)
		for i in range(1,totalLen):
			userInputList.append(0)

	else:
		for i in range(0,value):
			userInputList.append(0)

		userInputList.append(1)

		for i in range(value+1, totalLen):
			userInputList.append(0)


def	InsertSmokeData(SMK_STAT_v,SMK_TERM_v,DSQTY_v):
	smk_stat_V= SMK_STAT_Cat.index(SMK_STAT_v)

	if smk_stat_V == 0 : #not smoke
		pushIndexInfoToList(0, len(SMK_STAT_Cat)+len(SMK_TERM_Cat)+len(DSQTY_Cat))

	else:
		pushIndexInfoToList(smk_stat_V, len(SMK_STAT_Cat))
		pushIndexInfoToList(SMK_TERM_Cat.index(SMK_TERM_v), len(SMK_TERM_Cat))
		pushIndexInfoToList(DSQTY_Cat.index(DSQTY_v), len(DSQTY_Cat))


#######################################################################

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
	# 순서 중요함
	userInputList.append(float(request.form.get('BMI')))
	userInputList.append(float(request.form.get('BP_HIGH')))
	userInputList.append(float(request.form.get('BP_LWST')))
	userInputList.append(float(request.form.get('BLDS')))
	userInputList.append(float(request.form.get('TOT_CHOLE')))
	userInputList.append(float(request.form.get('HMG')))
	userInputList.append(float(request.form.get('SGOT_AST')))
	userInputList.append(float(request.form.get('SGPT_ALT')))
	userInputList.append(float(request.form.get('GAMMA_GTP')))

	pushIndexInfoToList(disease_Cat.index(diseaseCheckNone(request.form.get('HCHK_PMH_CD1'))), len(disease_Cat))
	pushIndexInfoToList(disease_Cat.index(diseaseCheckNone(request.form.get('HCHK_PMH_CD2'))), len(disease_Cat))
	pushIndexInfoToList(disease_Cat.index(diseaseCheckNone(request.form.get('HCHK_PMH_CD3'))), len(disease_Cat))
	userInputList.append(yesNoToInt(request.form.get('famLIVER', '')))
	userInputList.append(yesNoToInt(request.form.get('famHPRTS', '')))
	userInputList.append(yesNoToInt(request.form.get('famAPOP', '')))
	userInputList.append(yesNoToInt(request.form.get('famHDISE', '')))
	userInputList.append(yesNoToInt(request.form.get('famDIABML', '')))
	userInputList.append(yesNoToInt(request.form.get('famCANCER', '')))
	InsertSmokeData(request.form.get('SMK_STAT',''),request.form.get('SMK_TERM',''),request.form.get('DSQTY',''))
	print(userInputList)
	pushIndexInfoToList(DRNK_HABIT_Cat.index(request.form.get('DRNK_HABIT', '')), len(DRNK_HABIT_Cat))
	if request.form.get('TM1_DRKQTY') == None:
		pushIndexInfoToList(0, len(DRNK_QTY_Cat))  #반병이하로 처리.
	else:
		pushIndexInfoToList(DRNK_QTY_Cat.index(request.form.get('TM1_DRKQTY', '')), len(DRNK_QTY_Cat))

	pushIndexInfoToList(EXERCI_Cat.index(request.form.get('EXERCI', '')), len(EXERCI_Cat))
	# validation check (유효성 검사)

	# if not famLIVER or not famHPRTS or not famAPOP \
	# 	or not famHDISE or not famDIABML or not famCANCER \
	# 	or not [v for v in request.form.getlist('attributes[]')] :

	# 	errors = "Please enter all the fields."

	# 	return render_template('measure.html', errors = errors)

	print(userInputList)
	logisticResults = calculateResult_Logistic()

	pred3year = logisticResults[0]
	pred5year = logisticResults[1]
	pred7year = logisticResults[2]
	pred9year = logisticResults[3]

	print(pred3year,pred5year,pred7year,pred9year)

	del userInputList[:] #계산하고 지움.
	#return render_template('result.html')
	return render_template('result.html', pred3year=pred3year, pred5year=pred5year,pred7year=pred7year,pred9year=pred9year) # 임시로 최종 결과를 메인페이지 볼수 있게 처리함.



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
	file = request.files['file']

	#if file :
		#filename = secure_filename(file.filename)

	ss = file.read().decode('utf-8')
	print(ss)

#	stream = io.StringIO(file.stream.read().decode('utf-8') , newline=None)
	#csv_input = csv.reader(stream)

	#readCSVweight(file.read())


	#readCSVweight(open(request.files['file']))
	#print(request.files['file'])

	return redirect(url_for('showMainPage'))




if __name__=="__main__":
	app.run(debug=True, host = '127.0.0.1', port= 5000)
	#app.run(host='163.152.184.176', port= 5000, debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

