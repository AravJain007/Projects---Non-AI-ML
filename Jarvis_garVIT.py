from email.mime import audio
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import date
from datetime import datetime
import os
import pywhatkit as kt
import time
from setuptools import * # To overcome the problem of making it an exe type file
# This whole part is for importing sql and we made a cursor for it too named cursor [obvio]
import mysql.connector
con = mysql.connector.connect(host='localhost', user='root', password='project', database='bank')
if con.is_connected():
    print("Connected Successfully")
else:
    print("Connection not established!!!")
cursor = con.cursor(buffered=True)
# This whole part is for web scraping
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
import requests


# Initializing the Recognizer class
r = sr.Recognizer()


def speak_text(command):
    # Initializing the engine for converting text to speech
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Now we will take input of sound from the user
def get_input():
    try:
        with sr.Microphone() as source:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=10)
            print("Please speak now")
            speak_text("Please speak now")
            audio = r.listen(source)
            print("Recognizing sound")
            speak_text("Recognizing sound")
            myText = r.recognize_google(audio)
            myText = myText.lower()
            print("You said : ", myText.lower())
            speak_text(myText)
            return myText
    except sr.RequestError as e:
        print("Could not process your request;{0}".format(e))
    except sr.UnknownValueError:
        print("Unknown Error occured")


# now we break the input string word by word
arr_of_words = []


def split_into_words(myText):
    count = int(0)
    j = 0
    word = ""
    for i in range(0, len(myText)):
        if (myText[i] == ' '):
            arr_of_words.append(word)
            count += 1
            j = 0
            word = ""
        elif (i == (len(myText)-1)):
            word = word + myText[i]
            arr_of_words.append(word)
        else:
            word = word + myText[i]

def get_date(birthday):
    date1 = 0
    for i in range(0,len(birthday)):
        if(birthday[i].isdigit()):
            date1 = date1*10 + int(birthday[i])
        elif(birthday[i] == "th" or birthday[i] == "st" or birthday[i] == "nd" or birthday[i] == "rd"):
            i = i + 1
        else:
            break
    month = birthday[i+1:len(birthday)]
    print("date1 = ", date1)
    print("month = ", month)
    mnth = 0
    if(month == "january"):    
        mnth = 1
    elif(month == "february"):     
        mnth = 2
    elif(month == "march"):     
        mnth = 3
    elif(month == "april"):     
        mnth = 4
    elif(month == "may"):     
        mnth = 5
    elif(month == "june"):     
        mnth = 6
    elif(month == "july"):     
        mnth = 7
    elif(month == "august"):     
        mnth = 8
    elif(month == "september"):     
        mnth = 9
    elif(month == "october"):     
        mnth = 10
    elif(month == "november"):     
        mnth = 11
    elif(month == "december"):     
        mnth = 12
    d = mnth*100 + date1
    return d

# We make a key value pair for easier opening of famous sites and all. Its time complexity would be O[1] which is amazingly fast.
websites = {"google": "https://www.google.co.in/", "instagram": "https://www.instagram.com/", "spotify": "https://open.spotify.com/", "youtube": "https://www.youtube.com/", "twitter": "https://twitter.com/login",
            "discord": "https://discord.com/channels/@me", "netflix": "https://www.netflix.com/in/", "telegram": "https://web.telegram.org/k/", "amazon": "https://www.amazon.in/", "whatsapp": "https://web.whatsapp.com/",
            "prime video": "https://www.primevideo.com", "hotstar": "https://www.hotstar.com/in", "wikipedia": "https://www.wikipedia.org/", "gmail": "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox", "email": "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox",
            "pornhub": "https://www.pornhub.com/", "linkedin": "https://in.linkedin.com/", "twitch": "https://www.twitch.tv/", "quora": "https://www.quora.com/", "reddit": "https://www.reddit.com/", "pinterest": "https://in.pinterest.com/"
            }
apps = {"google chrome": "chrome", "microsoft powerpoint": "powerpnt",
        "microsoft word": "winword", "microsoft excel": "excel", "vlc player": "vlc"}
# now we use the input taken from the user to do tasks
myText = get_input()
split_into_words(myText)
if (arr_of_words[0] == "open"):
    try:
        sentence = ""
        for i in range(1, len(arr_of_words)):
            sentence = sentence + arr_of_words[i]
        url = websites[sentence]
        webbrowser.open_new_tab(url)
    except:
        try:
            app = apps[arr_of_words[1]+" "+arr_of_words[2]]
            os.system(app)
        except:
            print("Sorry can't recognize the website or app!")
            speak_text("Sorry can't recognize the website or app")

