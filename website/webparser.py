import sys
from newspaper import Article
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer,TfidfTransformer
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

argerror = -1
if sys.argv[0] == 0:
    print('URL Error')
    sys.stdout.flush()
    exit()

sys.stdout.flush()

#url = 'https://hackernoon.com/a-guide-to-open-enrollment-and-the-health-insurance-marketplace-931h32j1'
url = sys.argv[1]

try:
    article = Article(url)
    article.download()
    article.parse()
except:
    print('URL Error')
    sys.stdout.flush()
    exit()
f = open('article.txt', 'w')
f.write(article.text)
f.close()

lines = []
fp = open('article.txt', 'r')
for line in fp:
    lines.append(line + '\n')
fp.close()

loaded_vec = TfidfVectorizer(stop_words='english',lowercase=True,vocabulary=pickle.load(open("feature.pkl", "rb")))

corpus = open("article.txt")
transformed2 = loaded_vec.fit_transform(corpus)
with open("trial.pkl", 'rb') as file:
    pickle_model = pickle.load(file)
pred = pickle_model.predict(transformed2)

count = 0
for label in pred:
    if label == 'propaganda':
        print(lines[count] + '\n')
    count += 1

sys.stdout.flush()
exit()