import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import time

path_to_save = "C:/Users/UserVert/Desktop/all/sentiment_analysis_twitter/dfs/"

list_of_words = ['vacinação', 'coronavac', 'Vacina', 'vacina', 'vachina', 'Vacinação',
                              '#vacinação', '#coronavac', '#Vacina', '#vacina', '#Vacinação']

sentiment_words = ['brasil', 'brazil', 'guedes', 'bolsonaro', 'lula', 'covid', 'covid19', 'covid-19']

df = pd.read_excel("C:/Users/UserVert/Desktop/all/sentiment_analysis_twitter/dfs/1616953279.7671642_tweets.xlsx")
df = df.dropna().reset_index(drop=True)

vacina_clean = ' '.join(df['tweet_clean'].tolist()).split()
vacina_counts = Counter(vacina_clean)
vacina_common_words = [word[0] for word in vacina_counts.most_common(20)]
vacina_common_counts = [word[1] for word in vacina_counts.most_common(20)]
fig = plt.figure(figsize=(24, 12))
sns.barplot(x=vacina_common_words, y=vacina_common_counts)
plt.title(f'Most common words')
plt.show()

vacina_common_words = [word[0] for word in vacina_counts.most_common(20) if word[0] not in list_of_words]
vacina_common_counts = [word[1] for word in vacina_counts.most_common(20) if word[0] not in list_of_words]
fig_wl = plt.figure(figsize=(24, 12))
sns.barplot(x=vacina_common_words, y=vacina_common_counts)
plt.title(f'Most common words without list of words')
plt.show()

for sentiment in ['positive', 'negative']:

    text_initial = " ".join(review for review in df.tweet_clean[df['sentiment'] == sentiment])
    text = " ".join(word for word in text_initial.split())
    word_cloud = WordCloud(background_color="white").generate(text)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    text = " ".join(word for word in text_initial.split() if word not in list_of_words and word not in sentiment_words)
    word_cloud = WordCloud(background_color="white").generate(text)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    c_vec = CountVectorizer(ngram_range=(2, 3))
    # matrix of ngrams
    ngrams = c_vec.fit_transform(df['tweet_clean'][df['sentiment'] == sentiment])
    # count frequency of ngrams
    count_values = ngrams.toarray().sum(axis=0)
    # list of ngrams
    vocab = c_vec.vocabulary_
    df_ngram = pd.DataFrame(sorted([(count_values[i], k) for k, i in vocab.items()], reverse=True)
                            ).rename(columns={0: 'frequency', 1: 'bigram/trigram'})
    writer = pd.ExcelWriter(path_to_save + f'{time.time()}_{sentiment}_anagrams.xlsx', engine='xlsxwriter')
    df_ngram.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()