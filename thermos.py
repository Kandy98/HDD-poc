from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from dbtables import *
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
#app.secret_key = 'meow'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/hdd'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def index():
	return render_template('home.html') #title = "Title passed from view to template", user = User("Kandarp", "Verma"))


#-------------------------------test
# @app.route('/concept/test')
# def concept_test():
# 	concept_t = Concept(cid="Medication frequency", concept_definition="Tells about the time duration between subsiquent intake of medicine", type=1)  
# 	session.add(concept_t)  
# 	session.commit()
# 	return "Tuple created"


#------concepts begin
#------concepts Create
@app.route('/concept/create', methods = ['GET', 'POST'])
def concept_create():
	if request.method == "POST":
		ci = request.form['cid']
		c_d = request.form['c_d']
		t = request.form['type']
		concept_c = Concept(cid=ci, definition=c_d, type=t)
		concept_c.status = 1
		concept_c.vnd = "0.0"
		concept_c.doud = datetime.utcnow()

		concept_c.add_concept()
		flash("Stored concept '{}'".format(ci))
		return redirect(url_for('index'))
	return render_template('testy.html') 

#------concepts Read
@app.route('/concept/read', methods = ['GET', 'POST'])
def concept_read():
	if request.method == "POST":
		id = request.form['id']
		con = Concept()
		return jsonify({'concept' : con.get_concept(id)})
	return render_template('concept_read.html')

#------concepts Update
@app.route('/concept/update', methods = ['GET', 'POST'])
def concept_update():
	if request.method == "POST":
		id = request.form['id']
		ci = request.form['cid']
		c_d = request.form['c_d']
		t = request.form['type']
		sta = request.form['status']
		vn = request.form['vnd']
		con = Concept() 
		#n_com = con.update_concept(id, ci, c_d, t, sta, vn)
		flash("Updated concept '{}'".format(id))
		return jsonify({'concept' : con.update_concept(id, ci, c_d, t, sta, vn)})
	return render_template('concept_update.html')


#------concepts Delete
@app.route('/concept/delete', methods = ['GET', 'POST'])
def concept_delete():
	if request.method == "POST":
		id = request.form['id']
		con = Concept()
		con.delete_concept(id)
		# c_d = db.session.query(Concept).filter_by(ncid=id).delete()
		# db.session.commit()
		flash("Deleted concept '{}'".format(id))
		return redirect(url_for('index'))
	return render_template('concept_delete.html')

#------concepts get_all_concept
@app.route('/concept/get_all_concept')
def get_all_concept():
	con = Concept()
	return jsonify({'Concepts' : con.get_all_concept()})

#------concepts get_concept_by_name
@app.route('/concept/getConceptByName', methods = ['GET', 'POST'])
def concept_getConceptByName():
	if request.method == "POST":
		cid = request.form['cid']
		con = Concept()
		return jsonify({'Concepts' : con.getConceptByName(cid)})
	return render_template('concept_rbn.html') 

#------concepts get_representations by concept
@app.route('/concept/getRepresentationByConcept', methods = ['GET', 'POST'])
def concept_getRepresentationsByConcept():
	if request.method == "POST":
		cid = request.form['id']
		# con = db.session.query(Concept).filter_by(ncid=cid).first()
		# data = []
		# for i in con.representations:
		# 	rep = i.representation_id
		# 	repser = db.session.query(Representation).filter_by(representation_id=rep).first()
		# 	#return repser.definition
		# 	data.append(repser)
		# return render_template('concept_representation.html', data)
		con = Concept()
		return jsonify({'Representations' : con.getRepresentationsByConcept(cid)})
	return render_template('concept_getRepresentationsByConcept.html')


#-----concepts end


#------concept_representation begin
#------concept_representation Create
@app.route('/concept_representations/create', methods=['GET', 'POST'])
def concept_representations_create():
	if request.method == "POST":
		ci = request.form['cid']
		c_d = request.form['c_d']
		rep_c = Representation(representation_cid=ci, definition=c_d)
		rep_c.status = 1
		rep_c.vnd = "0.0"
		rep_c.doud = datetime.utcnow()

		rep_c.add_representation()
		flash("Stored representation '{}'".format(ci))
		return redirect(url_for('index'))
	return render_template('representation_create.html') 

#------concept_representation Read
@app.route('/concept_representations/read', methods=['GET', 'POST'])
def concept_representations_read():
	if request.method == "POST":
		id = request.form['id']
		con = Representation()
		return jsonify({'representation' : con.get_representation(id)})
	return render_template('representation_read.html')

#------concept_representation Update
@app.route('/concept_representations/update')
def concept_representations_update():
	if request.method == "POST":
		id = request.form['id']
		ci = request.form['cid']
		d = request.form['c_d']
		vn = request.form['vnd']
		con = Representation() 
		flash("Updated representation '{}'".format(id))
		return jsonify({'representation' : con.update_representation(id, ci, d, vn)})
	return render_template('representation_update.html')
	# concept_representations_u = db.session.query(Concept_representations)
	# for i in concept_representations_u:
	# 	if i.representation_id==21:
	# 		con_u = i
	# con_u.representation = "hehe changed"
	# db.session.commit()
	# return "Tuple updated"

#------concept_representation Delete
@app.route('/concept_representations/delete')
def concept_representations_delete():
	concept_representations_d = session.query(Concept_representations)
	for i in concept_representations_d:
		if i.representation_id==21:
			con_d = i
	db.session.delete(con_d)  
	db.session.commit()
	return "Tuple deldeted"

#------concept_representation get_concept_from_representation
@app.route('/concept_representations/getcfr')
def concept_representations_getcfr():
	rep = "NUID"
	con_re = db.session.query(Concept_representations)
	for i in con_re:
		if i.representation == rep:
			x = i.concept_ncid

	con = db.session.query(Concept)
	for i in con:
		if i.ncid == x:
			ans = i.cid
	
	return ans

#------concept_representation get_all_representation
@app.route('/concept_representations/getar')
def concept_representations_getar():
	cid = "Adhaar"
	con_r = db.session.query(Concept)
	for i in con_r:
		if i.cid == cid:
			x = i.ncid

	ans = ''
	con_rep_r = db.session.query(Concept_representations)
	for i in con_rep_r:
		if i.concept_ncid == x:
			ans = ans + i.representation
			ans = ans + ', '
	
	return ans	

#------concept_representation get_all_representation_by_context
@app.route('/concept_representations/getarbc')
def concept_representations_getarbc():
	context = "physical unique ID proof"
	con_rep_r = db.session.query(Concept_representations)
	for i in con_rep_r:
		if i.context == context:
			x = i.concept_ncid

	ans = ''
	for i in con_rep_r:
		if i.concept_ncid == x:
			ans = ans + i.representation
			ans = ans + ', '
	
	return ans

#-----concept_representation end



@app.route('/getConcept_representations')
def concept_representations():
	concept_rep = db.session.query(Concept_representation) 
	con = concept_rep[2] 
	return "{}: {}: {}".format(con.representation, con.context, con.preferred_score)

@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == "POST":
		url = request.form['url']
		app.logger.debug('stored url: ' + url )
	return render_template('add.html')

if __name__ == "__main__":
	app.run(debug=True)







