import nltk
import csv
import string
import re
from nltk.corpus import stopwords
from collections import Counter
from nltk import ngrams
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


non_speaker = re.compile('[A-Za-z]+: (.*)')

def untokenize(ngram):
    tokens = list(ngram)
    return "".join([" "+i if not i.startswith("'") and \
                             i not in string.punctuation and \
                             i != "n't"
                          else i for i in tokens]).strip()

#get more frequency phrases
def extract_phrases(text, phrase_counter, length):
    #Remove stop words
    stop = set(stopwords.words('spanish'))
    word = [i for i in text.lower().split() if i not in stop]
    words = " ".join(str(x) for x in word)


    for sent in nltk.sent_tokenize(words):
        strip_speaker = non_speaker.match(sent)
        if strip_speaker is not None:
            sent = strip_speaker.group(1)
        words = nltk.word_tokenize(sent)
        for phrase in ngrams(words, length):
            if all(word not in string.punctuation for word in phrase):
                phrase_counter[untokenize(phrase)] += 1

phrase_counter = Counter()

#open file
with open("titulos.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter=",")


    next(reader)
    for sentence in reader:

        extract_phrases(str(sentence[4]), phrase_counter, 3)



most_common_phrases = phrase_counter.most_common(150)

#Write output in a file
f = open('outFrequentlyPhrases.txt', 'w')
for k,v in most_common_phrases:
    print ('{0: <5}'.format(v), k)
    print >> f, ('{0: <5}'.format(v), k)

f.close()
