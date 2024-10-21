Ethereum EIPs Ontology
======================

Usage
-----
The basic vocabulary (glossary.txt) is meant as dynamic input to generic Large Language Models to give them up-to-date context on Ethereum terms and definitions.

The generated ontology (ethereum_skos.ttl) is a more full-featured variant useful in orchestrated systems using a graph database.

![Screenshot of an example interaction.](https://github.com/prototypo/ethereum-eips-ontology/blob/main/images/example-interaction.png?raw=true&token=GHSAT0AAAAAACYBPZR4CN4JMSQNKPBSI5G6ZYVUIWQ)

Creation
--------
This repository combines the following sources into a single clean text file in _term : definition_ format. That file (glossary.txt) contains duplicated entries from the sources.

Sources:

1. The Ethereum Foundation's [Ethereum Glossary](https://ethereum.org/en/glossary/)
2. Consensys' [A Blockchain Glossary for Beginners](https://consensys.io/knowledge-base/a-blockchain-glossary-for-beginners)
3. The Ethereum Foundation's active [Ethereum Improvement Proposals (EIPs)](https://github.com/ethereum/EIPs/tree/master)

ChatGPT 4o (Enterprise edition) was used to extract newly-created terms from the EIPs and add them sequentially to the text file until they are all represented.

A python script (mk_skos.py) is used to generate a de-duplicated [SKOS](https://en.wikipedia.org/wiki/Simple_Knowledge_Organization_System) ontology. Where multiple definitions exist for the same term, both are kept both using different predicates (skos:definition for the primary and rdfs:comment for the secondary). EIPs are linked via skos:broader where they are found.

The SKOS file parses cleanly into the [Protege ontology editor](https://protege.stanford.edu/).

Prompt used to ChatGPT 4o Enterprise
------------------------------------

---

> Please summarise the newly-introduced terms defined in these documents.
> Add the EIP number without any hyperlinks to the end of the definition,
> enclosed in parentheses. Your output format should be "term : definition (EIP number)" 
> 
> Use succinct terms. For example, when a new opcode is introduced, use the opcode name
> as the term.
