import urllib.request
import bs4 as BeautifulSoup
import nltk
from nltk.corpus import stopwords 
from string import punctuation

#getting the data from the wikipedia page
data = urllib.request.urlopen("https://en.wikipedia.org/wiki/Iron_Man")
article = data.read()

#The imported Article is filled with HTML tags and more
#print(article)
parse_article = BeautifulSoup.BeautifulSoup(article,'html.parser')

#finding all the P tags
paras = parse_article.find_all('p')

#looping through all the paras to get the content
content = ''
for i in paras:
    content += i.text  #i.text returns only the content in the tag

#stopwords might be already there when you import nltk so this is step is optional
nltk.download('stopwords')
stop_words = stopwords.words('english') #considering only english stopwords here

#adding '/n' to the punctiation
punctuation = punctuation + '/n'
print(punctuation)

#creating tokens to the whole content #tokens means list of words
tokens = nltk.tokenize.word_tokenize(content)

#Here we are counting the frequency of each word present in the content
#Stopwords and ounctuations are excluded
word_freq = {}
for word in tokens:    
    if word.lower() not in stop_words:
        if word.lower() not in punctuation:
            if word not in word_freq.keys():
                word_freq[word] = 1
            else:
                word_freq[word] += 1

max_freq = max(word_freq.values())

#calculating the word_frequency of each word 
for word in word_freq.keys():
    word_freq[word] = word_freq[word]/max_freq

#tokenizing the content into sentences
#List of Sentences
sent_token = nltk.tokenize.sent_tokenize(content)

sentence_scores = {}
for sent in sent_token:
    sentence = sent.split(" ")
    for word in sentence:        
        if word.lower() in word_freq.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_freq[word.lower()]
            else:
                sentence_scores[sent] += word_freq[word.lower()]



from heapq import nlargest

select_length = int(len(sent_token)*0.3)

summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

result = [word for word in summary]
summary = ' '.join(result)

print(summary)

