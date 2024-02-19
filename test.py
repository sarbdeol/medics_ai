import re

# Given text
text = "### [Click here for more details](https://www.monito.com/en/compare/transfer)"

# Regular expression pattern to match the HTML anchor tag
anchor_pattern = r'\[([^\[\]]+)\]\((https?://[^)]+)\)'

# Find the anchor tag in the given text
anchor_match = re.search(anchor_pattern, text)

# If an anchor tag is found, extract and print it
if anchor_match:
    anchor_text = anchor_match.group(1)
    anchor_link = anchor_match.group(2)
    html_anchor_tag = f'<a href="{anchor_link}">{anchor_text}</a>'
    print("Extracted HTML anchor tag:", html_anchor_tag)
else:
    print("No HTML anchor tag found in the given text.")
