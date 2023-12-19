import numpy as np

def detect_outliers(data, threshold=3):
    """
    使用 x_sigma 方法检测异常值

    参数:
    data: 输入的数据列表或数组
    threshold: 定义异常值的阈值，默认为 3

    返回值:
    outliers: 异常值列表
    """
    mean = np.mean(data)
    std_dev = np.std(data)
    outliers = [x for x in data if abs(x - mean) > threshold * std_dev]
    return outliers

# 示例数据
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100, 200]

# 检测异常值
outliers = detect_outliers(data)

print("异常值：", outliers)
