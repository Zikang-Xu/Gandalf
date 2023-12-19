from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
def get_txt_data():
    # 日志信息存储在elasticsearch中
    # 连接到 Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])  # 替换为你的 Elasticsearch 地址和端口
    # 从 Elasticsearch 中检索日志信息
    # 假设日志存储在名为 'log_index' 的索引中，字段为 'message'
    index_name = 'log_index'
    field_name = 'message'
    query = {
        "query": {
            "match_all": {}  # 匹配所有文档
        }
    }

    # 从 Elasticsearch 中获取所有日志消息
    response = es.search(index=index_name, body=query, size=1000)  # 调整 size 参数以获取更多文档
    logs = [hit['_source'][field_name] for hit in response['hits']['hits']]

    # 使用 TF-IDF 向量化文本数据
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(logs)

    # 应用层次聚类
    num_clusters = 5  # 假设聚类为 5 类
    cluster = AgglomerativeClustering(n_clusters=num_clusters, affinity='cosine', linkage='average')
    cluster.fit_predict(X)

    # 输出每个日志的聚类标签
    for i, log in enumerate(logs):
        print(f"Log {i + 1} belongs to cluster: {cluster.labels_[i]}")

def get_ts_data():
    # 时序数据存储在influxDB中
    pass