elif (arr_of_words[0] == "what" or arr_of_words[0] == "when"):
    for i in range(0,len(arr_of_words)):
        if (arr_of_words[i] == "date"):
            today = date.today()
            d2 = today.strftime("%B %d, %Y")
            print("Date = ", d2)
            speak_text("date is " + d2)
        elif (arr_of_words[i] == "time"):
            now = datetime.now()
            dt = now.strftime("%h:%M:%S") 
            print ("Time is : " + dt)
            speak_text("Time is " + dt)
        elif(arr_of_words[i] == "next"):  #This is for seeing the next thing in the event reminder and birthday chart
            if(arr_of_words[i+1] == "event"):
                try:
                    cursor.execute("SELECT time FROM event_reminder order by time")
                    date = cursor.fetchone()
                    cursor.execute("SELECT reminder FROM event_reminder order by time")
                    remind = cursor.fetchone()
                    print(remind)
                    speak_text(remind)
                except:
                    print("There is no reminder saved as of now")
                    speak_text("There is no reminder saved as of now")
            elif(arr_of_words[i+1] == "birthday"):
                try:
                    todayDate = date.today()
                    mnt = todayDate.month
                    day = todayDate.day
                    toFind = mnt*100 + day
                    try:
                        cursor.execute("SELECT dates FROM birthday where time > {} order by time".format(toFind))
                        dates = cursor.fetchone()
                        cursor.execute("SELECT name FROM birthday where time > {} order by time".format(toFind))
                        name = cursor.fetchone()
                        what_to_say = "The next birthday is " + str(name[0]) +"'s on " + str(dates[0])
                    except:
                        cursor.execute("SELECT dates FROM birthday order by time".format(toFind))
                        dates = cursor.fetchone()
                        cursor.execute("SELECT name FROM birthday order by time".format(toFind))
                        name = cursor.fetchone()
                        what_to_say = "The next birthday is " + str(name[0]) +"'s on " + str(dates[0])
                    print(what_to_say)
                    speak_text(what_to_say)
                except:
                    print("There is no birthday saved as of now")
                    speak_text("There is no birthday saved as of now")
    
elif (arr_of_words[0] == "search"):
    query = ""
    for i in range(1, len(arr_of_words)):
        query = query + " " + arr_of_words[i]
    print("Opening Google Chrome")
    speak_text("Opening Google Chrome")
    kt.search(query)

elif (arr_of_words[0] == "play"):
    query = ""
    for i in range(1, len(arr_of_words)):
        query = query + "%20" + arr_of_words[i]
    url = "https://open.spotify.com/search/"+query
    print("Opening Spotify on Chrome ")
    speak_text("Opening Spotify on Chrome")
    webbrowser.open_new_tab(url)

elif (arr_of_words[0]+" "+arr_of_words[1] == "set reminder"):
    try:
        cursor.execute("CREATE TABLE event_reminder(reminder varchar(255),time int)")
        con.commit()
    except:
        print("",end="")
    current_time = datetime().datetime().now()
    print("Whats the reminder")
    reminder = get_input()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    time_value = int(current_time[0:2])*10000 + int(current_time[3:5])*100 + int(current_time[6:])
    cursor.execute("insert into event_reminder values({},'{}')".format(time_value,reminder))
    con.commit()
    
elif (arr_of_words[0]+" "+arr_of_words[1] == "set birthday"):
    print("Please tell the birthday date")
    speak_text("Please tell the birthday date")
    birthday = get_input()
    proper_date_format = get_date(birthday)
    print("Whose birthday is it ?")
    speak_text("Whose birthday is it ?")
    name = input("Enter the Name here using keyboard : ")
    try:
        cursor.execute("CREATE TABLE birthday(dates varchar(15),name varchar(20),time int)")
        con.commit()
    except:
        print("",end="")
    query = "insert into birthday(dates,name,time) values(%s,%s,%s)"
    cursor.execute(query, (birthday,name,proper_date_format))
    con.commit()

elif(arr_of_words[0]+" "+arr_of_words[1] == "find flight" or arr_of_words[0]+" "+arr_of_words[1] == "find flights" or arr_of_words[0] == "flight" or arr_of_words[0] == "flights"):
    destination1 = ""
    destination2 = ""
    i = 0
    while(arr_of_words[i] != "from"):
        i = i+1
    while(i < len(arr_of_words)):
        if(arr_of_words[i] == "from"):
            while(arr_of_words[i] != "to"):
                if(arr_of_words[i] == "from"):
                    i = i+1
                if(destination1 == ""):
                    destination1 = destination1 + arr_of_words[i]
                    i = i+1
                else:
                    destination1 = destination1 + "_" + arr_of_words[i]
                    i = i+1
        else:
            if(arr_of_words[i] == "to"):
                i = i+1
            if(destination2 == ""):
                destination2 = destination2 + arr_of_words[i]
                i = i+1
            else:
                destination2 = destination2 + "_" + arr_of_words[i]
                i = i+1
    #Now i have to provide 5 options and jarvis will say the cheapest option
    query1 = "https://www.makemytrip.com/flights/"
    query2 = destination1 + "-" + destination2
    query3 = "-cheap-airtickets.html"
    webbrowser.open_new_tab(query1+query2+query3)
    
#elif(arr_of_words[0] + " " + arr_of_words[1] == "send mail"):
    
elif(arr_of_words[0] + " " + arr_of_words[1] == "who is"):
    search_request1 = "https://en.wikipedia.org/wiki/"
    search_request2 = ""
    for i in range(2,len(arr_of_words)):
        if(i == len(arr_of_words)):
            search_request2 = search_request2 + arr_of_words[i]
        search_request2 = search_request2 + arr_of_words[i] + "_"
    search_request = search_request1 + search_request2
    # This is for getting the url and all the html walla data
    page = requests.get(search_request)
    # Now using beautiful soup to make it all better
    soup = BeautifulSoup(page.content, 'html.parser')
    list(soup.children)
    # Now we find all occurences of p since they have all the written parts
    # The 0 index doesnt give anything at all you have to start from 1st index onwards for whichever paragraph they put
    total_data = soup.find_all('p')[1].get_text()
    print(total_data)
    speak_text(total_data)