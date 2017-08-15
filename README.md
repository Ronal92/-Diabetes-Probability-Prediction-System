#변경 사항은 아래에요~

##1. measure.html -> hello.py (브라우저에서 받은 입력값 처리)

	for v in request.form.getlist('attributes[]')
		==> attributes[] 배열에 담겨오는 변수들임. 그 외 나머지는 라디오 체크 변수들인데 배열에 담을 수 없어서 아래처럼 따로 불러와야함.

	famLIVER 		= request.form.get('famLIVER', '')
	famHPRTS 		= request.form.get('famHPRTS', '')
	famAPOP 		= request.form.get('famAPOP', '')
	famHDISE 		= request.form.get('famHDISE', '')
	famDIABML 		= request.form.get('famDIABML', '')
	famCANCER 		= request.form.get('famCANCER', '')

### attributes[]에서 변수를 불러오는 순서
 	체질량지수
	총 콜레스트롤
	감마지티피
	수축기혈압 
	혈색소 
	과거병력(1) 
	이완기혈압 
	AST 
	과거병력(2) 
	식전혈당 ALT 
	과거병력(3) 
	흡연상태 
	음주습관 
	흡연기간 
	1회 음주량 
	HDL
	GPT 
	하루흡연량 
	1주 운동횟수

### 라디오 체크 변수들

	famLIVER 	:	간장질환유무
	famHPRTS 	:	고혈압유무
	famAPOP 	:	뇌졸중유무
	famHDISE 	:	심장병유무
	famDIABML 	:	당뇨병유무
	famCANCER   :	암유무

##2. setting.html -> hello.py (브라우저에서 받은 입력값 처리)
	
	**배열**
	changedDL1[] : diabetes 1
	changedDL2[] : diabetes 2
	changedHL1[] : hypertension 1
	changedHL2[] : hypertension 2

##3. uploadCSV.html -> hello.py (파일 업로드)