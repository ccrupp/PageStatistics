from bs4 import BeautifulSoup
import operator
import string
import urllib.request
import math
import re

def freqFourLetterWords(url):
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    paragraphs = soup.find_all('p')
    fourWordDict = {}
    for p in paragraphs:
        pText = p.get_text()
        pattern = re.compile("\W")
        pText = re.sub(pattern, " ", pText)
        words = pText.split()

        for word in words:
            word = word.lower()
            if len(word) == 4:
                if (word in fourWordDict.keys()):
                    fourWordDict[word] += 1
                else:
                    fourWordDict[word] = 1
    sortedDict = sorted(fourWordDict.items(), key=operator.itemgetter(1), reverse=True)
    mystring = ""
    for item in sortedDict:
        mystring += (item[0] + "," + str(item[1]) + "\n")
    return mystring
print (freqFourLetterWords('https://en.wikipedia.org/wiki/Data_science'))

def freqFourLetterWordsNoStopWords(url):
    #Function that calculates the frequencies of four letter words without including stopwords.
    stopWords = open("stop_words.txt", "r")
    stopWords = stopWords.read()
    stopWords = stopWords.split("\n")
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    paragraphs = soup.find_all('p')
    text = ""
    for p in paragraphs:
        pText = p.get_text()
        pattern = re.compile("\W")
        pText = re.sub(pattern, " ", pText)
        words = pText.split()
        text += pText
    for word in stopWords:
        word = word.lower()
        pattern = re.compile(r"\s" + word + "\s", re.IGNORECASE)
        text = re.sub(pattern, " ", text)
    allWords = text.split()
    fourWordDict = {}
    for word in allWords:
        word = word.translate(str.maketrans('', '', string.punctuation))
        word = word.lower()
        if len(word) == 4:
            if (word in fourWordDict.keys()):
                fourWordDict[word] += 1
            else:
                fourWordDict[word] = 1
    sortedDict = sorted(fourWordDict.items(), key=operator.itemgetter(1), reverse=True)
    mystring = ""
    for item in sortedDict:
        mystring += (item[0] + "," + str(item[1]) + "\n")
    return mystring
print (freqFourLetterWordsNoStopWords('https://en.wikipedia.org/wiki/Data_science'))

def linkTexts(url):
    #Function that finds all links on a webpage and prints the link's text
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link)
    urls = []
    linkTexts = []
    for link in links:
        linkUrl = link["href"]     # filter for html pages with absolute path
        if linkUrl not in urls:
            urls.append(linkUrl)
        linkText = link.get_text().strip()
        if linkText == "":
            linkTexts.append("\n")
        if linkText not in linkTexts:
            linkTexts.append(linkText)
    print ("URL")
    print ("URL Text")
    for i in range(len(urls)):
        print (urls[i])
        print (linkTexts[i])
linkTexts("http://google.com")


