"""
XML Parser
"""

# Imports
import json
import xml.etree.ElementTree as ET
from rdflib import Graph, Literal, URIRef
from rdflib.compare import graph_diff

# Main Functions
# XML Vars
BANKING_CLASSES = {
    "Branch": "http://webprotege.stanford.edu/RBl5y8zYcaCdGL3tKdrck4L",
    "GoldStorage": "http://webprotege.stanford.edu/R7zjqcAI6Y8bP3k6B0Y4EVK",
    "Manager": "http://webprotege.stanford.edu/R7H6oHgu21jWZYvhGBbW5Y9",
    "Cashier": "http://webprotege.stanford.edu/RDjFTJaA24w8BBjTUKe1MqO",
    "CustomerCare": "http://webprotege.stanford.edu/RCO0O51gy2TN7APskvYJt4D",
    "Security": "http://webprotege.stanford.edu/RBURugVHBoEYWdPAhvbbaSH",
    "Technician": "http://webprotege.stanford.edu/RDIC5vfXXOHbR2Y4fNUD93E",
    "Teller": "http://webprotege.stanford.edu/R9GNYir55KhUrecWPNcLY7i",
    "Borrower": "http://webprotege.stanford.edu/RCg3840rAGL3ScNqrxMjwhK",
    "Depositor": "http://webprotege.stanford.edu/R7UYSurF8olG4I7qbEGX6ey",
    "Deposit": "http://webprotege.stanford.edu/RCJYCjAImEkxH9sfqnAW5DC",
    "VehicleLoan": "urn:webprotege:ontology:f8af5f74-014c-411c-bb58-0e885c2d99a4#VehicleLoan",
    "Payment": "http://webprotege.stanford.edu/RC9M2hdfx4Wm9hPoDFqXh9P",
    "PaymentNumber": "http://webprotege.stanford.edu/R94q7B8QaYMsKrmDN6a0r59",
    "Transaction": "http://webprotege.stanford.edu/R9E9oMSk1WDyJWwWqe0IMLU",
    "Withdrawal": "http://webprotege.stanford.edu/R43HI7MepwAxTshb7MCxOk",
    "ATM": "http://webprotege.stanford.edu/R9hFqoDxO5i1Mwiu9nv6dut",
    "Cheque": "http://webprotege.stanford.edu/RDqkpew5LixolaWc7CIixUd",
    "Cash": "http://webprotege.stanford.edu/RDaPa87Fi2RPD9TeS51ZdjU",
    "Redressal": "http://webprotege.stanford.edu/RDuPkZ0b8iyErNnyUskrNVg",
    "LoanAccount": "http://webprotege.stanford.edu/R8Y9qtpECqAs5ILBlkL8MXU"
}
# XML Functions
def XML_Load(path):
    '''
    Loads the XML file from the given path
    '''
    tree = ET.parse(path)
    root = tree.getroot()
    return root

def XML_Save(root, path):
    '''
    Saves the XML file to the given path
    '''
    tree = ET.ElementTree(root)
    tree.write(path)

def BankingXML_Parse(root):
    '''
    Parses the XML file to a list of transactions
    '''
    # Init
    Data = {c: [] for c in BANKING_CLASSES.keys()}
    # Load
    for c in BANKING_CLASSES.keys():
        for child in root.findall(".//" + c):
            # Get Data
            indivData = {
                "text": child.text,
                "attributes": child.attrib
            }
            Data[c].append(indivData)
    # print(json.dumps(Data, indent=4))

    return Data

# RDF Vars
NAMESPACE = "http://www.semanticweb.org/cseka/ontologies/2022/3/banking"
NAMED_INDIV = URIRef('http://www.w3.org/2002/07/owl#NamedIndividual')
RDF_URIs = {
    "type": URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
}
# RDF Functions
def getIndivURI(name):
    name = name.replace(" ", "_")
    return URIRef(NAMESPACE + "#" + name)

def BankingRDF_SetTriples(path, xml_data, RDF_GRAPH=None):
    '''
    Set the triples for the banking data
    '''
    # Init Graph
    if RDF_GRAPH is None: RDF_GRAPH = Graph()
    TRIPLES = []
    # RDF_GRAPH.load(path, format='xml')

    # Set Triples
    for c in BANKING_CLASSES:
        # CLASS_INDIV = getIndivURI(c)
        CLASS_INDIV = URIRef(BANKING_CLASSES[c])
        for i in range(len(xml_data[c])):
            indivData = xml_data[c][i]
            attributes = indivData["attributes"]
            ID = attributes["id"]
            Text = indivData["text"]
            # Set Individual
            indiv = getIndivURI(ID)
            TRIPLES.append((indiv, RDF_URIs["type"], CLASS_INDIV))
            # TRIPLES.append((indiv, RDF_URIs["type"], NAMED_INDIV))
            # Set Attributes
            for a in attributes:
                if(not a in ["id"]):
                    attr_indiv = getIndivURI(attributes[a])
                    TRIPLES.append((indiv, getIndivURI(a), attr_indiv))
            # Set Text
            TRIPLES.append((indiv, getIndivURI("text"), Literal(Text)))

    # print(TRIPLES)
    
    # Save
    for t in TRIPLES: RDF_GRAPH.add(t)
    RDF_GRAPH.serialize(destination=path, format="xml")

def RDF_Save(RDF_GRAPH, path):
    '''
    Save the RDF Graph to the given path
    '''
    RDF_GRAPH.serialize(destination=path, format="xml")