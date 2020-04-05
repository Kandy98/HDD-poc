from base import base
from sqlalchemy import Column, String, Integer, Date, Sequence

#TABLE_ID = Sequence('table_id_seq', start=2)
class Concept(base):  
    __tablename__ = 'concept'

    ncid = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(String)
    concept_definition = Column(String)
    type = Column(Integer)
    status = Column(Integer)
    data_type = Column(Integer)
    vnd = Column(String)
    doud = Column(Date)

    def __init__(self, cid, concept_definition, type):
    	#self.ncid = ncid
    	self.cid = cid
    	self.concept_definition = concept_definition
    	self.type = type
        #self.status = status
        #self.data_type = data_type
        #self.vnd = vnd
        #self.doud = doud