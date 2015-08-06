# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

from gluon import current

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

current.db = db

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

auth.settings.extra_fields['auth_user']=[
                                                        Field('image', 'upload',default="static/images/others/no-image.jpg"),
                                                        Field('created_on', 'datetime', default=request.now,writable = False),
                                                        Field('created_by', 'reference auth_user', default=auth.user_id,writable = False),
                                                        Field('updated_on', 'datetime', update=request.now,writable = False),
                                                        Field('updated_by', 'reference auth_user', update=auth.user_id,writable = False)
                                                           ]

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)



db.define_table('item_category',
                        Field('name_item_category','string'),
                        Field('created_on', 'datetime', default=request.now,writable = False),
                        Field('created_by', 'reference auth_user', default=auth.user_id,writable = False),
                        Field('updated_on', 'datetime', update=request.now,writable = False),
                        Field('updated_by', 'reference auth_user', update=auth.user_id,writable = False))

db.define_table('item',
                        Field('title','string'),
                        Field('category_id','reference item_category'),
                        Field('description','string'),                        
                        Field('created_on', 'datetime', default=request.now,writable = False),
                        Field('created_by', 'reference auth_user', default=auth.user_id,writable = False),
                        Field('updated_on', 'datetime', update=request.now,writable = False),
                        Field('updated_by', 'reference auth_user', update=auth.user_id,writable = False))


db.item_category.name_item_category.requires = IS_NOT_EMPTY()
'''
db.item_category.created_by.readable = db.item_category.created_by.writable = False
db.item_category.created_on.readable = db.item_category.created_on.writable = False
db.item_category.updated_by.readable = False
db.item_category.updated_on.readable = False
'''

db.item.title.requires = IS_NOT_EMPTY()
db.item.category_id.requires=IS_IN_DB(db, db.item_category.id,'%(name_item_category)s',zero='Selecione uma categoria',error_message='Categoria não encontrada.')
db.item.description.requires = IS_NOT_EMPTY()
'''
db.item.created_by.readable = db.item.created_by.writable = False
db.item.created_on.readable = db.item.created_on.writable = False
'''
