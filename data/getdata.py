from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import paramiko
def get_txt_data():
    # 日志信息存储在elasticsearch中
    # 连接到 Elasticsearch
    es = Elasticsearch([{'host': '10.26.43.31:8103', 'port': 9200}])  # 替换为你的 Elasticsearch 地址和端口
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

    # SSH 服务器的信息
    ssh_host = '10.26.43.31'
    ssh_port = 8103
    ssh_username = 'xzk'
    ssh_password = 'xzk201'

    # InfluxDB 服务器的信息
    influxdb_host = 'localhost'  # 因为通过 SSH 隧道，InfluxDB 将在本地访问
    influxdb_port = 8086  # 替换为 InfluxDB 的端口号
    influxdb_username = 'xzk'
    influxdb_password = 'xzk201'
    influxdb_database = 'prometheus'

    # 创建 SSH 客户端
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ssh_host, ssh_port, ssh_username, ssh_password)

    # 创建本地端口转发到 InfluxDB 服务器的连接
    transport = ssh_client.get_transport()
    local_port = 3333  # 本地端口，可以任意选择
    destination_server = (influxdb_host, influxdb_port)
    transport.open_channel("direct-tcpip", ("127.0.0.1", local_port), destination_server)

    # 连接到本地端口的 InfluxDB
    client = InfluxDBClient(host='127.0.0.1', port=local_port, username=influxdb_username,
                            password=influxdb_password, database=influxdb_database)

    # 计算过去 30 天的时间戳
    start_date = datetime.utcnow() - timedelta(days=30)
    end_date = datetime.utcnow()

    print(f"start_date: {start_date}")
    print(f"end_date: {end_date}")
    your_measurement = 'up'
    # 构建查询语句
    query = f"SELECT * FROM {your_measurement} WHERE timestamp >= '{start_date.isoformat()}' AND timestamp <= '{end_date.isoformat()}'"

    # 查询数据
    result = client.query(query)

    # 处理查询结果
    for point in result.get_points():
        print(f"Time: {point['time']}, Value: {point['value']}")  # 假设 'value' 是你的时序数据字段名

    # 关闭连接
    client.close()
    ssh_client.close()


if __name__ == '__main__':
    get_ts_data()