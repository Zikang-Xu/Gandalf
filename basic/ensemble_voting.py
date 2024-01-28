import pandas as pd
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'Timestamp_fault': [
        '2023-12-10 08:00:00',
        '2023-12-10 08:10:00',
        '2023-12-10 08:30:00',
        '2023-12-10 09:00:00'
    ],
    'Component_deployed': [
        'Component_A',
        'Component_B',
        'Component_C',
        'Component_D'
    ],
    'Node': [
        'Node_1',
        'Node_2',
        'Node_1',
        'Node_3'
    ]
}

df = pd.DataFrame(data)
df['Timestamp_fault'] = pd.to_datetime(df['Timestamp_fault'])

# 初始化投票和否决的字典
votes = {}
vetoes = {}

# 初始化窗口大小
window_sizes = [1, 24, 72]  # 以小时为单位

# 计算故障与部署组件之间的关系
for index, row in df.iterrows():
    fault_timestamp = row['Timestamp_fault']
    component = row['Component_deployed']
    node = row['Node']

    for window_size in window_sizes:
        # 计算年龄
        age = fault_timestamp - timedelta(hours=window_size)

        # 对齐投票和否决
        if age not in votes:
            votes[age] = {}
            vetoes[age] = {}

        # 统计投票和否决
        for i, window in enumerate(window_sizes):
            if window <= window_size:
                if age not in votes[age]:
                    votes[age][i] = 0
                    vetoes[age][i] = 0

                # 根据条件进行投票
