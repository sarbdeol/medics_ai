import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import pycountry
def check_sentance(sentence):


	# Tokenize the sentence
	tokens = word_tokenize(sentence)

	# Perform part-of-speech tagging
	tagged_tokens = pos_tag(tokens)

	# Extract nouns and proper nouns
	keywords = [word for word, pos in tagged_tokens if pos in ['NN', 'NNS', 'NNP', 'NNPS']]

	# Check if any keyword is a country
	for keyword in keywords:
		try:
			country = pycountry.countries.lookup(keyword)
			print("Country:", country.name)
			return {'country': country.name}
		except LookupError:
			return {'country':''}
# check_sentance('india')