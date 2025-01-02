import exceptions
import string
alphabet = list(string.ascii_lowercase + string.ascii_uppercase)

def checkpassword(password:str,login:str):
	if len(password) > 0 and password[0] not in alphabet:
		return exceptions.errors(1)
	elif len(password ) < 4:
		return exceptions.errors(3)
	elif len(login) < 3:
		return exceptions.errors(3)
	return True

def getinfo(db, user):
	for line in db.query.all():
		if line.username == user:
			return [line.username, line.Subscribers, line.friends_cnt]

def getuserbyname(db, user,passw):
	for line in db.query.all():
		if line.username == user and line.password == passw:
			return True
	return False
		
def getusers(db,part):
	all_users = []
	for line in db.query.all():
		if part == '' or part==None:
			all_users.append(line.username)
		else:
			if part in line.username:
				all_users.append(line.username)
	return all_users
def isuserthere(db,user):
	for line in db.query.all():
		if line.username == user:
			return True

	return False