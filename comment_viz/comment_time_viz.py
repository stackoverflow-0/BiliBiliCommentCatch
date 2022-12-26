from matplotlib import pyplot as plt
import pandas as pds
import matplotlib
from wordcloud import WordCloud, STOPWORDS
import jieba
def comment_time_viz(level_list = ['0','1','2','3','4','5','6'], main_path = './comment_data/default_main_data.csv',reply_path = './comment_data/default_reply_data.csv'):
    
    main_comment = pds.read_csv(main_path)
    reply_comment = pds.read_csv(reply_path)
    d = dict()
    
    for line in range(main_comment.shape[0]):
        level = str(main_comment['等级'][line])
        if level not in level_list :
            continue
        
        comment_time = main_comment['发布时间'][line]
        
        if comment_time.find('天') != -1:
            comment_time = float(comment_time.split('天')[0])
        elif comment_time.find('小时') != -1 :
            comment_time = float(comment_time.split('小时')[0])/24
        elif comment_time.find('分钟') != -1 :
            comment_time = float(comment_time.split('分钟')[0])/24/60
            
        if d.get(comment_time) is None:
            d.update({comment_time:1})
        else:
            d.update({comment_time:d.get(comment_time)+1})
            
    for line in range(reply_comment.shape[0]):
        level = str(reply_comment['等级'][line])
        if level not in level_list :
            continue
        
        comment_time = reply_comment['发布时间'][line]
        
        if comment_time.find('天') != -1:
            comment_time = float(comment_time.split('天')[0])
        elif comment_time.find('小时') != -1 :
            comment_time = float(comment_time.split('小时')[0])/24
        elif comment_time.find('分钟') != -1 :
            comment_time = float(comment_time.split('分钟')[0])/24/60
        
        if d.get(comment_time) is None:
            d.update({comment_time:1})
        else:
            d.update({comment_time:d.get(comment_time)+1})
            
    from collections import OrderedDict
    d = OrderedDict(sorted(d.items()))
    
    fig = matplotlib.figure.Figure(figsize=(15, 5), dpi=75)
    fig.add_subplot(111).plot(d.keys(),d.values())
    
    return fig

def comment_level_viz(level_list = [] ,main_path = './comment_data/default_main_data.csv',reply_path = './comment_data/default_reply_data.csv'):
    
    main_comment = pds.read_csv(main_path)
    reply_comment = pds.read_csv(reply_path)
    d = dict()
    for i in range(7) :
        d.update({i:0})
    
    for line in range(main_comment.shape[0]):
        level = main_comment['等级'][line]
        d.update({level:d.get(level)+1})
            
    for line in range(reply_comment.shape[0]):
        level = reply_comment['等级'][line]
        d.update({level:d.get(level)+1})    
        
    select_list = [0] * len(d.values())
    for l in level_list:
        select_list[int(l)] = 0.05
    select_list[1] = 0.8
    from collections import OrderedDict
    
    d = OrderedDict(sorted(d.items()))
    
    labels = [ f'level{i}:{d[i]}' for i in d.keys()]
    
    fig = matplotlib.figure.Figure(figsize=(5, 5), dpi=75)
    fig.add_subplot(111).pie(d.values(),labels = labels,explode=select_list,wedgeprops=dict(width=0.4, edgecolor='w'))
    
    return fig

def word_cloud(main_path = './comment_data/default_main_data.csv',reply_path = './comment_data/default_reply_data.csv'):
    main_comment = pds.read_csv(main_path)
    reply_comment = pds.read_csv(reply_path)
    content = ''
    for line in range(main_comment.shape[0]):
        
        content += main_comment['评论内容'][line] + ' '
        # d.update({level:d.get(level)+1})
            
    for line in range(reply_comment.shape[0]):
        content += reply_comment['评论内容'][line] + ' '
        # content = reply_comment['评论内容'][line]
        # d.update({level:d.get(level)+1})
    word_list = jieba.cut(content,cut_all=True)
    cmt_word_split = (' '.join(word_list))
    # import sys
    # sys.stdout.reconfigure(encoding='utf-8')
    # print(cmt_word_split)
    cmt_wordcloud = WordCloud(background_color='#ffffff',font_path='./font/SmileySans-Oblique.ttf').generate(cmt_word_split)
    
    fig = matplotlib.figure.Figure(figsize=(9.9, 5), dpi=75)
    fig.add_subplot(111).imshow(cmt_wordcloud)
    fig.axes[0].get_xaxis().set_visible(False)
    fig.axes[0].get_yaxis().set_visible(False)
    
    return fig