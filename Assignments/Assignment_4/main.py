"""
Main file for Ontology Assignment 4
"""

# Imports
import argparse

from XMLParse import *
from OWL import *

# Main Functions
def Convert_OWL2RDF(world):
    '''
    Converts the ontology to RDF
    '''
    return world.as_rdflib_graph()

def Compare_Triples(paths):
    '''
    Compares the triples in the given paths
    '''
    # Load RDF Triples
    WORLDS = {
        "ext": OWL_CreateWorld(),
        "ext-ref": OWL_CreateWorld(),
        "inf": OWL_CreateWorld()
    }
    OWL_Load(paths["ext"], WORLDS["ext"])
    OWL_Load(paths["ext"], WORLDS["ext-ref"])
    OWL_Load(paths["ref"], WORLDS["ext-ref"])
    OWL_Load(paths["inf"], WORLDS["inf"])
    # Convert to RDF
    GRAPHS = {
        "ext": Convert_OWL2RDF(WORLDS["ext"]),
        "ext-ref": Convert_OWL2RDF(WORLDS["ext-ref"]),
        "inf": Convert_OWL2RDF(WORLDS["inf"])
    }
    # Compare
    diff = graph_diff(GRAPHS["ext-ref"], GRAPHS["inf"])
    # Save
    RDF_Save(diff[2], paths["out_inf_rdf"])
    diff[2].print(out=open(paths["out_inf"], "w"))
    GRAPHS["ext"].print(out=open(paths["out_ext"], "w"))

# Main Function
def main(args):
    '''
    Main Function
    '''
    # Load Args
    XML_LOAD_PATH = args.xml
    ONTOLOGY_LOAD_PATH = args.ontology
    OUTPUT_DIR = args.output
    RDF_SAVE_PATH = f"{OUTPUT_DIR}/RDF_Extracted.owl"
    RDF_INFERRED_SAVE_PATH = f"{OUTPUT_DIR}/RDF_Inferred.owl"
    RDF_REASONED_SAVE_PATH = f"{OUTPUT_DIR}/RDF_Final.owl"
    EXTRACTED_TRIPLES_SAVE_PATH = f"{OUTPUT_DIR}/extracted_triples.txt"
    INFERRED_TRIPLES_SAVE_PATH = f"{OUTPUT_DIR}/inferred_triples.txt"

    # Create World
    WORLD = OWL_CreateWorld()
    # Load Reference Ontology
    REFERENCE_ONTO = OWL_Load(ONTOLOGY_LOAD_PATH, WORLD)

    # Load XML
    root = XML_Load(XML_LOAD_PATH)
    # Parse XML
    DATA = BankingXML_Parse(root)
    # Convert to Triples and Save RDF
    BankingRDF_SetTriples(RDF_SAVE_PATH, DATA)
    # Load Triples Ontology
    ONTO = OWL_Load(RDF_SAVE_PATH, WORLD)

    # Run Reasoner
    print("Reasoning...")
    OWL_Reasoner(WORLD)
    print()

    # Convert to RDF Graph
    RDF_GRAPH = Convert_OWL2RDF(WORLD)
    # Save RDF Graph
    RDF_Save(RDF_GRAPH, RDF_REASONED_SAVE_PATH)

    # Compare
    paths = {
        "ext": RDF_SAVE_PATH,
        "ref": ONTOLOGY_LOAD_PATH,
        "inf": RDF_REASONED_SAVE_PATH,
        "out_ext": EXTRACTED_TRIPLES_SAVE_PATH,
        "out_inf": INFERRED_TRIPLES_SAVE_PATH,
        "out_inf_rdf": RDF_INFERRED_SAVE_PATH
    }
    Compare_Triples(paths)
    # Display
    print("Extracted Triples:")
    print(open(EXTRACTED_TRIPLES_SAVE_PATH, "r").read())
    print()
    print("Inferred Triples:")
    print(open(INFERRED_TRIPLES_SAVE_PATH, "r").read())
    print()

# Run
if __name__ == "__main__":
    # Parse Arguments
    parser = argparse.ArgumentParser(description="Ontology Assignment 4")
    parser.add_argument("-x", "--xml", help="Input XML File", default="Data/Banking_Data.xml")
    parser.add_argument("-on", "--ontology", help="Input Ontology File", default="Data/Banking_Ontology.owx")
    parser.add_argument("-o", "--output", help="Output Save Dir", default="Output")
    args = parser.parse_args()
    # Run
    main(args)