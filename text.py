# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:49:42 2020

@author: Keshav Ganapathy
"""

from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import PyPDF2

from youtube_transcript_api import YouTubeTranscriptApi


class Text:
    message = ""
    polarity = 0
    wordCount = 0
    characterCount = 0
    subjectivity = 0
    spacecount = 0

    def __init__(self, string):
        self.message = string
        self.doSentiment()

    def doSentiment(self):
        blob = TextBlob(self.message)
        self.polarity = blob.polarity
        self.subjectivity = blob.subjectivity
        self.doWordCount()

    def doWordCount(self):
        length = len(self.message.split())
        self.wordCount = length
        self.doCharacterCount(self.message.split())
        self.doSpaceCount(self.message.split())

    def doCharacterCount(self, wordArr):
        charCount = 0
        for i in range(len(wordArr)):
            currWord = wordArr[i]
            charCount = charCount + len(currWord)
        self.characterCount = charCount
        
    def doSpaceCount(self, wordArr):
        self.spacecount = (len(wordArr) - 1)
        
    def getMessage(self):
        return self.message
    
    @staticmethod
    def url_to_string(url):
        res = requests.get(url)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        #print(set([t.parent.name for t in text]))
        txt = ''
        blacklist = [
            '[document]',
            'a',
            'body',
            #'cite',
            #'div',
            #'h1',
            'h2',
            'h3',
            'h4',
            'li',
            'link',
            #'p',
            'script',
            #'span',
            'style',
            #'title'
        ]
        for t in text:
            if t.parent.name not in blacklist:
                txt += '{} '.format(t)

            
            #formatting        
        txt = txt.replace("\n","")
        txt = " ".join(txt.split())
        return txt

    @staticmethod
    def txtFile_to_string(path):
        txt = open(path, 'r', encoding = 'utf8').read()
        txt = txt.replace("\n","")
        txt = " ".join(txt.split())
        return txt
    
    @staticmethod
    def pdf_to_string(path):
        pdffileobj=open(path,'rb')
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        x=pdfreader.numPages
        pageobj=pdfreader.getPage(x-1)
        txt=pageobj.extractText()
        #txt = txt.replace("\n","")
        #txt = " ".join(txt.split())
        return txt

    @staticmethod
    def youtube_to_string(link):
        try:
            link = link.replace('https://www.youtube.com/watch?v=', '')
    
            transcription_dict = YouTubeTranscriptApi.get_transcript(link)
            txt = ''
            for i in transcription_dict:
                txt=txt+i['text']
            return txt
        except:
            return None