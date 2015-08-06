from common import requires_membership

@auth.requires_login() 
@auth.requires_membership('administrator')
def users():
	grid = SQLFORM.smartgrid(db.auth_user,linked_tables=['name'])
	return dict(grid=grid)

@auth.requires_login() 
def myitems():
	grid = SQLFORM.smartgrid(db.item,linked_tables=['title'])

	'''
	if requires_membership(auth.user_id,'administrator'):
	    print 'passou o/'
	else:
	    print 'nao passou :/'
	'''

	return dict(grid=grid)