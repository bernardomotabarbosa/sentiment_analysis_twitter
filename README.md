# Twitter sentiment analysis


This project was created with the aim of studying people's feelings about the vaccine theme.
In Portuguese tweets were extracted with words related to that theme, the tweets were cleaned and classified with the TextBlob package 
and descriptive analyzes were made, the code can be adapted to analyze any topic.

# Installation (Recommended to use python 3.9)

```
git clone https://github.com/bernardomotabarbosa/sentiment_analysis_twitter.git
cd sentiment_analysis_twitter
conda create --name envname
conda activate envname
conda install pip
pip install -r requirements.txt
```

# Usage
```
python twitter_extract.py --list vacinação vacina coronavac -n 1 -p "C:/Users/UserVert/Desktop/all/sentiment_analysis_twitter/dfs/"
```

# Result

The most common words found when cleaning and deleting the list of words used in the search were:

![Words most commum](https://github.com/bernardomotabarbosa/sentiment_analysis_twitter/blob/master/figures/word_cloud_positive_clean.png?raw=true)

The positive and negative word clouds were:

![Cloud positive](https://github.com/bernardomotabarbosa/sentiment_analysis_twitter/blob/master/figures/most_comm_words_without_list_of_words.png?raw=true)
![Cloud negative](https://github.com/bernardomotabarbosa/sentiment_analysis_twitter/blob/master/figures/word_cloud_negative_clean.png?raw=true)

# Getting access to the twitter api


I removed the access keys for the twitter API from the code.
To get these keys, just follow the instructions on the link: https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

After obtaining the keys, just add at the beginning of the class on lines 35 to 38 on twitter_extract.py