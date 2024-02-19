import requests
from bs4 import BeautifulSoup
import json

def get_bitcoin_price():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        price_element = soup.find("span", class_="sc-f70bb44c-0 jxpCgO base-text")
        if price_element:
            bitcoin_price = price_element.get_text(strip=True)
            print(bitcoin_price)
            return bitcoin_price
        else:
            print("Bitcoin price not found on the webpage.")
            return None
    else:
        print("Failed to fetch webpage data.")
        return None

def gpt(input_text):
    url = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "max_tokens": 2000,
        "messages": [{"role": "system",
                      "content": f"You are an analysis tool named Rudex. Provide info to the user based on current updates"},
                     {"role": "user",
                      "content": input_text}]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }
    response = requests.post(url, headers=headers, data=payload)
    output = json.loads(response.text)
    output = output['choices'][0]['message']['content']
    return output

if __name__ == "__main__":
    user_message = input("Enter your message: ")
    if "bitcoin price" in user_message.lower():
        bitcoin_price = get_bitcoin_price()
        if bitcoin_price:
            input_text = f"The current price of Bitcoin is {bitcoin_price}."
            gpt_output = gpt(input_text)
            print("GPT Output:", gpt_output)
        else:
            print("Failed to retrieve the Bitcoin price.")
    else:
        print("User is not asking for the Bitcoin price.")
