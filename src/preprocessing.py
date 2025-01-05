import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')

from sklearn.feature_extraction.text import CountVectorizer


def bow_model(spam_data_path: str) -> CountVectorizer:
    cv = CountVectorizer(max_features=42500)
    corpus_array = []
    with open(spam_data_path, 'r') as file:
        for line in file:
            corpus_array.append(line.strip())
    X = cv.fit_transform(corpus_array).toarray()
    return cv

def preprocess_email(email: str, cv: CountVectorizer) -> str:
    """
        This function to preprocessing email before to model
    
    Args:
        email (str): content email
        
    Returns:
        str: Email 
    """
    
    # Eliminate space
    email = re.sub(r'\r\n', ' ', email)
    
    # 6. Eliminate stopwords
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    stop_words.remove('not')

    email = email.lower().translate(str.maketrans('','', string.punctuation)).split()
    email = [ps.stem(word) for word in email if word not in stop_words]
    email = ' '.join(email)
    
    # 7. BOW model
    email = cv.transform([email]).toarray()

    return email

