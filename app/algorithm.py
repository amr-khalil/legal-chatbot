# algorithm.py conains our special algorithms  

# Import libraries 
# import Levenshtein algorithm
from Levenshtein import ratio 
# summy for text summarization
from sumy.parsers.plaintext import PlaintextParser 
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer1
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer2
from sumy.summarizers.lsa import LsaSummarizer as Summarizer3
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import pandas as pd
import requests
import string
# import google search
from googlesearch import search
from bs4 import BeautifulSoup
import os
# import AWS DynamoDB
import boto3
from botocore.exceptions import ClientError
import json


def FAQ_data(): 
    # DynamoDB connection
    dynamodb = boto3.resource('dynamodb',
                         aws_access_key_id = os.environ.get('aws_access_key_id'),
                         aws_secret_access_key = os.environ.get('aws_secret_access_key'),
                         region_name = "eu-central-1")

    # import DB table
    table = dynamodb.Table('legalbot-FAQ')
    # convert table into json and extract items
    items = table.scan()['Items']
    # load table in dataframe
    df = pd.json_normalize(items)
    return df


    # Search in FAQ data using Levenshtein distance
def search_FAQ(questions):
    # Open the dataframe
    df = FAQ_data()
    def getApproximateAnswer(q):
        max_score = 0
        answer = ""
        prediction = ""

        # itteration on FAQ dataframe
        for idx, row in df.iterrows():
            # Score
            score = ratio(row["Question"], q)
            if score >= 0.9: # I'm sure, stop here
                return row["Answer"], score, row["Question"]
            elif score > max_score: # I'm unsure, continue
                max_score = score
                answer = row["Answer"]
                prediction = row["Question"]
        if max_score >= 0.5: # min. score
            return answer, max_score, prediction
        return "", max_score, prediction

    # Get the best result 
    def getResult(q):
        answer, score, prediction = getApproximateAnswer(q)
        return [q, prediction, answer, score]
    return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])



# To clean any text
def text_processing(text):
    text = text.replace('"', "'").replace('\n', '').strip()
    return text

# If we don't have the answer we will use google
def web_mining(question):
    question = str(question)
    # Open ten pages 
    urls = search(question, num_results=10, lang='de')
    # Fetch all pages
    def fetch_page(idx):
        url = urls[idx]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_p = soup.find_all('p')
        text = ""
        paragraphs = []
        for p in soup.find_all('p'):
            paragraphs.append(p.text)
        return paragraphs

    idx = 0
    paras = fetch_page(idx)
    # If the nummber of the paragraphes less than 7 paragraphs look for another page
    while len(paras) < 7:
        idx += 1
        paras = fetch_page(idx)
    # Join all paragraphs
    text = "".join(paras[:15])
    # clean the text
    processed_text = text_processing(text)
    # summarize the text
    summarized_text = summarize(processed_text, 4, 'TextRank')
    return summarized_text, urls[idx]

# To summerize the google articles and get rid of the similar answers
def summarize(text, SENTENCES_COUNT=3, algorithm = "LSA"):
    # Choose language
    LANGUAGE = "german"
    # Text container
    result = ""
    #Parser
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    # Stemmer
    stemmer = Stemmer(LANGUAGE)
    
    # Choose text summrization algorithm
    if algorithm == "LexRank":
        summarizer = Summarizer1(stemmer)
        
    elif algorithm == "TextRank":
        summarizer = Summarizer2(stemmer)
        
    elif algorithm == "LSA":
        summarizer = Summarizer3(stemmer)
    else:
        print("Error: algorithm = LexRank or TextRank or LSA. We choosed LSA for you.\n")
        summarizer = Summarizer3(stemmer)
    
    # Remove stopwords
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # Summrize the text
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        result += str(sentence)
    return result
