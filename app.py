# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:32:38 2020

@author: Keshav Ganapathy
"""

from text import Text
from network import Network
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods = ["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/message", methods = ["POST"])
def message():
    var1 = request.form.get("name")
    var2 = request.form.get("input")
    #info = upload_file()
    if var2 == "":
        info = text(var1)
    elif var1 == "":
        info = link(var2)
    else:
        info = upload_file()
    #print(info)
    return render_template("results.html", number=info[0], wordPolarity=info[1], message=info[2], polarity=info[3], 
                           wordCount=info[4], charCount=info[5], subjectivity=info[6], spaceCount=info[7])

def text(txt):
    text = Text(txt)    
    display = txt
    if len(txt)>1000:
        display = txt[:1000]+' ...'
    values = ["Message is: " + display, "Polarity Value(-1 to 1): " + str(text.polarity), 
              "Word Count is: " + str(text.wordCount), "Character Count is: " + str(text.characterCount), 
              "Subjectivity Score(0 to 1): " + str(text.subjectivity), "Space Count is: " + str(text.spacecount)]
    #print(txt)
    network = Network(txt)
    value = network.getVal()
    wordPolarity = network.getBias()
    #print(value, wordPolarity)
    values.insert(0, wordPolarity)
    values.insert(0, (value*100))
    return values

def link(url):
    #print("entered url")
    #print(url)
    message = ""
    if Text.youtube_to_string(url) == None:
        message = Text.url_to_string(url)
    else:
        message = Text.youtube_to_string(url)
    text = Text(message)
    display = message
    if len(message)>1000:
        display = message[:1000]+' ...'
    values = ["Message is: " + display, "Polarity Value(-1 to 1): " + str(text.polarity), 
        "Word Count is: " + str(text.wordCount), "Character Count is: " + str(text.characterCount), 
        "Subjectivity Score(0 to 1): " + str(text.subjectivity), "Space Count is: " + str(text.spacecount)]
    network = Network(message)
    value = network.getVal()
    wordPolarity = network.getBias()
    #print(wordPolarity, value)
    values.insert(0, wordPolarity)
    values.insert(0, (value*100))
    return values

def upload_file():
    print('hello this is uploading a file')
    file = request.files["file"]
    with open(file) as f:
        file_content = f.read() 
    print(file_content)
    #filename = secure_filename(file.filename) 
    #file.save(os.path.join("Data",filename))
    '''with open("Data/filename") as f:
        file_content = f.read() 
    print(file_content)'''
    
@app.route("/file")
def file():
    var = request.args.get("text")
    text = Text(var)
    values = ["Message is: " + str(text.getMessage()), "Polarity Value(-1 to 1): " + str(text.polarity), 
              "Word Count is: " + str(text.wordCount), "Character Count is: " + str(text.characterCount), 
              "Subjectivity Score(0 to 1): " + str(text.subjectivity), "Space Count is: " + str(text.spacecount)]
    string = ""
    for i in range (len(values)):
        string += values[i]
        string += "<br/>"
    return render_template("index.html", var = var)

@app.route("/url", methods = ["POST","GET"])
def url():
    print("entered url")
    var = request.form.get("urlThing")
    print(var)
    message = ""
    if Text.youtube_to_string(var) == None:
        message = Text.url_to_string(var)
    else:
        message = Text.youtube_to_string(var)
    print(message)
    text = Text(message)
    values = ["Message is: " + str(text.getMessage()), "Polarity Value(-1 to 1): " + str(text.polarity), 
        "Word Count is: " + str(text.wordCount), "Character Count is: " + str(text.characterCount), 
        "Subjectivity Score(0 to 1): " + str(text.subjectivity), "Space Count is: " + str(text.spacecount)]
    string = ""
    for i in range (len(values)):
        string += values[i]
        string += "<br/>"
    network = Network(message)
    value = network.getVal()
    wordPolarity = network.getBias()
    return render_template("results.html", number=100-(value*100), wordPolarity=wordPolarity, additionalInfo=string)

if __name__ == '__main__':
    app.run()
    