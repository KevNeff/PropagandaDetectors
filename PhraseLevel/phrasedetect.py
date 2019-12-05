import os
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn import metrics
def create_t3df():
    trainpath = 'D:/Desktop/datasets-v5/tasks-2-3/train'
    t3df = pd.DataFrame(columns=['article', 'label', 'startc', 'endc', 'text'])
    dfi = 0
    for filename in os.listdir(trainpath):
        namesplit = filename.split('.')
        if namesplit[1] == 'task3':
            lblfile = open(trainpath + '/' + filename, 'r', encoding="utf-8")
            with open(trainpath + '/' + namesplit[0] + '.txt', 'r', encoding="utf-8")as artfile:
                arttxt = artfile.read()
            for line in lblfile:
                linesplit = line.split()#0 article, #1 label, #2 starting character, #3 ending character
                if linesplit != []:
                    phrasetxt = arttxt[int(linesplit[2]):int(linesplit[3])]
                    phrasetxt = re.sub(r'[^A-Za-z0-9 ]+', '', phrasetxt.strip('\'s'))
                    t3df = t3df.append(pd.Series([int(linesplit[0]), linesplit[1], int(linesplit[2]), int(linesplit[3]), phrasetxt], index=t3df.columns, name=dfi))

                    dfi += 1
            lblfile.close()

    t3df.to_json('task3_dataframe.json')
    return t3df

def load_t3df():
    t3file = 'task3_dataframe.json'
    if os.path.exists(t3file):
        t3df = pd.read_json(t3file)
    else:
        t3df = create_t3df()
    return t3df

def text2file():
    text = t3df['text']
    textfile = open('text.txt', 'w')
    for line in text:
        textfile.write(line + "\n")
    textfile.close()
    print(text)

def prepare_bert_data():
    t3df = load_t3df()
    t3df['id'] = t3df['article'] + t3df['startc']
    bert_df_all = pd.DataFrame({'guid': t3df['id'], 'label': t3df['label'], 'text': t3df['text']})
    bert_train, bert_test = train_test_split(bert_df_all, test_size = .3, shuffle = False)
    bert_df = pd.DataFrame({'guid': bert_train['guid'], 'label': bert_train['label'], 'alpha': ['a']*bert_train.shape[0], 'text': bert_train['text']})
    train_df, dev_df = train_test_split(bert_df, test_size=0.05)
    test_df = pd.DataFrame({'guid': bert_test['guid'], 'label': bert_test['label'], 'alpha': ['a']*bert_test.shape[0], 'text': bert_test['text']})

    train_df.to_csv('bert-master/dataset/train.tsv', sep='\t', index=False, header=False)
    test_df.to_csv('bert-master/dataset/dev.tsv', sep='\t', index=False, header=False)
    test_df.to_csv('bert-master/dataset/test.tsv', sep='\t', index=False, header=True)

def Main():
    #function to prepare dataset
    #prepare_bert_data()

    #command to run bert fine tuning in bert-master path
    #python run_classifier.py --task_name=cola --do_train=false --do_eval=true --data_dir=./dataset --vocab_file=./model/vocab.txt --bert_config_file=./model/bert_config.json --init_checkpoint=./model/bert_model.ckpt --max_seq_length=64 --train_batch_size=2 --learning_rate=2e-5 --num_train_epochs=3.0 --output_dir=./bert_output/ --do_lower_case=False --save_checkpoints_steps 10000

    #command to evaluate in bert-master path
    #python run_classifier.py --task_name=cola --do_predict=true --data_dir=./dataset --vocab_file=./model/vocab.txt --bert_config_file=./model/bert_config.json --init_checkpoint=.\bert_output\model.ckpt-5100 --max_seq_length=64 --output_dir=./bert_output/ --do_lower_case=False



    #read the original test data for the text and id
    df_test = pd.read_csv('bert-master/dataset/test.tsv', sep='\t')['label'].tolist()

    label_list = ["Appeal_to_Authority",
                  "Appeal_to_fear-prejudice",
                  "Bandwagon",
                  "Black-and-White_Fallacy",
                  "Causal_Oversimplification",
                  "Doubt",
                  "Exaggeration,Minimisation",
                  "Flag-Waving",
                  "Loaded_Language",
                  "Name_Calling,Labeling",
                  "Obfuscation,Intentional_Vagueness,Confusion",
                  "Red_Herring",
                  "Reductio_ad_hitlerum",
                  "Repetition",
                  "Slogans",
                  "Straw_Men",
                  "Thought-terminating_Cliches",
                  "Whataboutism"]
    label_map = {}
    label_ids = []
    for (i, label) in enumerate(label_list):
        label_map[label] = i
        label_ids.append(i)

    truths = []
    for truth in df_test:
        truths.append(int(label_map[truth]))

    #read the results data for the probabilities
    df_result = pd.read_csv('bert-master/bert_output/test_results.tsv', sep='\t', header=None)
    #create a new dataframe
    df_map_result = pd.DataFrame({'truth': ['a']*df_result.shape[0],
                                  'label': df_result.idxmax(axis=1)})
    #view sample rows of the newly created dataframe
    #print(df_map_result.sample(10))
    predicts = df_map_result['label'].tolist()

    avg = 0
    for i in range(len(predicts)):
        predicts[i] = int(predicts[i])
        if predicts[i] == truths[i]:
            avg += 1

    #print(avg/len(predicts))
    average = metrics.recall_score(truths, predicts, average='weighted')
    precision = metrics.precision_score(truths, predicts, average='weighted')
    recall = metrics.recall_score(truths, predicts, average='weighted')
    f1 = metrics.f1_score(truths, predicts, average='weighted')
    print("average:")
    print(average)
    print("precision:")
    print(precision)
    print("recall:")
    print(recall)
    print("f1:")
    print(f1)


if __name__ == "__main__":
    Main()
