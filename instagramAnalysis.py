'''
author : Arav Jain 
project description : This bot basically sends user analysis data like how many people are following them and how many people they are following
and how many people follow them back and the users which are common (like they both follow and are being followed). Then next part of it is mostly
going to be scanning through the comments and then unfollowing the person who makes cheap comments about users.
date of initiation : 17-10-2022 03:28:30 PM
'''
from instabot import Bot
import pandas as pd
import time
import os
import glob
import instaloader
import csv

L = instaloader.Instaloader()
username = "aravqt.69"
password = "project22"
L.login(username,password)

following = 0
followers = 0
profile = instaloader.Profile.from_username(L.context, "dee.see_")
followers_list = []
following_list = []
for i in profile.get_followers():
    followers+=1
    followers_list.append(i)
print("Followers : ", followers)
time.sleep(5)
for i in profile.get_followees():
    following+=1
    following_list.append(i)
print("Following : ", following)
time.sleep(5)
followers_that_follow_you_back = []
for i in followers_list:
    for j in following_list:
        if(i == j):
            followers_that_follow_you_back.append(i)
print("Number of people whom you follow that follow you back : ", len(followers_that_follow_you_back))

followers_that_dont_follow_you_back = []
for i in following_list:
    count1 = 0
    for j in followers_list:
        if(i == j):
            break
        else:
            count1 += 1
    if(count1 == len(followers_list)):
        followers_that_dont_follow_you_back.append(i)

print("Followers that you follow that do not follow you back : ", len(followers_that_dont_follow_you_back))
for i in followers_that_dont_follow_you_back:
    print(i)
        
comments_on_posts = []
username_to_be_blocked = []
"""
with open("./badCommentsWhichGetUsersBlock",'r') as badComments:
    csvreader = csv.reader(badComments,delimiter = ',')
    for i in profile.get_all_posts():
        for j in i.get_comments():
            comments_text_part = j.text
            for k in csvreader:
                if (j == k):
                    username_to_be_blocked.append(j.owner)
print("The people who need to be blocked : ")
for i in username_to_be_blocked  :
    print(i)
"""
print("Comments : ")
#with open(r"C:\Users\DELL\Desktop\PROJECTS\instagramBotForAnalysis\badCommentsWhichGetUsersBlock.csv") as badcomments:
    #csvreader = csv.reader(badcomments, delimiter = '\n')
for i in profile.get_posts():
    time.sleep(5)
    for j in i.get_comments():
        comments_text_part = j.text.lower()   # Since the i.get_comments() returns a tuple with text, created at, id, owner and answers if available.
        comments_id_part = j.owner
        print(comments_id_part)
        print(comments_text_part)
        #if(comments_text_part in csvreader):
            #username_to_be_blocked.append(j.owner)
        time.sleep(5)
        for k in j.answers:
            print(k.text)
            #if(k.text.lower() in csvreader):
                #username_to_be_blocked.append(k.owner)