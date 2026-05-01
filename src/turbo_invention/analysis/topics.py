from __future__ import annotations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def cluster(docs: list[str], k: int = 5) -> tuple[list[int], list[list[str]]]:
    vec = TfidfVectorizer(stop_words="english", max_features=2000)
    X = vec.fit_transform(docs)
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    labels = km.labels_.tolist()
    terms = vec.get_feature_names_out()
    centroids = km.cluster_centers_.argsort()[:, ::-1]
    top = [[terms[i] for i in centroids[c, :8]] for c in range(k)]
    return labels, top
