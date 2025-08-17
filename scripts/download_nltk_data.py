# scripts/download_nltk_data.py
import nltk

print("Downloading NLTK data...")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
print("NLTK data downloaded successfully.")