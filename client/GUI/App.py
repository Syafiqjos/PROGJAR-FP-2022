import tkinter as tk

import sys
sys.path.append('..')

root_original = None
root = None

dataManager = None
socketManager = None
accountSocket = None
gameSocket = None

def find_match(token, role):
	if accountSocket != None:
		res = accountSocket.sendFindMatchEvent(token, role)

		return res
	return None

def on_login_success(res):
	token = res['token']
	role = res['role_input']

	dataManager.set('user_email', res['email_input'])
	dataManager.set('user_password', res['password_input'])
	dataManager.set('user_token', token)
	dataManager.set('user_role', role)

	ne = find_match(token, role);
	print(ne)
	if ne['success'] and ne['match_status'] == 'waiting':
		anotherNe = socketManager.receive()
		print(anotherNe)

	root_original.quit()

def on_login_user_not_found(res):
	print('User not found!')

def on_login_invalid_password(res):
	print('User Password wrong!')

def on_login_email_and_password_empty(res):
	print('Email and password are empty')

def on_login_error(res):
	print(res['message'])

def on_login(res):
	if res['success'] == True:
		on_login_success(res)
	elif res['message'] == 'Email and password are required!':
		on_login_email_and_password_empty(res)
	elif res['message'] == 'Email is not registered!':
		on_login_user_not_found(res)
	elif res['message'] == 'Wrong password!':
		on_login_invalid_password(res)
	else:
		on_login_error(res)

def try_login(entries, role = 'plant'):
	email_input = entries['Email'].get()
	password_input = entries['Password'].get()
	role_input = role

	print(email_input, password_input)

	if accountSocket != None:
		res = accountSocket.sendAccountLoginEvent(email_input, password_input)
		res['email_input'] = email_input
		res['password_input'] = password_input
		res['role_input'] = role_input

		print(res)
		on_login(res)

def try_register(entries):
	email_input = entries['Email'].get()

	print(email_input)

	if accountSocket != None:
		res = accountSocket.sendAccountRegisterEvent(email_input)
		print(res)

def makeform(root, fields, values = None):
	entries = {}
	for it in range(len(fields)):
		field = fields[it]
		value = ''

		if values is not None:
			value = values[it]

		row = tk.Frame(root)
		lab = tk.Label(row, width=22, text=field+": ", anchor='w')
		ent = tk.Entry(row)
		ent.insert(0, value)
		row.pack(side = tk.TOP, fill = tk.X, padx = 5 , pady = 5)
		lab.pack(side = tk.LEFT)
		ent.pack(side = tk.RIGHT, expand = tk.YES, fill = tk.X)
		entries[field] = ent
	return entries

def reset_window(root):
	for widget in root.winfo_children():
		widget.destroy()

def make_login_window(root):
	reset_window(root)

	fields = ('Email', 'Password')

	heading = tk.Label(root, width=32, text="Login Account", anchor='n')
	heading.pack(side = tk.TOP, fill = tk.X, padx = 5 , pady = 5)

	ents = makeform(root, fields)

	b12 = tk.Button(root, text = 'Login as Zombie',
		command=(lambda e = ents: try_login(e, 'zombie')))
	b12.pack(side = tk.RIGHT, padx = 5, pady = 5)

	b1 = tk.Button(root, text = 'Login as Plant',
		command=(lambda e = ents: try_login(e, 'plant')))
	b1.pack(side = tk.RIGHT, padx = 5, pady = 5)

	b2 = tk.Button(root, text='Register',
	command=(lambda e = ents: make_register_window(root)))
	b2.pack(side = tk.LEFT, padx = 5, pady = 5)
	b3 = tk.Button(root, text = 'Quit', command = root.quit)
	b3.pack(side = tk.LEFT, padx = 5, pady = 5)

	return ents

def make_register_window(root):
	reset_window(root)

	fields = ('Email',)

	heading = tk.Label(root, width=32, text="Register New Account", anchor='n')
	heading.pack(side = tk.TOP, fill = tk.X, padx = 5 , pady = 5)

	ents = makeform(root, fields)

	b1 = tk.Button(root, text = 'Register',
		command=(lambda e = ents: try_register(e)))
	b1.pack(side = tk.RIGHT, padx = 5, pady = 5)
	b2 = tk.Button(root, text='Login',
	command=(lambda e = ents: make_login_window(root)))
	b2.pack(side = tk.LEFT, padx = 5, pady = 5)
	b3 = tk.Button(root, text = 'Quit', command = root.quit)
	b3.pack(side = tk.LEFT, padx = 5, pady = 5)

	return ents

def app(m_dataManager, m_socketManager = None, m_accountSocket = None, m_gameSocket = None):
	global root_original
	global root

	global dataManager
	global socketManager
	global accountSocket
	global gameSocket

	dataManager = m_dataManager
	socketManager = m_socketManager
	accountSocket = m_accountSocket
	gameSocket = m_gameSocket

	if socketManager != None:
		socketManager.connect()

	root_original = tk.Tk()
	root = tk.Frame(root_original)
	root.pack(side = tk.LEFT)
	ents = make_login_window(root)

	root.mainloop()