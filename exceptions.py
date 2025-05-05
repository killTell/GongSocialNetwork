class errors(Exception):
	def __init__(self,*args):
		self.errorcode = 0
		if args:
			self.errorcode = args[0]
		else:
			self.errorcode = None

	def __str__(self):
		_errors = {1:"Пароль должен начинаться с букв!",2:"Имя пользователя должно начинаться с букв!",3:"Слишком короткий пароль или имя пользователя",
			  4:"Слишком короткая почта",5:"Неправильный пароль или имя пользователя!",6:"Такой пользователь уже зарегистрирован!"}
		return _errors[self.errorcode]
