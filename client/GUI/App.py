import tkinter as tk

import sys
sys.path.append('..')

dataManager = None
socketManager = None
accountSocket = None
gameSocket = None

def try_login(entries):
	email_input = entries['Email'].get()
	password_input = entries['Password'].get()

	print(email_input, password_input)

	if accountSocket != None:
		res = accountSocket.sendAccountLoginEvent(email_input, password_input)
		print(res)

def try_register(entries):
	email_input = entries['Email'].get()

	print(email_input)

	if accountSocket != None:
		res = accountSocket.sendAccountRegisterEvent(email_input)
		print(res)

def makeform(root, fields):
	entries = {}
	for field in fields:
		row = tk.Frame(root)
		lab = tk.Label(row, width=22, text=field+": ", anchor='w')
		ent = tk.Entry(row)
		ent.insert(0,"")
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

	b1 = tk.Button(root, text = 'Login',
		command=(lambda e = ents: try_login(e)))
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
	ents = make_register_window(root)

	root.mainloop()