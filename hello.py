from flask import Flask, render_template
app = Flask(__name__)

# @app.errorhandler(404)
# def page_not_found(error):
# 	app.logger.error(error)
# 	return render_template('page_not_found.html'), 404



@app.route("/")
def hello(name=None):
	return render_template("hello.html")

@app.route("/signUp", methods=['GET','POST'])
def showSignUp():
	print("showSignUp")
	return render_template('signup.html')


if __name__=="__main__":
	app.run(debug=True)

#<!-- page_not_found.html -->
#sorry, snacky... page not found...

