@auth.requires_login() 
def myitems():
	grid = SQLFORM.smartgrid(db.item,linked_tables=['title'])
	return dict(grid=grid)