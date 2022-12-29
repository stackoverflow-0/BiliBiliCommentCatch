# import numpy as np
import pandas as pd
# import glob
# import re
# import jieba

#可视化库
import matplotlib.pyplot as plt
# import seaborn as sns
# from IPython.display import Image
from scipy.stats import gaussian_kde
import numpy as np
#文本挖掘库
from snownlp import SnowNLP
# from gensim import corpora,models
import matplotlib
# import pyLDAvis.gensim_models

def clean_csv(path):
    df = pd.read_csv(path)
    df = df.iloc[:,[2,5]] #取账号和评论内容
    df = df.drop_duplicates() #删除重复行

    df = df.dropna() #删除存在缺失值的行

    df.columns = ["user","comment"] #对字段进行命名
    df['comment'] = df['comment'].str.extract(r"([\u4e00-\u9fa5]+)")

    df = df.dropna()  #纯表情直接删除

    #另外，过短的弹幕内容一般很难看出情感倾向，可以将其一并过滤。
    df = df[df["comment"].apply(len)>=4]
    df = df.dropna()
    df['score'] = df["comment"].apply(lambda x:SnowNLP(x).sentiments)
    return df

def comment_senti(main_path = './comment_data/BV1sP411g7PZ_main_data.csv',reply_path = './comment_data/BV1sP411g7PZ_reply_data.csv') :
    rate= []
    df = clean_csv(main_path)
    rate += df['score'].tolist()
    df = clean_csv(reply_path)
    rate += df['score'].tolist()

    fig = matplotlib.figure.Figure(figsize=(15, 5), dpi=75)
    
    #整体情感倾向
    density = gaussian_kde(rate)

    xs = np.linspace(0,1,200)

    density._compute_covariance()
    fig.add_subplot(111).hist(rate)
    fig.axes[0].set_title('Comment sentiment analysis')
    fig.axes[0].set_xlabel("negative - positive")
    fig.axes[0].set_ylabel("comment number")
    # plt

    # plt.show()
    return fig