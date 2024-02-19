import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import requests
from google_bard_api import user_msg
def get_bitcoin_price(stock):
    # Define the API endpoint
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={stock}&vs_currencies=usd"
    
    try:
        # Send a GET request to the API
        response = requests.get(url)
        # Parse the JSON response
        data = response.json()
        # Extract the price of the specified cryptocurrency
        price = data.get(stock, {}).get('usd')
        return price
    except Exception as e:
        print(f"Error fetching {stock} price:", e)
        return None

def extract_entities(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Perform Part-of-Speech tagging
    pos_tags = pos_tag(tokens)
    # Perform Named Entity Recognition (NER)
    named_entities = ne_chunk(pos_tags)
    # Extract named entities
    entities = []
    for entity in named_entities:
        if isinstance(entity, nltk.Tree):
            entities.append(" ".join([word for word, tag in entity.leaves()]))
    return entities

# Example usage
text = "stock price of tesla and bitcoin"
entities = extract_entities(text)
print("Entities:", entities)

# Fetch prices for each entity
for entity in entities:
    price = get_bitcoin_price(entity.lower())
    if price is not None:
        print(f"The current price of {entity.capitalize()} is ${price}")
    else:
        print(f"Failed to retrieve the price for {entity.capitalize()}.")













# def _get_chatgpt_response(self, prompt):
#         ICP = self.env['ir.config_parameter'].sudo()
#         api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
#         gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
#         gpt_model = 'gpt-3.5-turbo'
#         try:
#             if gpt_model_id:
#                 gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
#         except Exception as ex:
#             gpt_model = 'gpt-3.5-turbo'
#             pass
#         try: 
#             client = OpenAI(api_key=api_key)
#             completion = client.chat.completions.create(
#                 model=gpt_model,
#                 messages=[
#                 {"role": "system", "content": "You are a helpful Medical Advisor."},
#                 {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.6,
#                 max_tokens=3000,
#                 top_p=1,
#                 frequency_penalty=0,
#                 presence_penalty=0,
#                 user = self.env.user.name,
#             )
#             res = completion.choices[0].message.content
#             return res
#         except Exception as e:
#             raise UserError(_(e))