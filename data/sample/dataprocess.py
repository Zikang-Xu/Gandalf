import pandas as pd

# 读取 CSV 文件
data = pd.read_csv('pro_data.csv')

# 找出在所有时间戳下都有值的列
complete_columns = data.columns[data.notnull().all()]

print(len(complete_columns))
# 输出含有完整数据的列到新文件
complete_data = data[complete_columns]
complete_data.to_csv('complete_metrics.csv', index=False)

# 输出找到的列名
print(f"所有时间戳下都有值的列已输出到 complete_metrics.csv 文件中。")
print(f"这些列名为: {', '.join(complete_columns)}")


# # 将 'timestamp' 列转换为 datetime 类型
# data['timestamp'] = pd.to_datetime(data['timestamp'])
#
# # 获取时间范围
# start_time = data['timestamp'].min()
# end_time = data['timestamp'].max()
#
# # 生成完整的时间戳范围
# full_range = pd.date_range(start=start_time, end=end_time, freq='1min')
#
# # 检查每个 metric 列是否有缺失的时间戳
# not_missing_metrics = []
# for column in data.columns[1:]:  # 从第二列开始检查，第一列是时间戳列
#     missing_count = full_range.difference(data[data[column].notnull()]['timestamp']).size
#     if missing_count == 0:
#       not_missing_metrics.append(column)
#
# # 输出缺失的 metric 到新文件
# if not_missing_metrics:
#     # 选取包含缺失的 metric 列并输出到新文件
#     missing_data = data[['timestamp'] + not_missing_metrics]
#     missing_data.to_csv('not_missing_metrics.csv', index=False)
#     print("缺失的 Metric 已输出到 not_missing_metrics.csv 文件中。")
#     print(f"共有 {len(not_missing_metrics)} 个 Metric 不缺失数据，占总数的 {(len(not_missing_metrics) / (len(data.columns) - 1)) * 100:.2f}%。")
# else:
#     print("没有发现缺失数据的 Metric。")


