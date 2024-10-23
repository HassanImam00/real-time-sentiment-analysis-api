'''

Author: Hassan Imam

This script is used for preprocessing the dataset. We perform certain steps such as NLTK Downloads, Data Cleaning Steps, Text Preprocessing
Data Splitting and Saving the Processed Data

'''

import pandas as pd
import numpy as np
import string
import nltk
import os

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Paths to input and output files
DATA_DIR = 'data'
INPUT_FILE = os.path.join(DATA_DIR, 'Reviews.csv')
TRAIN_OUTPUT = os.path.join(DATA_DIR, 'train_data.csv')
TEST_OUTPUT = os.path.join(DATA_DIR, 'test_data.csv')

def load_data(file_path):
    """Load the dataset from a CSV file."""
    print("Loading data...")
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    """Clean and preprocess the data."""
    print("Preprocessing data...")

    # Drop rows with missing values in 'Text' or 'Score'
    df = df.dropna(subset=['Text', 'Score'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['Text'])

    # Convert 'Score' to integer
    df['Score'] = df['Score'].astype(int)

    # Remove neutral reviews (Score == 3)
    df = df[df['Score'] != 3]

    # Map scores to sentiments
    df['Sentiment'] = df['Score'].apply(lambda x: 'positive' if x > 3 else 'negative')

    # Normalize text
    df['Text'] = df['Text'].str.lower()

    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    df['Text'] = df['Text'].apply(lambda x: x.translate(translator))

    # Tokenization
    df['Tokens'] = df['Text'].apply(nltk.word_tokenize)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    df['Tokens'] = df['Tokens'].apply(lambda tokens: [word for word in tokens if word not in stop_words])

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    df['Tokens'] = df['Tokens'].apply(lambda tokens: [lemmatizer.lemmatize(token) for token in tokens])

    # Join tokens back to string
    df['Processed_Text'] = df['Tokens'].apply(lambda tokens: ' '.join(tokens))

    return df

def split_and_save_data(df, train_output, test_output):
    """Split the data into training and testing sets and save them to CSV files."""
    print("Splitting data into training and testing sets...")

    X = df['Processed_Text']
    y = df['Sentiment']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Combine features and labels
    train_data = pd.DataFrame({'Text': X_train, 'Sentiment': y_train})
    test_data = pd.DataFrame({'Text': X_test, 'Sentiment': y_test})

    # Save to CSV files
    train_data.to_csv(train_output, index=False)
    test_data.to_csv(test_output, index=False)

    print(f"Training data saved to {train_output}")
    print(f"Testing data saved to {test_output}")

def main():
    # Check if data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created data directory at {DATA_DIR}")

    # Check if input file exists
    if not os.path.isfile(INPUT_FILE):
        print(f"Input file not found at {INPUT_FILE}")
        print("Please ensure the dataset is downloaded and placed in the 'data/' directory.")
        return

    # Load, preprocess, and split the data
    df = load_data(INPUT_FILE)
    df = preprocess_data(df)
    split_and_save_data(df, TRAIN_OUTPUT, TEST_OUTPUT)
    print("Data preprocessing completed successfully.")

if __name__ == '__main__':
    main()
