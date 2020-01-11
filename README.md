# Propaganda Detection in News Articles
 

## Introduction
A lot of importance is placed on detecting fake-news in present times. As seen in the venn diagram[1] on the left, not all fake news impact us. So as to create news that cause impact, journalists use psychological and rhetorical techniques called propaganda. Propaganda is a technique, especially of a biased or misleading nature, used to promote or publicize a particular political cause or point of view. Looking at the picture on the left[5], we realize that even true images if published with malicious intent can cause damaging effects.
With the rise in social media, these propagandistic articles reach millions of people in a short time. As propagandistic content try to bias our thoughts, it is very difficult to identify their presence.
The aim of this project is to detect propaganda in news articles with focus on the impact, rather than factual correctness. We classify documents and sentences as propagandistic or not and identify the propaganda technique used at a phrase level.

<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/1.png" alt="[5]" width="400">


## Dataset
The data for this project is obtained from Hack the News Datathon Case – Propaganda Detection [2] challenge. The data is divided into three parts.
1. Propaganda detection at article level, which consists of news articles and labels as propaganda or non-propaganda.
2. Propaganda detection at sentence level, which consists of propaganda or non-propaganda label associated with each sentence in a news article.
3. Propaganda type recognition at phrase level, which consists of the type of propaganda for phrases in news articles.

## Exploratory Data Analysis
The below plots help us understand the proportion of propaganda and non-propaganda labels at different granularities.
From the first two plots, we see that the percentage of input that belongs to the class Propaganda is less that 25 percent at both the article and sentence levels. Additionally, we can see that there are about 18 propaganda techniques at phrase level.

<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/2.jpg" alt="alt text" width="600">

## Implementation

### Article Level
This was the basic starting level block of the propaganda detection. All common operations were performed at this level to be substituted to further levels. The following tasks were performed:
..*	Tokenized the words, converted to lowercase, stemmed them, removed stopwords
..*	Experimented with various classifiers like, Naive Bayes, Logistic regression, Support Vector Classifier, MLP Classifier, Passive Aggressive and LSTM and vectorizers like Count vectorizers and TFIDF. 
..*	Experimented with several hyperparameters like mindf, maxdf, analysers and, n-grams on the classifiers.
..*	We further annotated question marks (?) and exclamation marks (!) and that improved performance of the model.

### Sentence Level
With sentence as the granualarity level, we started off with TF-IDF feature extraction to train our classification models. The results were not impressive and improvement in features was required to make the models learn the data better. Included six additional features[3] along with TF-IDF features to create a feature union, which was further used to train the models. The features are briefly described below.
..*	Exclamations - Exclamations indicate exaggerations in propaganda sentences. 
..*	Plural and singular pronouns - Use of plural pronouns indicate the expression of opinion of the author and may influence the public in a similar way.
..*	Confusing words - Used wordnet data to check synonym nest in sentence.
..*	Loaded language - List of words with strong emotional implications.
..*	Polarity - Used textblob to compute how positive or negative a sentence is.
After having obtained the feature union, trained various classifiers like Logistic Regression, Passive Aggressor, and LSTM to perform classification at sentence level.

<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/3.png" alt="alt text" width="600">

### Phrase Level
At the phrase level, instead of classifying whether on not we chose BERT as our model which stands for Bidirectional Encoder Representations from Transformers. In other words, texts are fed in forwards and in reverse into a transformer encoder. A number of choices and techniques were used to tune this model.
..*	Pretrained weights - Pretrained weights exist that have been trained on a very large corpus in a number of ways. 
..*	Cases - We chose pretrained weights trained with cases to keep as much context as possible within the short phrases.
..*	Whole word maskings - This technique improves the robustness of models and increases the variety of the corpus. 
..*	Tokenization - Word Piece is an unsupervized word tokenization technique which tokenizes words and common subparts of words parts and is not limited to finding prefix or suffix word parts. 
..*	Fine tuning - Finally, with a model, phrases extracted, and phrase texts tokenized, we began the fine tuning process of BERT. Best performance is not achieved through completely retraining this model on a small corpus, but leveraging learned features to classify new labels. While this is a slow training process, with BERT, many tasks only take a few epochs to converge, with our model performance maximizing in three.
 
<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/4.png" alt="alt text" width="600">

