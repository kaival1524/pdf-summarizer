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

def 