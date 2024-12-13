Ethereum EIPs Ontology
======================

The Ethereum EIPs Ontology provides current AI systems with up-to-date knowledge of the Ethereum ecosystem via serialisation of key concepts from the Ethereum Improvement Proposals. It is supplemented with general Ethereum glossaries of terms for added context.

There are three key files in this repository:

* ethereum-glossary.txt, a glossary of Ethereum terms and their definitions.
* eip-ontology.txt, a simple _term: definition_ version of the ontology with some duplicate terms in plain text format. This version is intended for single-user interactions with an LLM user interface that supports file uploading.
* eip-ontology-skos.ttl, a more complete ontology in [SKOS](https://en.wikipedia.org/wiki/Simple_Knowledge_Organization_System) format. This version is intended for use in a graph database orchestrated with an LLM in production products or services. 

Why?
----
The Ethereum EIPs Ontology is necessary because popular LLMs often give very wrong answers about the Ethereum ecosystem. This is often due to the gap between their training data and the current date. LLMs will "hallucinate", or produce a response in the absence of knowledge on a subject.

The following two screenshots illustrate the problem. In those interactions, ChatGPT.com and Claude.ai gave incorrect answers to the question "What is FOCIL in Ethereum?". The correct answer should have been something like "Fork-choice enforced Inclusion Lists as proposed in [EIP-7805](https://eips.ethereum.org/EIPS/eip-7805)". These examples were taken on 10 December 2024.

![Wrong answer by ChatGPT.](images/ChatGPT-wrong-answer-20241210.png?raw=true)

![Wrong answer by Claude.](images/Claude-wrong-answer-20241210.png?raw=true)

We note that LLMs are upgrading their capabilities quickly. ChatGPT will already search the Web dynamically and can discover the correct answer. However, as shown, opportunities for error are still rife.

Usage
-----
The flat file ontology (eip-ontology.txt) is meant as dynamic input to generic Large Language Models to give them up-to-date context on Ethereum terms and definitions for single-user interactions.

The Ethereum glossary (ethereum-glossary.txt) may be used in conjunction with the onology if desired. In most cases, modern LLMs will already have time-delayed understanding of most of the terms in the glossary.

The screenshot below shows a simple interaction between a user and ChatGPT 4o (although any LLM that provides for file uploads may be used). In this example, one can see how easy it to upload the file and then prompt the LLM to provide correct, contextual information about current Ethereum concepts.

![Uploading the ontology to ChatGPT.](images/Upload-ontology-to-ChatGPT.png?raw=true)

![Getting the correct answer after using the ontology.](images/ChatGPT-correct-answer-20241210.png?raw=true)

A more full-featured version of the ontology (eip-ontology-skos.ttl) is useful in orchestrated systems using a graph database as a contraint on LLM inputs. It is shown below in the [Protege ontology editor](https://protege.stanford.edu) for reference. That file would be uploaded into a graph database for production systems.

This version of the ontology is intended for use in multi-person, production products or services.

![Screenshot of the ontology in Protege.](images/ontology_in_protege.png?raw=true)


Creation
--------
This repository combines the following sources into two formats: The first is a simple _term : definition (EIP number)_ format. That file (eip-ontology.txt) contains duplicated entries from the sources.

Sources:

1. The Ethereum Foundation's [Ethereum Glossary](https://ethereum.org/en/glossary/)
2. Consensys' [A Blockchain Glossary for Beginners](https://consensys.io/knowledge-base/a-blockchain-glossary-for-beginners)
3. The Ethereum Foundation's active [Ethereum Improvement Proposals (EIPs)](https://github.com/ethereum/EIPs/tree/master)

ChatGPT 4o is used to extract newly-created terms from the EIPs and add them sequentially to the text file until they are all represented.

A python script (mk_skos.py) is used to generate a de-duplicated and extended [SKOS](https://en.wikipedia.org/wiki/Simple_Knowledge_Organization_System) ontology. Where multiple definitions exist for the same term, both are kept using different predicates (skos:definition for the primary and rdfs:comment for the secondary). EIPs are linked via skos:broader where they are found.

The SKOS file parses cleanly into the [Protege ontology editor](https://protege.stanford.edu/) if hand editing or human review is desired. However, its intended purpose is to be uploaded into a graph database that supplements an LLM in an orchestrated system.

Prompt used to ChatGPT 4o
--------------------------------------

---

> Please summarise the newly-introduced terms defined in these documents. Add the EIP
> number without any hyperlinks to the end of the definition, enclosed in parentheses. Your
> output format should be "term : definition (EIP-number)".

> Use succinct terms. For example, when a new opcode is introduced, use the opcode
> name as the term.

> For example, if EIP 100000 defines the FOO opcode, then the term is FOO. If the
> definition was 'The FOO opcode prints "foo" when it is called' then your output should be:
> 'FOO: The FOO opcode prints "foo" when it is called. (EIP-100000)'
