import math

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def Gandalf():
    """
    Gandalf模型包括三个主要步骤:
    (1)
    异常检测从原始遥测数据中检测系统级故障;
    原文方式是对故障文本信息聚类后，以故障签名为单位检测异常
    我们这里直接使用性能指标数据*
    使用前12h的数据来预测1h窗口内的数据
    """

    data = pd.read_csv('data/sample/complete_metrics.csv') # 该文件中存储的是Hadoop单个节点上的性能指标数据 同时已经做好预处理

    # 将 'timestamp' 列转换为 datetime 类型
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # 显式指定时间频率为分钟级 'T'
    data.set_index(pd.date_range(start=data['timestamp'].min(), periods=len(data), freq='1T'), inplace=True)
    data.drop('timestamp', axis=1, inplace=True)

    # 选择除时间戳列外的其他数据列
    data_columns = data.columns

    # 针对每个数据列进行预测和异常检测
    anomalies = {}

    """
    使用前12小时（720个数据点）的数据来预测这一小时（60个数据点）中的异常
    """

    for col in data_columns:
        anomalies[col] = []
        for i in range(0, len(data), 60):
            if i < 720 or i + 60 >= len(data):
                continue

            # 取过去 12h 的数据用于训练
            train_data = data[col].iloc[i - 720:i]

            # 使用 Holt-Winters 模型进行训练
            model = ExponentialSmoothing(train_data, trend='add', seasonal='add', seasonal_periods=12)
            fitted_model = model.fit()

            # 对当前 1h 的数据进行预测
            forecast = fitted_model.forecast(steps=60)

            # 计算观察值与预测值之间的差异
            residual = data[col].iloc[i: i+60] - forecast.iloc[0: 60]  # 修改此行

            # 计算标准差
            std_dev = np.std(train_data)

            # 判断是否为异常点
            for j in range(0, 60):
                if abs(residual[j]) >= 4 * std_dev:
                    anomalies[col].append(data.index[i+j])
        # break

    # 输出标记为异常点的时间戳
    print("每个数据列的异常点时间戳：")
    for col, anomaly in anomalies.items():
        print(f"数据列 '{col}' 的异常点时间戳：")
        print(anomaly)

    sample_deployment = {
        "datanode_upgrade": "2023-12-09 03:00:01",
        "namenode_upgrade": "2023-12-09 05:00:01"
    } # 假设从日志中收集到升级相关的部署信息

    """
    (2)
    相关性分析识别出多个部署中检测到故障的部件;
    (2.1)集合投票
    """
    # 指定一些窗口大小 每个异常投票给发生在异常之间且在窗口内的部署
    wd = [1, 24, 72] # 假设单位为min

    # 对sample_deployment中的每个元素item:遍历所有的异常点，如果异常点发生在item的时间之前，让计数器加一

    blame = {}
    for deployment in sample_deployment:
        p1 = p2 = p3 = 0
        b = 0
        td = sample_deployment[deployment]
        print(deployment, td)
        for col, anomaly in anomalies.items():
            for tf in anomaly:
                time_difference = tf - pd.Timestamp(td)
                minutes = float(time_difference.total_seconds() / 60.0)
                if minutes < 0:
                    if abs(minutes <= 72):
                        b = b+1
                    else:
                        continue
                if minutes <= 1:
                    p1 = p1 + 1
                if minutes <= 24:
                    p2 = p2 + 1
                if minutes <= 72:
                    p3 = p3 + 1
        print(p1, p2, p3, b)

        # (2.2)时间相关
        # 给p1, p2, p3的权重分别设置0.6, 0.3, 0.1
        st = 0.6 * (math.log(p1 - b + 1) - math.log(b + 1)) + \
             0.3 * (math.log(p2 - b + 1) - math.log(b + 1)) + \
             0.1 * (math.log(p3 - b + 1) - math.log(b + 1))

        print("时间相关性st = ", st)
        blame[deployment] = st
        # (2.3)空间相关
        # 空间相关性通过计算部署过程中的故障节点占所有故障节点比例来筛选掉一些低比例的部署
        # pass

    # (2,4)指数时间衰减
    # 找到st最大的部署e
    max_key = max(blame, key=blame.get)
    print('指责分数最高的部署组件为: ', max_key)
    """
    (3)
    决策步骤评估影响范围，决定是否停止。换言之，决定该部署是否是导致故障的部署
    文中的方式是通过给每个特征的静态阈值，决策标准通过高斯判别分类器进行动态训练
    """
    my_threshold = 0
    if blame[max_key] > my_threshold:
        print("no go!")
    else:
        print("go!")
    # pass

if __name__ == '__main__':
    Gandalf()