# Publicized for GitHub
# pkmiya@All rights reserved.

#ref
#https://py-memo.com/python/english-wordbook-part1/

#ver. 1.1.0
#REMARK: Development is in-progress, and I'm aware of many existing bugs.

import requests
from bs4 import BeautifulSoup
import csv
import sys

help = "\'r\': Search for one word and register to list, \'rr\': Register continuously, \'s\': Just search for a word, \'h\': Help, 'q': Quit"

isExist = 1 # Flag

def disphelp():
    print("[HELP]")
    print(help + "\n")
    return

def scrape(word):
    #scrape here
    search_word = "https://ejje.weblio.jp/content/" + word
    try:
        url = requests.get(search_word)
        soup = BeautifulSoup(url.text, "html.parser")
        word_mean = soup.find(class_='content-explanation ej').get_text()
        isExist = 1
        return word_mean
    except:
        isExist = 0
        print("This word does not exist.")
        return
        #exit(1)

    #Display meaninig

def word_app(word):
    data = [word, scrape(word)]
    with open('list.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(data)

#Open list file where words are saved
print("Importing list file...")
try:
    with open('list.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
except:
    print("Eoor: Listfile doesn't exist. Consider to create or import \'list.csv\'.")
    exit(1)

#Display opening menu

print("English dictiionary ver. 1.1.0")
print("Hello")
print(help)
#"'r': Search for one word and register to list, 'rr': Register continuously, 's': Just search for a word, 'h': Help, 'q': Quit"

while True:
    #Select menu
    menu = input("Select actions: ")
    if menu == "h":
        disphelp()
    elif menu == "s":
        word = input("Enter a word to look up its meanings: ")

        word_mean = scrape(word)
        print(word_mean)

        for exist_word in l:
            if exist_word[0] != word:
                while True:
                    append_or_not = input("Append this word to list? y/n: ")
                    if append_or_not == "y":
                        word_app(word)
                        break
                    elif append_or_not == "n":
                        break
                    else:
                        print("Warning: Enter \'y\' or \'n\'. Please try again.")
    elif menu == "r":
        word = input("Enter a word you\'d like to register: ")
        for exist_word in l:
            if exist_word[0] == word:
                while True:
                    exist_word_verif = input("This word is already registered. Check its meaning? y/n:")
                    if exist_word_verif == "n":
                        break
                        #sys.exit(0)
                    elif exist_word_verif == "y":
                        print(exist_word[1])
                        break
                        #sys.exit(0)
                    else:
                        print("Please enter \'y\' or \'n\'.")
                        #sys.exit(1)
        print(scrape(word))
    elif menu == "rr":
        print("[Continuous mode] Enter \'q\' to quit this mode.")
        while True:
            word = input("Enter a word to append to the list: ")
            if word == "q":
                break
            for exist_word in l:
                if exist_word[0] == word:
                    continue
            #scrape(word) and if not existed, not append
            print(scrape(word))
            if isExist == 0:
                continue
            word_app(word)
    elif menu == "q":
        print("bye")
        sys.exit(0)





"""
Main menu
    Select menu(h: help, s: search, r: register, rr: continuous register, q: quit)
    1. help
        show help
    2. search
        2-1. scrape
        2-2. display
    3. register
        3-1. scrape
        3-2. display
        3-3. append
    4. continuous register
        4-1. scrape
        4-2. append
    5. quit
"""
