# -*- coding: utf-8 -*-
from common import update_auth_user

@auth.requires_login() 
@auth.requires_membership('admin')
def users():
	form = SQLFORM.smartgrid(db.auth_user,linked_tables=['item'],searchable= dict(item=False))
	update_auth_user(auth) #depois que atualizar as inf, atualiza a sessão
	return dict(form=form)

@auth.requires_login() 
@auth.requires_membership('admin')
def categories():
	form = SQLFORM.smartgrid(db.item_category,linked_tables=['name_item_category'])
	return dict(form=form)

@auth.requires_login() 
@auth.requires_membership('admin')
def myitems_admin():
	form=SQLFORM.smartgrid(db.item)
	return dict(form=form)

@auth.requires_login() 
def myitems():
	#form = SQLFORM.grid(query=((db.item.created_by==auth.user_id)))
	#form = SQLFORM.smartgrid(query=db.item.created_by==auth.user_id)
	#SQMFORM.smartgrid(table, constraints = dict(tablename = query))
	form=SQLFORM.smartgrid(db.item,constraints=dict(item=db.item.created_by==auth.user_id))
	return dict(form=form)




######################################################
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)