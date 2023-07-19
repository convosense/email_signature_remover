## Importing dependencies:
# 1. email_reply_parser by zapier
# !pip install email_reply_parser
from email_reply_parser import EmailReplyParser


# 2. NLTK to tokenize the sentences

import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('punkt')
nltk.download('words')

from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

# 3. spaCy for NER in last sentence 
import spacy
nlp = spacy.load("en_core_web_sm")


# 4. ReGex to identify thank you keywords:

import re

"""## 0. Function for removing linespaces"""

def remove_newline(latest_reply):
  pattern = re.compile(r'\n{3,}')
  result = pattern.sub('\n\n', latest_reply)

  return result


"""## 1. Function for parsing the latest reply from email:"""

def parse_latest_reply(email_message):
  reply = EmailReplyParser.parse_reply(str(email_message))
  return reply


"""## Function for checking if the email starts with a special chr like a dash:"""

def check_email_starts_with_special_char(s):
    # Match any number of newline characters at the beginning of the string
    newline_regex = r"^\n*"
    newline_match = re.match(newline_regex, s)
    
    # Get the substring after the newline characters
    if newline_match:
        s = s[newline_match.end():]
    
    # Check if the substring has a special character at the beginning
    special_regex = r"^[^\w\s]+"
    special_match = re.match(special_regex, s)
    
    return special_match is not None


"""## 2. ReGex to remove the line if it contains anything inside angled braces:"""

def strip_lines_with_angles_and_newline(text):
    # Define the regular expression pattern to match lines containing angled brackets or square brackets and a newline character
    pattern = r'[\r\n]*'      # Match optional leading line breaks
    pattern += r'[<[].*?[>\]]' # Match angled or square brackets with any characters inside
    pattern += r'[\r\n]*'      # Match optional trailing line breaks
    
    # Use the re.MULTILINE flag to match the start and end of each line
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    
    # Loop through each match and remove the entire line containing the match
    for match in matches:
        text = re.sub(f'[\r\n]*{re.escape(match)}', '', text, flags=re.MULTILINE)
        
    return text


"""## 3. NLTK-spaCy combo function to remove signature:"""

# Combination of NLTK and spaCy:
# using nltk for sentence tokenization, and spaCy for word tokenization(NER in last sentence)

def nltk_remove_signature(email_text):
    # tokenize the email text into sentences
    sents = sent_tokenize(email_text)
    
    # check if the list of sentences is not empty
    if len(sents) > 0:
        last_sent = sents[-1]  # get the last sentence
        
        # use spaCy to parse the last sentence
        doc = nlp(last_sent)
        
        # check if the last sentence contains a named entity of type "PERSON"
        if any(ent.label_ == "PERSON" for ent in doc.ents):
            # remove the last sentence from the email
            email_text = email_text[:email_text.rfind(last_sent)]
    
    return email_text


"""## 4. ReGex function to identify thank-you keywords and strip everything after that:"""

def regex_ty_strip(text):
  signature_regex = r"(thank\s+you|sincerely|Regards,|Thank you,|CONFIDENTIALITY AND WARNING NOTICE:|best|regards|Best Regards|Happy holidays|thanks|kind\s+regards|many\s+thanks|warm\s+regards|cheers|thanks\s+again|thanks\s+and\s+regards)\s*,?\s*\n{1,2}"
  match = re.search(signature_regex, text, re.IGNORECASE)
  if match:
    text = text[:match.start()]

  return text



"""## Making a one-for-all function:"""

def remove_sign(email_message):
  if check_email_starts_with_special_char(email_message) == 0:
    # indentation  
    latest_reply = parse_latest_reply(email_message)

    sentences = nltk.sent_tokenize(latest_reply)
    length = len(sentences)

    # use nltk only if the length of sentences in the email is >1:
    if length > 1:

      # 1:
      angled_braces_removed = strip_lines_with_angles_and_newline(latest_reply)

      # 2:
      nltk_sign = nltk_remove_signature(angled_braces_removed)

      # use regex to remove any thank-you keywords followed by 1 or 2 newline characters, if any left:
      remove_ty = regex_ty_strip(nltk_sign)

      # Check if the string to be returned is not null:
      if len(remove_ty)!=0:
        return remove_newline(remove_ty)
      else:
        if len(nltk_sign)!=0:
          return remove_newline(nltk_sign)
        else:
          return remove_newline(angled_braces_removed)

    elif email_message == 'nan':
      return remove_newline(email_message)

    # if the email is only one-sentenced, then it means that it doesn't contain signature, so return the same latest email:
    else:
      return remove_newline(latest_reply)

  else:
    return remove_newline(email_message)