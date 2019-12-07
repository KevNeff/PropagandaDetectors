import sys
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer,TfidfTransformer

def url_miner():
    import re
    from newspaper import Article
    try:
        article = Article(sys.argv[1])
        article.download()
        article.parse()
    except:
        print('Invalid URL')
        sys.stdout.flush()
        exit()
    text = article.text.split('\n')
    corpus = []
    regex = re.compile('[\"#$%&\\\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c]')
    for line in text:
        if line != '':
            corpus.append(regex.sub('', line))

    if len(corpus) == 0:
        print('URL has no text')
        sys.stdout.flush()
        exit()
    return corpus

def modelLoader():
    import pickle
    loaded_vec = TfidfVectorizer(stop_words='english',lowercase=True,vocabulary=pickle.load(open("feature.pkl", "rb")))
    with open("trial.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    return loaded_vec, pickle_model

def inject_to_server(predictions, corpus):
    count = 0
    hasP = False
    for prediction in predictions:
        if prediction == 'propaganda':
            print(corpus[count] + '\n')
            hasP = True
        count += 1
    if hasP == False:
        print('No Propaganda')
    sys.stdout.flush()
    exit()

def Main():
    word_vector, model = modelLoader()
    corpus = url_miner()
    samples = word_vector.fit_transform(corpus)
    predictions = model.predict(samples)
    inject_to_server(predictions, corpus)

    print('Failed')
    sys.stdout.flush()
if __name__ == "__main__":
    Main()
