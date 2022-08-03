CS6852 Ontology Assignment 4

By,
N Kausik
CS21M037

To install required dependencies run,
   pip install -r requirements.txt

Command to run,
   python main.py -x <XML Filepath> -on <Ontology Filepath> -o <Output Dir>

Code Files,
 - main.py
    - Main file for the program
    - Runs the program with the given xml and ontology file and saves outputs in the given output directory
 - XMLParse.py
    - Functions for parsing the XML file and getting the list of triples
 - OWL.py
    - Functions for loading the Ontology and Reasoning

Input Files,
 - XML File (Updated from Assignment 2)
    - Path: Data/Banking_Data.xml
 - Ontology File (Asssignment 3)
    - Path: Data/Banking_Ontology.owx

Output Files,
 - Extracted RDF OWL
    - Path: Output/RDF_Extracted.owl
    - Extracted RDF triples in XML format
 - Inferred RDF OWL
    - Path: Output/RDF_Inferred.owl
    - Inferred RDF triples in XML format
 - Final Reasoned RDF OWL
    - Path: Output/RDF_Final.owl
    - Combined Extracted and Inferred (Reasoned) RDF triples in XML format
 - Extracted Triples
    - Path: Output/extracted_triples.txt
    - Extracted RDF triples in text format
 - Inferred Triples
    - Path: Output/inferred_triples.txt
    - Inferred RDF triples in text format