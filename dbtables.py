#from base import base
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
#from thermos import app, db
app = Flask(__name__)
app.secret_key = 'meow'
app.config['SECRET KEY'] = '~t\x17\x9f\x825\x91\xa1M\x86\xd1j)1\x80%3T\xb9\xae\x80\xe9\x1fW\xf7\x04'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/hdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Concept_type(db.Model):
    __tablename__ = 'concept_type'

    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))


class Concept_status(db.Model):
    __tablename__ = 'concept_status'

    status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))

concept_representation = db.Table('concept_representation',
        db.Column('concept_id', db.Integer, db.ForeignKey('concept.ncid')),
        db.Column('representation_id', db.Integer, db.ForeignKey('representation.representation_id'))
    )

class Concept(db.Model):  
    __tablename__ = 'concept'

    ncid = db.Column(db.Integer, primary_key=True)

    cid = db.Column(db.String(100))
    definition = db.Column(db.String(1000))
    type = db.Column(db.Integer)
    status = db.Column(db.Integer)
    vnd = db.Column(db.String(8))
    doud = db.Column(db.Date)
    representations = db.relationship("Representation", secondary=concept_representation, backref='concepts', lazy='dynamic')

    def json(self):
        return {'concept_id' : self.ncid, 'identifier' : self.cid, 'definition' : self.definition, 'type' : self.type, 'status' : self.status, 'version' : self.vnd, 'date of last update' : self.doud }

    def reps():
        return {'representation_id' : self.representation_id, 'definition' : self.definition}

    def add_concept(self):
        db.session.add(self)
        db.session.commit()

    def get_concept(self, id):
        return Concept.json(Concept.query.filter_by(ncid=id).first())

    def get_all_concept(self):
        return [Concept.json(co) for co in Concept.query.all()]

    def update_concept(self, id, ci, c_d, t, sta, vn):
        con = Concept.query.filter_by(ncid=id).first()

        if ci != "-":
            con.cid = ci
        if c_d != "-":
          con.definition = c_d
        if t != "-":
          con.type = t
        if sta != "-":
          con.status = sta
        if vn != "-":
            con.vnd = vn
        con.date = datetime.utcnow()
        db.session.commit()

        return Concept.json(Concept.query.filter_by(ncid=id).first())

    def delete_concept(self, id):
        con = Concept.query.filter_by(ncid=id).delete()
        db.session.commit()

    def getConceptByName(self, ci):
        return Concept.json(Concept.query.filter_by(cid=ci).first())

    def getRepresentationsByConcept(self, id):
        con = db.session.query(Concept).filter_by(ncid=id).first()
        data = []
        for i in con.representations:
          rep = i.representation_id
          repser = db.session.query(Representation).filter_by(representation_id=rep).first()
          #return repser.definition
          data.append(repser)
        return [Representation.json(di) for di in data]

    def __repr__(self):
        concept_object = {
            'ncid' : self.ncid,
            'cid' : self.cid,
            'concept_definition' : self. definition,
            'type' : self.type,
            'status' : self. status,
            'data_type' : self.data_type,
            'data_size' : self.data_size,
            'vnd' : self.vnd,
            'doud' : self.doud  
        }
        return json.dumps(concept_object)

# class Concept_representation(db.Model):  
#     __tablename__ = 'concept_representation'

#     concept_representation_id = db.Column(db.Integer, primary_key=True)
#     concept_ncid = db.Column(db.Integer)
#     representation_id = db.Column(db.Integer)

class Representation(db.Model):
    __tablename__ = 'representation'

    representation_id = db.Column(db.Integer, primary_key=True)
    representation_cid = db.Column(db.String(100))
    definition = db.Column(db.String(1000))
    vnd = db.Column(db.String(8))
    doud = db.Column(db.Date)

    def json(self):
        return {'representation_id' : self.representation_id, 'name' : self.representation_cid, 'definition' : self.definition, 'version' : self.vnd, 'date of last update' : self.doud}

    def add_representation(self):
        db.session.add(self)
        db.session.commit()

    def get_representation(self, id):
        return Representation.json(Representation.query.filter_by(representation_id=id).first())

    def update_representation(self, id, ci, d, vn):
        con = Representation.query.filter_by(representation_id=id).first()

        if ci != "-":
            con.cid = ci
        if d != "-":
          con.definition = d
        if vn != "-":
            con.vnd = vn
        con.doud = datetime.utcnow()
        db.session.commit()

        return Concept.json(Representation.query.filter_by(representation_id=id).first())


class Concept_relation(db.Model):
    __tablename__ = 'concept_relation'

    concept_relation_id = db.Column(db.Integer, primary_key=True)
    concept_relation_ncid = db.Column(db.Integer)
    concept_ncid = db.Column(db.Integer)
    relationship_ncid = db.Column(db.Integer)

    def __init__(self, concept_relation_ncid, concept_ncid, relationship_ncid):
        self.concept_relation_ncid = concept_relation_ncid
        self.concept_ncid = concept_ncid
        self.relationship_ncid = relationship_ncid

class Relationship(db.Model):
    __tablename__ = 'relationship'

    relationship_ncid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __intit__(self, name, description):
        self.name = name
        self.description = description

class Representation_context(db.Model):
    __tablename__ = 'representation_context'

    representation_context_id = db.Column(db.Integer, primary_key=True)
    representation_id = db.Column(db.Integer)
    context_id = db.Column(db.Integer)
    preferred_score = db.Column(db.Integer)

    def __init__(self, representation_id, context_id, preferred_score):
        self.representation_id = representation_id
        self.context_id = context_id
        self.preferred_score = preferred_score

class Context(db.Model):
    __tablename__ = 'context'

    relation_id = db.Column(db.Integer, primary_key=True)
    concept_ncid = db.Column(db.Integer)
    relation_type = db.Column(db.Integer)
    concept_relation_ncid = db.Column(db.Integer)

    def __init__(self, ncid, relation_type, concept_relation_ncid):
        self.concept_ncid = concept_ncid
        self.relation_type = relation_type
        self.concept_relation_ncid = concept_relation_ncid 


