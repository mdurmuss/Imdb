#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Mustafa Durmuş

from bs4 import BeautifulSoup
import sys,requests
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QVBoxLayout,QTextEdit,QHBoxLayout,QLineEdit,QLabel

class Film():
    def __init__(self):
        url = "https://www.imdb.com/chart/top"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content,"html.parser")
        self.film_names = soup.find_all("td",{"class":"titleColumn"})
        self.rating = soup.find_all("td",{"class":"ratingColumn imdbRating"})

    def list(self,rating):
        a = list()
        for self.topic,self.my_rating in zip(self.film_names,self.rating):
            self.topic = self.topic.text
            self.my_rating = self.my_rating.text

            self.topic = self.topic.strip()
            self.topic = self.topic.replace("\n","")

            self.my_rating = self.my_rating.strip()
            self.my_rating = self.my_rating.replace("\n", "")
            if rating == 0.0:
                a.append(self.topic+" Rating: "+self.my_rating)

            else:
                try:
                   if float(self.my_rating) >= float(rating):
                        a.append(self.topic + " Rating: " + self.my_rating)
                except:
                    if ValueError:

                        return "Enter a float number!"
        return a

class CopyUrl():
    def __init__(self,x):
        self.count = 1
        self.url = "https://www.imdb.com/chart/top"
        self.response = requests.get(self.url)
        self.html_content = self.response.content
        self.soup = BeautifulSoup(self.html_content, "html.parser")
        self.film_names = self.soup.find_all("td", {"class": "titleColumn"}, ("a"))

        for j in self.film_names:
            j = str(j).split("<a hre")
            if self.count == int(x):
                break
            self.count += 1
        j = j[1].split("title")
        j[1].strip()
        self.isim = str(j[1])

        url = "https://www.imdb.com/title" + self.isim
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        film_names = soup.find_all("div", {"class": "inline canwrap"})
        print(film_names)
        for i in film_names:
            self.storyline = i.text
        self.storyline = self.storyline.strip()
        
        
class Pencere(QWidget,Film):

    def __init__(self):
        super().__init__() # Call super class's init function.
        self.init_ui() # Create own init function.

    def init_ui(self):
        self.ratio = float(8.0) # RATING Standart Value
        self.films = Film() 
        self.text_place = QTextEdit() 
        self.list_button = QPushButton("LIST") 
        self.clear_button = QPushButton("CLEAR") 
        self.ratingButton = QLabel("RATING:") 
        self.line = QLineEdit(str(self.ratio)) 
        self.plus_button = QPushButton("+") 
        self.minus_button = QPushButton("-") 
        self.storyButton = QPushButton("STORY") 
        self.storyLabel = QLabel("Enter the number of the film you want to see and push STORY button!")
        self.story = QLineEdit()

        h_box = QHBoxLayout()
        h_box.addWidget(self.text_place)

        h_box2 =QHBoxLayout()
        h_box2.addWidget(self.list_button)
        h_box2.addWidget(self.clear_button)
        h_box2.addStretch()
        h_box2.addWidget(self.ratingButton)
        h_box2.addWidget(self.line)
        h_box2.addWidget(self.plus_button)
        h_box2.addWidget(self.minus_button)

        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.storyButton)
        h_box3.addWidget(self.storyLabel)
        h_box3.addWidget(self.story)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)

        self.setLayout(v_box)

        self.list_button.clicked.connect(self.click)
        self.clear_button.clicked.connect(self.click)
        self.plus_button.clicked.connect(self.click)
        self.minus_button.clicked.connect(self.click)
        self.storyButton.clicked.connect(self.click)

        self.setWindowTitle("IMDB FILMS")
        self.show()

    def click(self): 
        """
        Runs when user clicks a button
        """
        sender = self.sender() # Value of the pushed button
        if sender.text() == "LIST": 
            a = self.films.list(self.line.text())
            b = ""                                  
            for i in a:
                 b += (str(i)+"\n")

            self.text_place.setText(b)
        elif sender.text() == "CLEAR":
            self.text_place.clear()

        elif sender.text() == "+": 
            if self.ratio != 10.0:
             self.ratio += 0.1

        elif sender.text() == "-":
            if self.ratio != 8.0: 
                self.ratio -= 0.1
        elif sender.text() == "STORY": 
            self.show_topic() 

        self.line.setText(str(round(self.ratio,2)))

    def show_topic(self,):
        url = CopyUrl(self.story.text())
        self.text_place.setText(url.storyline) 
        self.number = self.films.topic.split(".")[0]


app = QApplication(sys.argv)

pen = Pencere()

pen.setGeometry(500,10,700,400)

sys.exit(app.exec_())

