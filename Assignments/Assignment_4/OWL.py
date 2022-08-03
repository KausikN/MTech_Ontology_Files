"""
OWL API

API: https://pypi.org/project/Owlready2/
"""

# Imports
import owlready2 as owl

# Main Functions
# OWL Functions
def OWL_CreateWorld():
    '''
    Creates a new world
    '''
    return owl.World()

def OWL_Load(path, world):
    '''
    Loads the ontology from the given path
    '''
    onto = world.get_ontology(path).load()
    return onto

def OWL_Save(onto, path):
    '''
    Saves the ontology to the given path
    '''
    onto.save(path)

def OWL_Reasoner(world):
    '''
    Runs Hermit reasoner for the ontology
    '''
    owl.sync_reasoner(world)