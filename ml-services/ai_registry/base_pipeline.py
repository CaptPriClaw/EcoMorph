# ml-services/ai_registry/base_pipeline.py

import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# --- NLTK Downloader ---
# The first time you run this, you may need to download the NLTK data.
# You can do this by running the following lines in a Python interpreter:
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# --- Initialize components ---
# We initialize these once to avoid reloading them on every function call.
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text: str) -> str:
    """
    A complete text preprocessing pipeline.

    This function takes raw text and performs the following steps:
    1. Converts to lowercase.
    2. Removes punctuation.
    3. Removes numbers.
    4. Tokenizes the text into words.
    5. Removes common English stopwords.
    6. Lemmatizes words to their root form.
    7. Joins the words back into a clean string.

    Args:
        text (str): The input string (e.g., "2 old blue denim jeans").

    Returns:
        str: The cleaned and preprocessed string (e.g., "old blue denim jean").
    """
    if not isinstance(text, str):
        return ""

    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 3. Remove numbers
    text = re.sub(r'\d+', '', text)

    # 4. Tokenize the text
    tokens = word_tokenize(text)

    # 5. Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # 6. Lemmatize words
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # 7. Join back into a single string
    return " ".join(lemmatized_tokens)