from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy

app = Flask(__name__)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/shelters/<int:shelter_id>/')
def shelters(shelter_id):
	shelter = session.query(Shelter).filter_by(id=shelter_id).one()
	puppies = session.query(Puppy).filter_by(shelter_id=shelter.id)
	return render_template('shelters.html', shelters=shelter, puppies=puppies)

@app.route('/shelters/<int:shelter_id>/new/', methods=['GET', 'POST'])
def newPuppy(shelter_id):
	if request.method == 'POST':
		newPuppy = puppies(
			name=request.form['name'], shelter_id=shelter_id)
		session.add(newPuppy)
		session.commit()
		flash("Added a new pup!")
		return redirect(url_for('shelters', shelter_id=shelter_id))
	else:
		return render_template('newpuppy.html', shelter_id=shelter_id)

@app.route('/shelters/<int:shelter_id>/<int:puppy_id>/edit', methods=['GET','POST'])
def editPuppy(shelter_id, puppy_id):
	editedPup = session.query(Puppy).filter_by(id=puppy_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedPup.name = request.form['name']
		session.add(editedPup)
		session.commit()
		flash("Edited pup!")
		return redirect(url_for('shelters', shelter_id=shelter_id\
			, puppy_id=puppy_id, i = editedPup))
	else:
		return render_template('editpuppy.html', \
			shelter_id=shelter_id, puppy_id=puppy_id, i = editedPup)

@app.route('/shelters/<int:shelter_id>/<int:puppy_id>/delete', methods=['GET','POST'])
def deletePuppy(shelter_id, puppy_id):
	deletedPup = session.query(Puppy).filter_by(id=puppy_id).one()
	if request.method == 'POST':
		session.delete(deletedPup)
		session.commit()
		flash("Pup deleted!")
		return redirect(url_for('shelters', \
			shelter_id=shelter_id, puppy_id=puppy_id))
	else:
		return render_template('deletepuppy.html', i = deletedPup,\
			puppy_id=puppy_id, shelter_id=shelter_id)



if __name__ == '__main__':
	app.secret_key = 'super secret key'
   	app.debug = True
	app.run(host='0.0.0.0', port=5000)
