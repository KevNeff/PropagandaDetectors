import sys
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer,TfidfTransformer

def url_miner():
    from newspaper import Article
    try:
        article = Article(sys.argv[1])
        article.download()
        article.parse()
    except:
        print('Invalid URL')
        sys.stdout.flush()
        exit()
    article = article.text.split('\n')
    return article

def modelLoader():
    import pickle
    loaded_vec = TfidfVectorizer(stop_words='english',lowercase=True,vocabulary=pickle.load(open("feature.pkl", "rb")))
    with open("trial.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    return loaded_vec, pickle_model

def inject_to_server(predictions, corpus):
    count = 0
    for prediction in predictions:
        if prediction == 'propaganda':
            print(corpus[count] + '\n')
        count += 1
    sys.stdout.flush()
    exit()

def Main():
    word_vector, model = modelLoader()
    corpus = url_miner()
    samples = word_vector.fit_transform(corpus)
    predictions = model.predict(samples)
    inject_to_server(predictions, corpus)

if __name__ == "__main__":
    Main()
