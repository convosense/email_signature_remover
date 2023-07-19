# Email Signature Remover

This repository contains a Python script to remove email signatures from the body of an email. The code is designed to extract the email body to obtain accurate sentiment and entity results for Natural Language Processing (NLP) tasks, like ***sentiment analysis*** and ***email categorization/classification***.

Thank-you keywords (like regards, kind regards, sincerely, thank you, etc) can play a significant role in determining the sentiment analysis of an email text. If not erased from the email text, an email in which the sender is angry(negative sentiment) may be evaluated as neutral(neutral sentiment) due to the auto-generated email signature which contained thank-you keywords. Also, the signature most often contains the sender's name and designation, which may affect the evaluation of the sentiment of email. So, in order to obtain accurate sentiment, removal of the signature from the email is essential.


## Dependencies to be installed

Before running the script, ensure you have the following dependencies installed in your environment:

1. [email_reply_parser](https://github.com/zapier/email-reply-parser): Email Reply Parser makes it easy to grab *only* the last reply to an on-going email thread. So, this script will work even if the text contains nested emails (often when the emails are scraped from a website using Web Scraping).

   ```bash
   pip install email_reply_parser
   ```

2. [NLTK (Natural Language Toolkit)](https://www.nltk.org/): Used for tokenizing sentences and parts-of-speech tagging.

   ```bash
   pip install nltk
   ```

3. [spaCy](https://spacy.io/): Used for Named Entity Recognition (NER) in the last sentence of the email.

   ```bash
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

4. [re (Regular expression operations)](https://docs.python.org/3/library/re.html): The built-in Python module for regular expressions, used for pattern matching and text processing.

   (No need to install separately, re is included in the Python standard library)


## Functions

The script contains several functions to remove email signatures step-by-step:

1. **`remove_newline(latest_reply)`**: Removes excessive line spaces from the email.

2. **`parse_latest_reply(email_message)`**: Parses the latest reply from the email using `email_reply_parser`.

3. **`check_email_starts_with_special_char(s)`**: Checks if the email starts with a special character (e.g., a dash).

4. **`strip_lines_with_angles_and_newline(text)`**: Removes lines that contain anything inside angled braces `< >` and any newline characters.

5. **`nltk_remove_signature(email_text)`**: Uses NLTK for sentence tokenization and spaCy for word tokenization (NER in the last sentence) to remove the signature from the email.

6. **`regex_ty_strip(text)`**: Uses regex to identify thank-you keywords and strip everything after them.

7. **`remove_sign(email_message)`**: Combines all the above functions to provide a one-for-all function to remove the email signature.



## Installation of the main library
Install the convosense_utilities library in your environment:
```python
pip install convosense_utilities

```


## How to Use

1. Install the required dependencies mentioned in the **Dependencies** section.

2. Use the `remove_sign(email_message)` function with the `email_message` as input to obtain the email body without the signature.
   Note: Make sure that the input email_message is in string format.

```python
# A sample to demonstrate the removal of email signature from the email body

# Replace the email_message with your input email text in string format
email_message = '''Hi Chinmay,

I hope this email finds you well. I have been following your work in the field of electrical engineeringand your contributions to the industry are truly impressive.

I am reaching out to explore the possibility of collaborating on a research project. 

Specifically, I am interested in optimizing power management systems through the integration of machine learning algorithms.

If you are open to a collaboration or have any thoughts on how we could potentially work together, I would love to hear from you.

Thank you for considering my inquiry. Looking forward to your response.

Regards,
Swapnil Bonde
Phone: (+91) 555-5555
Email: swapnilbonde94@gmail.com
LinkedIn: https://www.linkedin.com/in/swapnil-bonde-917905212/
'''
```
```python
# Import the email_signature_remover module
from convosense_utilities import email_signature_remover

# Pass on this email_message text in the remove_sign() function:
cleaned_text = email_signature_remover.remove_sign(email_message)

print(cleaned_text)
```
On printing the text with it's signature removed, the output will be:
```
Hi Chinmay,

I hope this email finds you well. I have been following your work in the field of electrical engineeringand your contributions to the industry are truly impressive.

I am reaching out to explore the possibility of collaborating on a research project. 

Specifically, I am interested in optimizing power management systems through the integration of machine learning algorithms.

If you are open to a collaboration or have any thoughts on how we could potentially work together, I would love to hear from you.

Thank you for considering my inquiry. Looking forward to your response.
```

The signature part from the original email text is removed, and this text can be further used for ***sentiment analysis***


## Accuracy

We have tested this python script extensively, and got very good results(> 95%). The email signature remover works well for most of the email texts.

Please note that the accuracy of the signature removal may vary depending on the email format and the presence of signatures.


## Contributions

Contributions are welcome! If you have any ideas, improvements, or bug fixes, please open an issue or submit a pull request.
