import pandas as pd  # 导入Pandas
import pickle  # 导入序列化工具Pickle

df_ads = pd.read_csv('易速鲜花微信软文.csv')  # 导入数据集

df_ads['转发数'].fillna(df_ads['点赞数'], inplace=True)  # 一种补值方法

X = df_ads.drop(['浏览量'], axis=1)  # 特征集，Drop掉标签相关字段
y = df_ads.浏览量  # 标签集

from sklearn.linear_model import LinearRegression  # 导入线性回归模型

regressor = LinearRegression()  # 创建线性回归模型

regressor.fit(X, y)  # 拟合模型

pickle.dump(regressor, open('model.pkl', 'wb'))  # 序列化模型（就是存盘）

model = pickle.load(open('model.pkl', 'rb'))  # 反序列化模型（就是再导入模型）

print(model.predict([[300, 800]]))  # 进行一个预测
