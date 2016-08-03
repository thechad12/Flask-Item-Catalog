from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from database import Base, Category, Item, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
<<<<<<< HEAD
import xml.etree.cElementTree as et

=======
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6

app = Flask(__name__)

# Open client secrets
CLIENT_ID = json.loads(
	open('google.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "item catalog app"

# Connect to database and create session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


<<<<<<< HEAD

=======
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
#JSON API endpoints
@app.route('/categories/JSON/')
def categoriesJSON():
	categories = session.query(Category).all()
	return jsonify(categories=[c.serialize for c in categories])

@app.route('/items/JSON/')
def itemsJSON():
	items = session.query(Item).all()
	return jsonify(items=[i.serialize for i in items])

@app.route('/category/<int:category_id>/JSON/')
def categoryJSON(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	items = session.query(Item).filter_by(category_id=category_id).all()
	return jsonify(items=[i.serialize for i in items])

# Create anti-forgery state token
@app.route('/login/')
def showLogin():
	state = ''.join(random.choice(
		string.ascii_uppercase + string.digits)
		for x in range(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)
<<<<<<< HEAD
# Logout the user
@app.route('/logout')
def logout():
	session.delete(login_session)
	session.commit()
	flash("You have successfully been logged out.")
	return render_template('catalog.html')
=======
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6

def createUser(login_session):
	newUser = User(name=login_session['username'],
		email=login_session['email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user = User(name=login_session['username'],
		email=login_session['email'], picture=login_session['picture'])
	return user

def getUserId(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

# Google login session
@app.route('/gconnect', methods=['POST'])
def gconnect():
<<<<<<< HEAD
	# Validate state token
=======
	 # Validate state token
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
<<<<<<< HEAD
        oauth_flow = flow_from_clientsecrets('google.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        #flow = OAuth2WebServerFlow(CLIENT_ID=google['web']['CLIENT_ID'],
        							#client_secret=google['web']['client_secret'],
        							#scope='',
        							#redirect_uri=oauth_flow.redirect_uri)
=======
        google = json.loads(open('google.json', 'r').read())
        oauth_flow = flow_from_clientsecrets('./google.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        client_id = google['web']['client_id']
        credentials = oauth_flow.step2_exchange(code)
        flow = OAuth2WebServerFlow(client_id=google['web']['client_id'],
        							client_secret=google['web']['client_secret'],
        							scope='',
        							redirect_uri=oauth_flow.redirect_uri)
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
<<<<<<< HEAD
    print "access token" + " " + access_token
=======
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    http = credentials.authorize(h)
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
<<<<<<< HEAD
    if result['issued_to'] != CLIENT_ID:
=======
    if result['issued_to'] != client_id:
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

<<<<<<< HEAD
    stored_credentials = login_session.get('access_token')
=======
    stored_credentials = login_session.get('credentials.access_token')
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response

<<<<<<< HEAD
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.to_json();
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

=======
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
     # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
<<<<<<< HEAD
    data = json.loads(answer.text)


    # Store the access token in the session for later use.
=======
    data = answer.json()


    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.to_json();
    login_session['gplus_id'] = gplus_id
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserId(login_session['email'])
    login_session['user_id'] = user_id



    if not user_id:
        user_id = createUser(login_session)


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

<<<<<<< HEAD
@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('access_token')
    print "in gdisconnect credentials === ", credentials
    if credentials is None:
        response = make_response(
            json.dumps('Current user is not connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    print "url ====", url
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print "result ==== ", result
    if result['status'] == '200':
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    return render_template("catalog.html")
=======

@app.route('/gdisconnect')
def gdisconnect():
	#Disconnect a connected user
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(
			json.dumps('Current user not connected'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	if result['status'] != '200':
	 	response = make_response(json.dumps
	 		('Failed to revoke token for given user'), 400)
	 	respon.headers['Content-Type'] = 'application/json'
	 	return response
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6

@app.route('/fbconnect')
def fbconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'),
			 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	access_token = request.data
	print "access token received %s" % access_token

	app_id = json.loads(open('facebook.json', 'r').read())
	['web']['app_id']
	app_secret = json.loads(open('facebook.json', 'r').read())
	['web']['app_secret']
<<<<<<< HEAD
	url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&CLIENT_ID=%s&client_secret=%s&fb_exchange_token=%s' % (
=======
	url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
        app_id, app_secret, access_token)
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]

	# Use token to get the user info from the API
	userinfo_url = "https://graph.facebook.com/v2.4/me"
	token = result.split("&")[0]

	url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]

	data = json.loads(result)
	login_session['provider'] = 'facebook'
	login_session['username'] = data['name']
	login_session['email'] = data['email']
	login_session['facebook_id'] = data['id']

	# Store the token in the session, in order to properly disconnect
	# Split from the equals sign
	stored_token = token.split("=")[1]
	login_session['access_token'] = stored_token

	# Load the user picture
	url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]
	data = json.loads(result)

	login_session['picture'] = data["data"]["url"]

	# Check that user actually exists
	# If not, create new user
	user_id = getUserId(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output +='<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' "style = "width: 300px; height: 300px;\
	border-radius: 150px; -webkit-border-radius: 150px;\
	-moz-border-radius: 150px">"'
	flash("Now logged in as % s" % login_session['username'])
	return output

@app.route('/fbdisconnect')
def fbdisconnect():
	facebook_id = login_session['facebook_id']
	# Access token must be included to be successful
	access_token = login_session['access_token']
	url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
	h = httplib2.Http()
	result = h.request(url, 'DELETE')[1]
	print "You have successfully been logged out"

# Show catalog with categories and latest items
@app.route('/')
@app.route('/catalog/')
def catalog():
	category = session.query(Category).all()
	latest_items = session.query(Item).order_by(Item.date.desc()).limit(5)
	if 'username' not in login_session:
 		return render_template('catalog.html', category=category)
 	else:
 		return render_template('privatecatalog.html', category=category)

# Show one category with items
@app.route('/catalog/<int:category_id>/', methods=['GET', 'POST'])
def showCategory(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	items = session.query(Item).filter_by(
		category_id=category_id).all()
	return render_template('category.html', items=items, category=category)

# Show item with description
@app.route('/catalog/<int:category_id>/<int:item_id>', methods=['GET', 'POST'])
def showItem(item_id, category_id):
	item = session.query(Item).filter_by(
		id=item_id).one()
	return render_template('item.html', item=item)

# Create new item
@app.route('/catalog/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
<<<<<<< HEAD

	image = request.files['image']
	image_data = None

	if image:
		return render_template('new_item.html', category_id=category_id)
		image_data = image.read()

	if request.method == 'POST':
		new_Item = Item(item_name=request.form['item_name'],
=======
	if request.method == 'POST':
		new_Item = Item(item_name=request.form['name'],
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
			 description=request.form['description'],
			 date=request.form['date'],
			 category_id=category_id,
			 user_id=login_session['user_id'])
<<<<<<< HEAD
		if image_data:
			item.image = image.filename
			item.image_data = image_data

		session.add(new_Item)
		session.commit()
		flash("New Item Added Successfully")
		return redirect(url_for('showCategory', category_id=category_id))
=======
		session.add(new_Item)
		session.commit()
		flash("New Item Added Successfully")
		return redirect(url_for('showCategory', category=category))
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
	else:
		return render_template('new_item.html', category_id=category_id)

# Edit existing item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
	editedItem = session.query(Item).filter_by(id=item_id).one()
	category = session.query(Category).filter_by(id=category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
<<<<<<< HEAD
	if editedItem.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this item.')}</script>"
	if request.method == 'POST':
		if request.form['name']:
			editedItem.item_name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['date']:
			editedItem.date = request.form['date']
=======
	if editItem.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this item.')}</script>"
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['desctiption']:
			editedItem.description = request.form['description']
		if request.form['date']:
			editedItem.date = request.form['date']
		if request.form['picture']:
			editedItem.picture = request.form['picture']
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
		session.add(editedItem)
		session.commit()
		flash("Item edited successfully")
		return redirect(url_for('showCategory', category_id=category_id))
	else:
		return render_template('edit_item.html', category_id=category_id,
<<<<<<< HEAD
			item_id=item_id, editedItem=editedItem)
=======
			item_id=item_id)
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6

# Delete existing item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
	category = session.query(Category).filter_by(id=category_id).one()
	deletedItem = session.query(Item).filter_by(id=item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
<<<<<<< HEAD
	if deletedItem.user_id != login_session['user_id']:
=======
	if deleteItem.user_id != login_session['user_id']:
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6
		return "<script>function myFunction() {alert('You are not authorized to delete this item.')}</script>"
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
<<<<<<< HEAD
		flash("Item successfully deleted")
		return redirect(url_for('showCategory', category_id=category_id))
	else:
		return render_template('delete_item.html', category_id=category_id,
			item_id=item_id, deletedItem=deletedItem)
=======
		return render_template('delete_item.html', category_id=category_id,
			item_id=item_id)
>>>>>>> 42f930646aa82e3fa861f26faed66c4929ff13f6



if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)