import os
import re
from pdfminer.high_level import extract_text
import streamlit as st
from io import StringIO
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from heapq import nlargest
from string import punctuation
from pdfminer.pdfpage import PDFPage
from pdfminer.interp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import TextConverter
from collections import Counter

st.title("PDF Summarizer")
file_path = st.file_uploader("Please choose a PDF", type=["pdf"], accept_multiple_files = False)

def extract_description(text, start, end):
    item = re.finditer(start, text)
    _start = list(item)[0].span()

    item2 = re.finditer(end, text)
    _end = list(item2)[0].span()
    description = text[_start[1]:_end[0]]

    return description

def fix_string(string):
    pattern = 'r([a-z])([A-Z])'
    fixed_string = re.sub(pattern, r'\1 \2', string)
    return fixed_string

if file_path is not None:

    text = extract_text(file_path).replace('\r', '').replace('\n', '  ')
    business_start = '((ITEM)|(ITEM)) 1. *((BUSINESS)|(BUSINESS))+\D'
    business_end = '((ITEM)|(ITEM)) 2. *((BUSINESS)|(BUSINESS))+\D'

    business_description = extract_description(extract_description(text, business_start, business_end))

    stopwords=list(STOP_WORDS)
    stopwords.append('@')
    stopwords.append(' ')

    punctuation = punctuation + '\n'

    text = business_description
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens=[token.text for token in doc]

    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys:
        word_frequencies[word] = word_frequencies[word]/max_frequency

    sentence_tokes = [sent for sent in doc.sents]

    sentence_scores = {}
