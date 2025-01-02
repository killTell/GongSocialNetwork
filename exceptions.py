class errors(Exception):
	def __init__(self,*args):
		self.errorcode = 0
		if args:
			self.errorcode = args[0]
		else:
			self.errorcode = None

	def __str__(self):
		if self.errorcode == 1:
			return "Пароль должен начинаться с букв!"
		elif self.errorcode == 2:
			return "Имя пользователя должно начинаться с букв!"
		elif self.errorcode == 3:
			return "Слишком короткий пароль или имя пользователя"
		elif self.errorcode == 4:
			return "Слишком короткая почта"
		if self.errorcode == 5:
			return "Неправильный пароль или имя пользователя!"
		elif self.errorcode == 6:
			return "Такой пользователь уже зарегистрирован!"