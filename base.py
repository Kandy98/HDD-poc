# from sqlalchemy import create_engine  
# from sqlalchemy import Column, String, Integer 
# from sqlalchemy.ext.declarative import declarative_base  
# from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLALchemy

db_string = 'postgresql://garimendra:topcoderkandy@localhost:5432/HDD'

db = create_engine(db_string)  
base = declarative_base()

Session = sessionmaker(db)  
session = Session()
base.metadata.create_all(db)