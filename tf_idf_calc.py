import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the CSV (ensure the CSV file is in the same directory or provide the full path)
df = pd.read_csv("allURLs.csv")

# Group URLs by category
categories = df['type'].unique()

def get_article_content(url, timeout=10):
    try:
        print(f"Fetching content from: {url}")
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Assuming the content is within a <p> tag; adjust as necessary
        paragraphs = soup.find_all('p')
        article_content = ' '.join([para.get_text() for para in paragraphs])

        if not article_content:
            print(f"No content found for {url}")
        return article_content

    except requests.exceptions.Timeout:
        print(f"Timeout error while fetching {url}. Skipping this URL.")
        return ""

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

# Get content for each category
category_contents = {}
all_contents = []  # Collect all contents to compute IDF on the entire dataset
for category in categories:
    category_urls = df[df['type'] == category]['url'].tolist()
    contents = [get_article_content(url) for url in category_urls]
    category_contents[category] = contents
    all_contents.extend(contents)

# Define a custom list of stopwords
custom_stopwords = ['english']

# Initialize the TF-IDF Vectorizer for the entire corpus (all categories)
vectorizer = TfidfVectorizer(stop_words='english')

# Fit the vectorizer on all articles
vectorizer.fit(all_contents)

def compute_top_10_tfidf(category_contents):
    # Transform the category's articles to get the TF-IDF matrix
    tfidf_matrix = vectorizer.transform(category_contents)
    
    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()

    # Sum up the TF-IDF scores for each word across all articles in the category
    tfidf_scores = tfidf_matrix.sum(axis=0).A1  # Flatten the array
    
    # Create a DataFrame to pair words with their scores
    word_scores = pd.DataFrame(zip(feature_names, tfidf_scores), columns=['word', 'score'])
    
    # Sort by the score in descending order
    word_scores = word_scores.sort_values(by='score', ascending=False)
    
    # Get the top 10 words
    top_10_words = word_scores.head(10)
    
    return top_10_words

# Compute TF-IDF for each category
category_top_10_words = {}
for category, contents in category_contents.items():
    category_top_10_words[category] = compute_top_10_tfidf(contents)

# Display the results
for category, top_words in category_top_10_words.items():
    print(f"Top 10 words for category '{category}':")
    print(top_words)
    print("\n")
