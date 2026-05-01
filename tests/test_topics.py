from turbo_invention.analysis.topics import cluster

def test_cluster_returns_k_groups():
    docs = ["machine learning python", "machine learning data",
            "football league win", "football team match",
            "cooking recipe pasta", "cooking baking bread"]
    labels, terms_per_cluster = cluster(docs, k=3)
    assert len(labels) == len(docs)
    assert len(terms_per_cluster) == 3
