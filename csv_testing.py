import os
import pandas as pd
from collections import Counter
import streamlit as st
import nltk
from nltk.corpus import stopwords
import re  # Import regular expressions

# Download the stopwords corpus (run this once)
nltk.download('stopwords')

# Load English stop words from NLTK
nltk_stop_words = set(stopwords.words('english'))

# Custom list of syncategorematic words (you can modify this list)
custom_syncategorematic_words = { "and", "or", "but", "if", "while", "because", "although", "the", "a", "an", "in", "on", "with",
    "by", "to", "of", "for", "from", "at", "about", "between", "before", "after", "since", "until",
    "does", "not", "really", "due", "it", "appears", "yet", "possible", "can", "transfer", "from",
    "in", "addition", "to", "the", "opposite", "stroke", "works", "well", "is", "only", "bit",
    "my", "opinion", "perfect", "platform", "this", "though", "leaves", "a", "lot",
    "to", "be", "desired", "specially", "around", "you", "can't", "even", "move",
    "a", "workout", "to", "a", "different", "day", "may", "be", "more", "data", "than", "i", "need",
    "personally", "but", "overall", "it's", "a", "training", "app", "the", "sync", "with", "the",
    "is", "a", "touch", "confusing", "the", "says", "i", "did", "it", "training", "peaks", "says",
    "i", "did", "something", "but", "it", "doesn't", "seem", "to", "know", "what", "unfortunately",
    "the", "preview", "images", "in", "are", "misleading", "the", "app", "is", "of",
    "little", "use", "without", "a", "good", "knowledge", "of", "it's", "a", "shame",
    "i'm", "convinced", "that", "it", "would", "otherwise", "be", "helpful", "trainingpeaks", "me", "p", 
    "com", "https", "www", "your", "please", "have", "1", "account", "hi", "email", "coach", "de", "thanks", 
    "thank", "help", "2024", "like", "tp", "im", "get", "support", "submitted", "workouts", "one", "request", "athlete",
    "hello", "la", "time", "see", "attached", "el", "want", "ive", "dont", "new", "llc", "information", "could", "regards",
    "cant", "add", "2", "way", "athletes", "change", "back", "wrote", "view", "using", "que", "using", "make", "received", 
    "un", "set", "date", "mi", "louisville", "co", "sep", "us", "didnt", "285", "century", "question", "able", "en", "happy",
    "httpsapptrainingpeakscomcalendar", "also", "still", "80027", "click", "pm", "trainingpeakscom", "let", "today", "con", "name", 
    "httpsapptrainingpeakscom","faqs"
                                 
}

st.title("Populate most used words in Zendesk")

# Combine NLTK stop words and custom syncategorematic words into one set
STOP_WORDS = nltk_stop_words.union(custom_syncategorematic_words)

# Function to clean and count words while ignoring stop words and unwanted characters
def count_words_ignore_stopwords(text_series, stop_words):
    words = []
    for text in text_series:
        # Remove unwanted characters like spaces, hyphens, and HTML tags using regex
        cleaned_text = re.sub(r'[^\w\s]', '', text)  # Remove non-word characters except spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with a single space
        cleaned_text = re.sub(r'<[^>]+>', '', cleaned_text)  # Remove HTML tags like <p>
        
        # Split the cleaned text into words, lowercase them, and filter out stop words
        words.extend([word for word in cleaned_text.lower().split() if word not in stop_words])
    
    return Counter(words)

# Build the file path dynamically
df = pd.read_csv('zd_tickets.csv')

# Count word occurrences in the 'Description' column while ignoring stop words and unwanted characters
occurrences = count_words_ignore_stopwords(df['Description'], STOP_WORDS)

# Get the top 10 most used words
top_10_most_used_words = occurrences.most_common(50)

# Print the top 10 most used words with their counts
#for word, count in top_10_most_used_words:
    #print(f"{word}: {count}")
if st.button("Submit"):
    result = (occurrences.most_common(50))
    output_message = f"""
    Top used words: {top_10_most_used_words}
    """
    st.write(output_message)


