from imports import *
from random import *
import socket
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "DEVELOPER"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
class user(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(16),nullable=False,unique=True)
	password = db.Column(db.String(16),nullable=False)
	Subscribers = db.Column(db.Integer,nullable=False)
	friends_cnt = db.Column(db.Integer,nullable=False)
	def __repr__(self):
		return f"{self.username}:{self.password}"


@login_manager.user_loader
def loader_user(user_id):
	return user.query.get(user_id)

@app.before_request
def create_table():
	db.create_all()

@app.route('/login', methods=["GET","POST"])
def loginpage():
	value3 = ""
	if request.method == "POST" and "submitbtn" in request.form:
		username = request.form.get("usr")
		password = request.form.get('passw')
		new_user = user.query.filter_by(username=username).first()
		if current_user.is_active:
			value3 = "Перед входом в другой, сначала выйдите с этого!"
		else:
			if new_user:
				if getuserbyname(user,username,password):
					if not current_user.is_active:
						login_user(new_user)
						return redirect(f'profile/{username}')
				else:
					value3=exceptions.errors(5)
			else:
				value3=exceptions.errors(5)

	return render_template("login.html",value2=value3)

@app.route('/userchoice', methods=["GET","POST"])
def userchoicepage():
	if request.method == "POST":
		if "registerbtn" in request.form:
			return redirect("/register")
		elif "loginbtn" in request.form:
			return redirect("/login")
	return render_template("choice.html")

@app.route("/register",methods=['GET','POST'])
def registerpage():
	value1=""
	if request.method == "POST":
		username = request.form.get("usr")
		password = request.form.get("passw")
		try:
			if checkpassword(password,username) != True:
				value1 = checkpassword(password,username)
			elif isuserthere(user,username):
				value1 = exceptions.errors(6)
				print(user.query.all())
			else:
				if current_user.is_active:
					value1 = "Перед созданием аккаунта, сначала выйдите с этого!"
				else:
					new_user = user(username=username,password=password,Subscribers=0,friends_cnt=0)
					
					db.session.add(new_user)
					db.session.commit()

					print(user.query.all())
					value1=""
					return redirect(f"profile/{username}")
		except Exception as e:
			raise e
			print(user.query.all())
	return render_template("register.html",value=value1)

@app.route('/')
def start():
	return redirect("/userchoice")
@app.route('/logout', methods=['GET','POST'])
def logout():
	logout_user()
	return redirect("/userchoice")
@app.route("/profile/<username>",methods=['GET','POST'])
def loadprofilepage(username): 
	try:
		information = getinfo(user,username)
		if request.method == "POST":
			if "logout" in request.form:
				return redirect(url_for("logout"))
			elif "subscribe" in request.form:
				if information[0] != current_user.username:
					current_user.friends_cnt += 1
					user1 = user.query.filter_by(username=information[0]).first()
					user1.friends_cnt = user1.friends_cnt + 1
					db.session.commit()
		return render_template("profile.html",profile_username=information[0],subs=information[1],friends_count=information[2])
	except TypeError:
		return render_template("profile.html",profile_username="USER NOT FOUND!",subs=0,friends_count=0)

@app.route("/profile",methods=['GET','POST'])
def foundaccount():
	value=""
	if request.method == "POST":
		value=""
		full_word = ""
		print(request.form.get("finduser"))
		for i in getusers(user, request.form.get("finduser")):
			full_word += i+" "
		value = full_word
		return render_template("profilefound.html",result=value)

	return render_template("profilefound.html",result=value)
@app.route("/administrator",methods=['GET','POST'])
@login_required
def adminmenu():
	if current_user.username != "admin":
		return "access denied"
	else:
		if request.method == "POST":
			if "ok" in request.form:
				username = request.form.get("useradder_inp")
				password = request.form.get("userpassw_inp")
				new_user = user(username=username,password=password,Subscribers=0,friends_cnt=0)
				db.session.add(new_user)
				db.session.commit()
				print(user.query.all())
		return render_template("adminmenu.html")

if __name__ == '__main__':
	app.run(debug=True)
