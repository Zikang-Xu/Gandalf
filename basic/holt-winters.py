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