def pageStats(urls):
    #Function that calculates statistics such as word frequencies, IDF, and TF-IDFs for a list of URLS
    containsStatistics = 0
    containsAnalytics = 0
    containsData = 0
    containsScience = 0
    urls = open("urls.txt", "r")
    urls = urls.readlines()
    urls = urls[0:3]

    ##First loop solely for calculating IDFS
    for url in urls:
        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, "lxml")
        paragraphs = soup.find_all('p')
        text = ""
        # Creates a string with all paragraph text
        for p in paragraphs:
            pText = p.get_text()
            text += pText
        text = text.lower()

        # Replaces all punctuation with a space
        pattern = re.compile("[\W ]+")
        text = re.sub(pattern, " ", text)
        words = text.split(' ')
        frequencies = {"statistics": 0, "analytics": 0, "data": 0, "science": 0}
        for word in words:
            if word in frequencies.keys():
                frequencies[word] += 1
        if frequencies["statistics"] >= 1:
            containsStatistics += 1
        if frequencies["analytics"] >= 1:
            containsAnalytics += 1
        if frequencies["data"] >= 1:
            containsData += 1
        if frequencies["science"] >= 1:
            containsScience += 1
        IDFstatistics = math.log(len(urls) / containsStatistics)
        IDFanalytics = math.log(len(urls) / containsAnalytics)
        IDFdata = math.log(len(urls) / containsData)
        IDFscience = math.log(len(urls) / containsScience)

    uniqueCounts = []
    wordCounts = []
    tfStats = []
    tfAnaly = []
    tfData = []
    tfSci = []
    tfIDFStats = []
    tfIDFAnaly = []
    tfIDFData = []
    tfIDFSci = []
    ##Second loop for the rest of the stats
    for url in urls:
        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, "lxml")
        paragraphs = soup.find_all('p')
        text = ""
        # Creates a string with all paragraph text
        for p in paragraphs:
            pText = p.get_text()
            text += pText
        text = text.lower()

        # Replaces all punctuation with a space
        pattern = re.compile("[\W ]+")
        text = re.sub(pattern, " ", text)
        words = text.split(" ")
        for i in range(len(words) - 1, -1, -1):
            if words[i] == "":
                words.remove(words[i])
                i = i - 1
        wordCounts.append(len(words))
        # Counting unique words
        uniqueWords = []
        for word in words:
            if (word) not in uniqueWords:
                uniqueWords.append(word)
        uniqueCounts.append(len(uniqueWords))
        # Calculating freqs
        frequencies = {"statistics": 0, "analytics": 0, "data": 0, "science": 0}
        for word in words:
            if word in frequencies.keys():
                frequencies[word] += 1
        if frequencies["statistics"] >= 1:
            containsStatistics += 1
        if frequencies["analytics"] >= 1:
            containsAnalytics += 1
        if frequencies["data"] >= 1:
            containsData += 1
        if frequencies["science"] >= 1:
            containsScience += 1
        # The term frequency (tf) of a term (word) is defined as the number of times that term
        # t occurs in document d, divided by the total number of words in the document. The tf
        # of a word depends on the document under consideration.
        tf_statistics = frequencies["statistics"] / len(words)
        tfStats.append(tf_statistics)
        tf_analytics = frequencies["analytics"] / len(words)
        tfAnaly.append(tf_analytics)
        tf_data = frequencies["data"] / len(words)
        tfData.append(tf_data)
        tf_science = frequencies["science"] / len(words)
        tfSci.append(tf_science)
        # Find tf-idf. The tf-idf of a word is the product of the term frequency of the word in
        # document d, and its inverse document frequency. The tf-idf of a word depends on the
        # document under consideration.
        tfIDFstatistics = tf_statistics * IDFstatistics
        tfIDFStats.append(tfIDFstatistics)
        tfIDFanalytics = tf_analytics * IDFanalytics
        tfIDFAnaly.append(tfIDFanalytics)
        tfIDFdata = tf_data * IDFdata
        tfIDFData.append(tfIDFdata)
        tfIDFscience = tf_science * IDFscience
        tfIDFSci.append(tfIDFscience)
    mystring = ""
    mystring += "unique: " + str(uniqueCounts) + "\n"
    mystring += "words: " + str(wordCounts) + "\n"
    mystring += "tf statistics: " + str(tfStats) + "\n"
    mystring += "tf analytics: " + str(tfAnaly) + "\n"
    mystring += "tf data: " + str(tfData) + "\n"
    mystring += "tf science: " + str(tfSci) + "\n"
    mystring += "idf statistics: " + str(IDFstatistics) + "\n"
    mystring += "idf analytics: " + str(IDFanalytics) + "\n"
    mystring += "idf data: " + str(IDFdata) + "\n"
    mystring += "idfscience: " + str(IDFscience) + "\n"
    mystring += "tf-idf statistics: " + str(tfIDFStats) + "\n"
    mystring += "tf-idf analytics: " + str(tfIDFAnaly) + "\n"
    mystring += "tf-idf data: " + str(tfIDFData) + "\n"
    mystring += "tf-idf science: " + str(tfIDFSci) + "\n"
    # CODE USED FOR OUTPUT FILE
    # outfile = open("Q3_Part1.txt","w")
    # outfile.write(mystring)
    return mystring