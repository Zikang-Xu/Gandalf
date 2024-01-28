import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def holtwinters(data):
    # 拟合 Holt-Winters 模型
    model = ExponentialSmoothing(data, trend='add', seasonal='add', seasonal_periods=12)
    fitted_model = model.fit()
    # 进行预测
    forecast = fitted_model.forecast(12)  # 预测未来 12 个时间点
    

# 创建示例时间序列数据
np.random.seed(0)
dates = pd.date_range('2023-01-01', periods=100)
data = np.random.randn(100)
ts = pd.Series(data, index=dates)

# 拟合 Holt-Winters 模型
model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=12)
fitted_model = model.fit()

# 进行预测
forecast = fitted_model.forecast(12)  # 预测未来 12 个时间点

# 可视化结果
plt.figure(figsize=(10, 6))
plt.plot(ts, label='Actual Data')
plt.plot(fitted_model.fittedvalues, label='Fitted Values')
plt.plot(forecast, label='Forecast')
plt.legend()
plt.title('Holt-Winters Forecast')
plt.show()



# 生成示例数据（替换为你的实际数据）
# 假设时间序列数据存储在名为 'data' 的 DataFrame 中，'value' 列包含数值数据
# 'timestamp' 列包含时间戳数据
# 生成时间范围（720个时间戳）
date_range = pd.date_range(start='2023-01-01', periods=720, freq='H')

# 生成随机数据（720个数据点）
value_data = np.random.randn(720)  # 这里用随机数据代替

# 创建 DataFrame
data = pd.DataFrame({'timestamp': date_range, 'value': value_data})

# 将时间列设置为索引
data.set_index('timestamp', inplace=True)

# 划分数据集为训练集和测试集
train_data = data.iloc[:500]  # 使用前面的500个数据点作为训练集
test_data = data.iloc[500:]   # 使用后面的数据进行测试

# 使用 Holt-Winters 模型进行训练
model = ExponentialSmoothing(train_data['value'], trend='add', seasonal='add', seasonal_periods=24)
fitted_model = model.fit()

# 对测试集进行预测
forecast = fitted_model.forecast(steps=len(test_data))

# 计算残差（观察值与预测值之间的差异）
residuals = test_data['value'] - forecast

# 计算标准差
std_dev = np.std(residuals)

# 标记异常点
anomalies = test_data[np.abs(residuals) > 4 * std_dev]

print("Anomalies Detected:")
print(anomalies)
