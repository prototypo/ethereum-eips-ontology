from rdflib import Graph, Namespace, Literal, RDF, RDFS, URIRef
from rdflib.namespace import SKOS
from urllib.parse import quote  # For URL-escaping
import logging
import os
import re
import sys

# Import shared functions
sys.path.append(os.path.dirname(sys.path[0]))
DHWBinDir='/Users/davidhyland-wood/bin'
sys.path.insert(1, DHWBinDir)
from ethOntologyUtilities import *

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

# Config
script = "mk_skos.py"
ontology_file = "eip-ontology.txt"
OntologyDir='/Users/davidhyland-wood/Documents/GitHub/ethereum-eips-ontology'
ontology_path = os.path.join(OntologyDir, ontology_file)
term_eips_relationships_file = 'eip-ontology-terms-EIP-relationships.txt'
term_eips_relationships = {}
LogFileDir ='/Users/davidhyland-wood/Desktop'

# Logger
logger = logging.getLogger()
log_file = os.path.join(LogFileDir, "mk_skos.log")

term_eips_relationships = {}

# Function to create SKOS concepts and their relations
def create_skos_concept(normterm, term_escaped, definition):

	global g
	global term_eips_relationships
	
	logger.debug(f"In create_skos_concept():")
	logger.debug(f"\tTerm-EIP mapping: {term_eips_relationships}")
	
	# Create a concept URIRef with the escaped term
	concept = URIRef(base_iri + term_escaped)
	
	# Add triples for the concept, its label, and definition
	g.add((concept, RDF.type, SKOS.Concept))
	g.add((concept, SKOS.prefLabel, Literal(normterm)))
	g.add((concept, SKOS.definition, Literal(definition)))

	# Look for EIP related to this term and create links if found
	# DBG
	logger.debug(f"Evaluating *{normterm}*:")
		
	if normterm in term_eips_relationships:
		for eip in term_eips_relationships[normterm]:
			eip_lower = eip.lower()
			eip_url = 'https://github.com/ethereum/EIPs/blob/master/EIPS/' + eip_lower + '.md'
			g.add((concept, SKOS.broader, URIRef(eip_url)))
			logger.debug(f"\tAdded '{eip_url}'")
	else:
		logger.debug(f"\tTerm {normterm} has no related EIPs")

	return concept
	

def main():

	global term_eips_relationships
	
	establish_logger(logger, log_file)	# Configure logging details
	date = datetime.now()
	
	logger.info(f"-----------------------------------------")
	logger.info(f"{script}: Started run at {datetime.now()}")
	logger.info(f"-----------------------------------------")
	

	# Keep track of terms seen
	terms = {}
	
	# Get a mapping of terms to EIPs
	term_eips_relationships = read_term_eips_relationships(OntologyDir, term_eips_relationships_file) # a dict
	
	# DBG
	logger.debug(f"Term-EIP mapping: {term_eips_relationships}")
	
	# Parse the ontology file
	with open(ontology_path, 'r') as file:
		lines = file.readlines()

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
	os.chdir(OntologyDir)
	output_file = "eip-ontology-skos.ttl"
	try:
		g.serialize(destination=output_file, format="turtle")
		# DBG
		print(f"SKOS vocabulary has been saved as '{output_file}'.")
		exit(0)
	except Exception as e:
		exit(1)

if __name__ == "__main__":
	main()

