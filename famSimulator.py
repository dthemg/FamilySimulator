# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 10:16:44 2017

@author: David Montgomery

Family Simulator, 1
Based on Markov Text Generator

It works but it kindof sucks
update to read two words backward when there is more than one possibility
"""
from os.path import dirname, abspath
import numpy.random as random

directory = dirname(abspath(__file__))
convoPath = directory + '\\data\\fullConversation.txt'
textFile = open(directory + "\\data\\fullConversation.txt", 'r')

lines = textFile.readlines()

# Define ID constants
ANNA_ID = str(100000690214136)
DAVID_ID = str(787509610)
MATTIAS_ID = str(539450389)
ERLAND_ID = str(100001975335371)

# Define sifting constants
SIFT_EMOJIS = True
SIFT_CALLS = False

# Define Markov constants
MAX_LENGTH = 100

numberOfLines = len(lines)

# Removing "\n", "??" from the lines
for i in range(numberOfLines):
    if SIFT_EMOJIS:
        lines[i] = lines[i].replace('??', '')
    lines[i] = lines[i].replace('\n', '')

messagesDavid = []
messagesAnna = []
messagesMatilda = []
messagesMattias = []
messagesErland = []

dictDavid = {'beginSequence':{}}
dictAnna = {'beginSequence':{}}
dictMatilda = {'beginSequence':{}}
dictMattias = {'beginSequence':{}}
dictErland = {'beginSequence':{}}

dict2Matilda = {}
dict2David = {}
dict2Mattias = {}
dict2Erland = {}
dict2Anna = {}

for i in range(numberOfLines-1):
    currentLine = lines[i]
    nextLine = lines[i+1]
    goodLine = True
    for year in [2013, 2014, 2015, 2016, 2017]:
        if str(year) in nextLine:
            goodLine = False
    if 'http' in nextLine:
        goodLine = False
    elif SIFT_CALLS:
        if 'has called' in nextLine:
            goodLine = False
        if 'har ringt' in nextLine:
            goodLine = False
    elif nextLine == '':
        goodLine = False
    elif '@facebook' in nextLine:
        goodLine = False
        
    if goodLine:
        if 'David Montgomery' in currentLine or DAVID_ID in currentLine:
            messagesDavid.append(lines[i+1])
        elif 'Matilda Nyholm' in currentLine:
            messagesMatilda.append(lines[i+1])
        elif 'Erland Montgomery' in currentLine or ERLAND_ID in currentLine:
            messagesErland.append(lines[i+1])
        elif 'Mattias Montgomery' in currentLine or MATTIAS_ID in currentLine:
            messagesMattias.append(lines[i+1])
        elif 'Anna Montgomery' in currentLine or ANNA_ID in currentLine:
            messagesAnna.append(lines[i+1])

"""Dictionary mapping the two last words to predict the next"""
def messageToDict2Deep(message, dictionary2):
    words = message.split(' ')
    words = list(filter(None, words))
    if len(words) > 2:
        for k in range(len(words)-2):
            newString = words[k] + ' ' + words[k+1]
            if newString not in dictionary2:
                dictionary2[newString] = {}
            if words[k+2] not in dictionary2[newString]:
                dictionary2[newString][words[k+2]] = 1
            else:
                dictionary2[newString][words[k+2]] += 1
    return dictionary2
    
"""Dictionary mapping the last word to find the next"""
def messageToDict(message, dictionary):
    words = message.split(' ')
    if words[0] not in dictionary['beginSequence']:

        dictionary['beginSequence'][words[0]] = 1
    else:
        dictionary['beginSequence'][words[0]] += 1
    for k in range(len(words)-1):
        if words[k] not in dictionary:
            dictionary[words[k]] = {}
        if words[k+1] not in dictionary[words[k]]:
            dictionary[words[k]][words[k+1]] = 1
        else:
            dictionary[words[k]][words[k+1]] += 1
    return dictionary 

def generateNextWord1(previousWord, dictionary):
    if previousWord in dictionary:
        possWords = list(dictionary[previousWord].items())
        s = 0        
        for item in possWords:
            s += item[1]
        r = random.uniform(low=0, high=s)
        runSum = 0
        for item in possWords:
            runSum += item[1]
            if runSum > r:
                nextWord = item[0]
                break
    else:
        nextWord = 'terminated'
    return nextWord

def generateNextWord2(prepreviousWord, previousWord, dictionary2):
    nextWord = 'terminated2'    
    previous2 = prepreviousWord + ' ' + previousWord
    if previous2 in dictionary2:
        if len(dictionary2[previous2]) > 1:
            possWords = list(dictionary2[previous2].items())
            s = 0
            for item in possWords:
                s += item[1]
            r = random.uniform(low=0, high=s)
            runSum = 0
            for item in possWords:
                runSum += item[1]
                if runSum > r:
                    nextWord = item[0]
                    break
    return nextWord
    
def generateStartWord(dictionary):
    possWords = list(dictionary['beginSequence'].items())
    s = 0    
    for item in possWords:
        s += item[1]
    r = random.uniform(low=0, high=s)
    runSum = 0
    for item in possWords:
        runSum += item[1]
        if runSum > r:
            firstWord = item[0]
            break
    return firstWord

def generateSentence(N, dictionary, dictionary2, name):
    firstWord = generateStartWord(dictionary)    
    connector = ' '
    sentence = [firstWord]
    d = []
    
    for _ in range(N):
        if len(sentence) > 1:
            nextWord = generateNextWord2(sentence[-2], sentence[-1], dictionary2)
            if nextWord == 'terminated2':
                nextWord = generateNextWord1(sentence[-1], dictionary)
                d.append(1)
                if nextWord == 'terminated':
                    break
            else:
                d.append(2)
        else:
            nextWord = generateNextWord1(sentence[-1], dictionary)
            if nextWord == 'terminated':
                break
            else:
                d.append(1)
        sentence.append(nextWord)
    print(d)
    return name + ': ' + connector.join(sentence)

def generateConversation(names, length, dictionaries, dictionaries2):
    conv = ''
    for _ in range(length):
        personChoice = random.choice(range(len(names)))
        newSentence = generateSentence(MAX_LENGTH, dictionaries[personChoice], \
                                      dictionaries2[personChoice], names[personChoice])
        conv += '\n\n'+ newSentence
    return conv

for message in messagesMatilda:
    dictMatilda = messageToDict(message, dictMatilda)
    dict2Matilda = messageToDict2Deep(message, dict2Matilda)
for message in messagesDavid:
    dictDavid = messageToDict(message, dictDavid)    
    dict2David = messageToDict2Deep(message, dict2David)
for message in messagesMattias:
    dictMattias = messageToDict(message, dictMattias)
    dict2Mattias = messageToDict2Deep(message, dict2Mattias)
for message in messagesAnna:
    dictAnna = messageToDict(message, dictAnna)
    dict2Mattias = messageToDict2Deep(message, dict2Anna)
for message in messagesErland:
    dictErland = messageToDict(message, dictErland)
    dict2Erland = messageToDict2Deep(message, dict2Erland)
    
print(generateConversation(['Mattias', 'Matilda', 'Anna', 'Erland', 'David'], 10, \
                    [dictMattias, dictMatilda, dictAnna, dictErland, dictDavid], \
                    [dict2Mattias, dict2Matilda, dict2Anna, dict2Erland, dict2David]))











