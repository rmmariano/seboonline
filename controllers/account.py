@auth.requires_login() 
def info():
	response.flash = T("Welcome to info!")
	return dict(message=T('Hello World'))

@auth.requires_login() 
def myitems():
	response.flash = T("Welcome to web2py!")
	return dict(message=T('Hello World'))