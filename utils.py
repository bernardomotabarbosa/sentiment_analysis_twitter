# corpus = ["I'd like an apple",
#         "An apple a day keeps the doctor away",
#         "Never compare an apple to an orange",
#         "I prefer scikit-learn to Orange",
#         "The scikit-learn docs are Orange and Blue"]
# vect = TfidfVectorizer()
# tfidf = vect.fit_transform(corpus)
# pairwise_similarity = tfidf * tfidf.T
# array = pairwise_similarity.toarray()