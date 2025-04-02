from rdflib import Graph, Namespace, Literal, RDF, RDFS, URIRef
from rdflib.namespace import SKOS
from urllib.parse import quote  # For URL-escaping
import re

# Base IRI for the SKOS vocabulary
base_iri = "http://www.consensys.net/ethereum-skos#"

# Create a new RDF graph
g = Graph()

# Define the SKOS namespace and Ethereum namespace
EX = Namespace(base_iri)

# Bind namespaces
g.bind("skos", SKOS)
g.bind("rdfs", RDFS)
g.bind("ex", EX)

# Read the ontology file
ontology_file = "eip-ontology.txt"

# Keep track of terms seen
terms = {}

# Parsing the ontology file
with open(ontology_file, 'r') as file:
    lines = file.readlines()

# Function to create SKOS concepts and their relations
def create_skos_concept(normterm, term_escaped, definition):
    
    # Create a concept URIRef with the escaped term
    concept = URIRef(base_iri + term_escaped)
    
    # Add triples for the concept, its label, and definition
    g.add((concept, RDF.type, SKOS.Concept))
    g.add((concept, SKOS.prefLabel, Literal(normterm)))
    g.add((concept, SKOS.definition, Literal(definition)))

    # Look for EIP numbers in definitions and create links if found
    p = re.compile(r"\(EIP-\d*\)")
    m = p.search(definition)
    if m:
        eip = m.group().lower().lstrip('(').rstrip(')')
        eip_url = 'https://github.com/ethereum/EIPs/blob/master/EIPS/' + eip + '.md'
        g.add((concept, SKOS.broader, URIRef(eip_url)))
        #print(f"Added '{eip_url}'")

    return concept

# Process each line in the ontology
for line in lines:

    if ( len(line) > 5 ):
      # Split the line into term and definition
      term, definition = line.strip().split(":", 1)

      # Normalise term's case
      normterm = term.title()
      # URL-escape the term for safe usage in the URI
      term_escaped = quote(normterm.strip())

      if ( term_escaped not in terms ):

        # Create a SKOS concept for the term
        concept = create_skos_concept(normterm, term_escaped, definition.strip())

        # Keep track of terms seen
        newterm = {term_escaped : concept}
        terms.update(newterm)
      else:
        # Add the definition to the previously-seen term's concept
        concept = terms.get(term_escaped)
        g.add((concept, RDFS.comment, Literal(definition)))
    
    else:
      # Found a non-matching line
      next

# Save the SKOS vocabulary to a file
output_file = "eip-ontology-skos.ttl"
try:
	g.serialize(destination=output_file, format="turtle")
	exit(0)
except:
	exit(1)

#print(f"SKOS vocabulary has been created and saved as '{output_file}'.")