## Live Website Demo
The live website can accessed at [propdetect.net](http://propdetect.net/)! Propdetect.net implements the PassiveAggressive model trained at the article level.

Below shows how the website may be used and a result demonstrating loaded language.

<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/6.PNG" alt="alt text" width="400">
<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/7.PNG" alt="alt text" width="400">

## Propaganda Techniques
The following are the propaganda techniques[4] we classified our phrases into :
1.	Presenting Irrelevant Data (Red Herring): Introducing irrelevant material to the issue being discussed, so that everyone's attention is diverted away from the points made. 
2.	Misrepresentation of Someone's Position (Straw Man): When an opponent's proposition is substituted with a similar one which is then refuted in place of the original proposition. 
3.	Whataboutism: A technique that attempts to discredit an opponent's position by charging them with hypocrisy without directly disproving their argument. 
4.	Causal Oversimplification : Assuming a single cause or reason when there are actually multiple causes for an issue. It includes transferring blame to one person or group of people without investigating the complexities of the issue 
5.	Obfuscation, Intentional vagueness, Confusion : Using words which are deliberately not clear so that the audience may have its own interpretations. 
6.	Appeal to authority : Stating that a claim is true simply because a valid authority or expert on the issue said it was true, without any other supporting evidence offered. We consider the special case in which the reference is not an authority or an expert in this technique, although it is referred to as Testimonial in literature. 
7.	Black-and-white Fallacy, Dictatorship: Presenting two alternative options as the only possibilities, when in fact more possibilities exist. As an the extreme case, tell the audience exactly what actions to take, eliminating any other possible choices (Dictatorship). 
8.	Name calling or labeling: Labeling the object of the propaganda campaign as either something the target audience fears, hates, finds undesirable or loves, praises. 
9.	Loaded Language: Using specific words and phrases with strong emotional implications (either positive or negative) to influence an audience.
10.	Exaggeration or Minimization: Either representing something in an excessive manner: making things larger, better, worse (e.g., "the best of the best", "quality guaranteed") or making something seem less important or smaller than it really is (e.g., saying that an insult was just a joke). 
11.	Flag-waving: Playing on strong national feeling (or to any group; e.g., race, gender, political preference) to justify or promote an action or idea 
12.	Doubt: Questioning the credibility of someone or something. 
13.	Appeal to fear/prejudice: Seeking to build support for an idea by instilling anxiety and/or panic in the population towards an alternative. In some cases the support is built based on preconceived judgements. 
14.	Slogans: A brief and striking phrase that may include labeling and stereotyping. Slogans tend to act as emotional appeals. 
15.	Thought-terminating cliché: Words or phrases that discourage critical thought and meaningful discussion about a given topic. They are typically short, generic sentences that offer seemingly simple answers to complex questions or that distract attention away from other lines of thought. 
16.	Bandwagon: Attempting to persuade the target audience to join in and take the course of action because "everyone else is taking the same action".
17.	Reductio ad hitlerum: Persuading an audience to disapprove an action or idea by suggesting that the idea is popular with groups hated in contempt by the target audience. It can refer to any person or concept with a negative connotation. 
18.	Repetition: Repeating the same message over and over again so that the audience will eventually accept it. 

## Results and Discussions
The results are tabulated for several classifiers that were experimented with different vectorizers and hyperparameters. Along with accuracies, F1 scores are measured to better determine the performance of the classifiers. 
From the below table, we see that Passive Aggressive classifier has performed the best at article level as it penalizes wrong classification and thus works to bring up the F1 score rather than accuracy. Key insight is that rather a simpler method worked better than a complex one for this task.
From the various models that were trained, LSTM is observed to have the best F1 score for classification tasks at sentence level as LSTM learns the long-term context or dependencies between symbols in the data, which is essential to identify propaganda at lower granualirites.
BERT being bidirectional can have a deeper sense of language context and flow than single direction models. This contextual learning of relation between words helps identify minor differences that are present between different propaganda techniques.
The problem becomes tougher to solve as the data becomes more granular and this is evident from the difference in F1 scores at article, sentence, and phrase levels. Additionally, at the phrase level, the problem is not binary classification anymore as there are 18 propaganda techniques that act as labels. These 18 techniques are quite similar in certain cases resulting in missclassifications.
 
<img src="https://github.com/KevNeff/PropagandaDetectors/blob/master/README_images/5.png" alt="alt text" width="600">

## Challenges
During the course of the project, we faced several challenges and some of them are highlighted below.
1. Challenges with the the dataset. There is a class imbalance in the dataset as seen in the Explorative Data Analysis section. With less than 25% of input belonging to propaganda class, it was tougher to train the models, since machine learning models train on accuracy and high accuracy can be achieved by a bad model in such skewed data-sets.
2. Feature engineering. Along with conventional TF-IDF features, we explored various other ways of extracting features to enrich the performance of the models.
3. One major challenge at the phrase level is the granularity of texts, and class imbalance. With loaded language often being between two to four words, the classification of other short, yet less frequent phrases takes a hit and only compounds the difficulty of classifying phrases this short.


## Future Work
1. Enhance model performance by exploring other algorithms with hyperparameter tuning.
2. Serialize the model. For an article, begin with detecting propaganda at article level and drill down to sentence and phrase levels.
3. Use ensemble techniques for better performance.


## References
[1] [Towards Impact Scoring of Fake News](https://www.albany.edu/~sp191221/publications/Towards_Impact_Scoring_of_Fake_News.pdf): Shivam B. Parikh, Vikram Patil, Ravi Makawana and Pradeep K. AtreyAlbany Lab for Privacy and Security, College of Engineering and Applied SciencesUniversity at Albany, State University of New York, Albany, NY, USA

[2] [Data Science Society: Hack the News Datathon Case – Propaganda Detection](https://www.datasciencesociety.net/hack-news-datathon-case-propaganda-detection/)

[3] [Data Science Society:Detecting Propaganda on Sentence Level](https://www.datasciencesociety.net/detecting-propaganda-on-sentence-level/)

[4] [QCRI: Propaganda Technique Definitions](https://propaganda.qcri.org/annotations/definitions.html)

[5] [13 Photos Demonstrate How Media Gives A False Idea Of The Truth](https://www.reckontalk.com/how-media-gives-a-false-idea-of-the-truth/)

## Team Members
[Kevin McNeff](https://github.com/KevNeff/)

[Monika Daryani](https://github.com/monikadaryani)

[Prathiksha R Prasad](https://github.com/PRATHIKSHA1995)


# Thank you!
