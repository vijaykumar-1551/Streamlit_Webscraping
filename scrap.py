import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from transformers import pipeline

def scrapeWikiArticle(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    st.write(f"Title: {title.text}")

    allLinks = soup.find(id="bodyContent").find_all("p")
    article = ""
    for link in allLinks:
        article += link.text

    # Remove invalid characters
    article = re.sub(r'[^\x00-\x7F]+', ' ', article)

    # Summarize text
    def summarizeText(text):
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", tokenizer="sshleifer/distilbart-cnn-12-6")
        max_chunk_len = 1024
        chunks = [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]
        summary = ""
        for chunk in chunks:
            summary += summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text'] + " "
        return summary

    # Save summary to file
    summary = summarizeText(article)
    with open('summary.txt', 'w') as f:
        f.write(summary)

    # Show summary in streamlit
    st.write("Summary:")
    st.write(summary)

# Streamlit UI
st.title("Wikipedia Article Summarizer")
url = st.text_input("Enter Wikipedia URL:")
if url:
    scrapeWikiArticle(url)
