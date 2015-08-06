# -*- coding: utf-8 -*-

from gluon import current

def requires_membership(auth_user_id,group_role):
	db = current.db #referência de memória do db corrente
	group=db(db.auth_group.role==group_role).select()
	isempty=db((db.auth_membership.user_id==auth_user_id)&(db.auth_membership.group_id==group[0].id)).isempty()
	if not isempty:
	    return True
	else:
	    return False

def update_auth_user(auth):
	try:
		foo = dict(auth.profile().as_dict()['record'])
		del foo['password']
		auth.user.update(**foo)
	except:
		pass