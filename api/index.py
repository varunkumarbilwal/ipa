import requests
from bs4 import BeautifulSoup
import json
import os.path
from os import path
import sys
import stat
import xml.etree.ElementTree as ET
import wget
from flask import Flask, render_template

app = Flask(__name__)

url = 'https://ipa-apps.me'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, features='html5lib')

articles = soup.find_all({'div': 'item-content'})

imgsrcs = []
titles = []
hrefs = []

for i in articles:

    itemMedia = i.find('div', class_ = 'item-media')
    if(itemMedia != None):
        imgTag = itemMedia.find('img', class_ = 'app-icon')
        if(imgTag != None):
            imgSrc = imgTag['src']
            if imgSrc not in imgsrcs:
                imgsrcs.append(imgSrc)
    
    itemInner = i.find('div', class_ = 'item-inner')
    if(itemInner != None):
        itemTitle = itemInner.find('div', class_ = 'item-title')
        title = itemTitle.text
        if title not in titles:
            titles.append(title)

    itemTitleRow = i.find('div', class_ = 'item-title-row')
    if(itemTitleRow != None):
        itemAfter = itemTitleRow.find('div', class_ ='item-after')
        if(itemAfter != None):
            alink = itemAfter.find('a', class_ = 'button')
            if(alink != None):
                ahref = alink['href']
                #fhref = "https://ipa-apps.me" + ahref
                rhref = ahref.replace("/Links/", "")
                fhref = rhref.replace(".php", "")
                if fhref not in hrefs:
                    hrefs.append(fhref)

certname = soup.find('span', class_ = 'success1')
certtext = certname.text
cert = certtext.split('"')
fcert = cert[1]

@app.route("/")
def home():
    return render_template("index.html", certname=fcert,len=len(hrefs), simgsrc=imgsrcs, stitle=titles, shref=hrefs)

@app.route("/install/<purl>")
def user(purl):
    url2 = "https://ipa-apps.me/Links/" + purl + ".php"
    r2 = requests.get(url2, headers=headers)
    soup2 = BeautifulSoup(r2.content, features='html5lib')
    articles2 = soup2.find('a')['href']
    plistu = articles2.split("url=")
    fplist = plistu[1]

    return render_template("install.html", plisturl=fplist)




