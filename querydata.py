# coding=utf-8

# 1 - imports
from base import Session
from concept_representation import Concept_representation
from concept import Concept

# 2 - extract a session
session = Session()

# 3 - extract all movies
concepts = session.query(Concept).all()

# 4 - print movies' details
print('\n### All concepts:')
for con in concepts:
    print('{con.id} has definition {con.concept_definition}')
print('')