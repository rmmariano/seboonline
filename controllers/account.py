@auth.requires_login() 
def myaccount():
	response.flash = T("Welcome to web2py!")
	return dict(message=T('Hello World'))