import os,json
import requests
		
import spacy
def check_sentance(user_message):
	# Load the English NER model provided by spaCy
	nlp = spacy.load("en_core_web_sm")

	# Function to get all named entities from the sentence
	def get_named_entities(sentence):
		doc = nlp(sentence)
		named_entities = {}
		for ent in doc.ents:
			named_entities[ent.label_] = ent.text
		return named_entities

	# Example sentence
	# sentence = "CBDC status in India"

	# Get all named entities from the sentence
	entities = get_named_entities(user_message)
	print(entities)
	return entities
	# Check if any named entities are detected
	


# check_sentance('Query Central Bank Digital Currencies')


