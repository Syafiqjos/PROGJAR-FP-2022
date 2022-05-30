from .SocketSender import SocketSender;

class AccountSocket(SocketSender):
	def sendAccountLoginEvent(self, email, password):
		return self.send({
            "request": "login",
            "email": email,
			"password": password
        })

	def sendAccountRegisterEvent(self, email):
		return self.send({
            "request": "register",
            "email": email
        })

	def sendFindMatchEvent(self, email):
		return self.send({
            "request": "find_match",
            "email": email
        })

	def sendCancelFindMatchEvent(self, token, role):
		return self.send({
            "request": "cancel_find_match",
            "token": token,
			"role": role
        })