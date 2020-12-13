# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import logging

# import csv
import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image

class WgPipeline:
    user_names = []
    comment_ratings = []
    comment_dates = []
    comment_contents = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        comment_dic = {'user_names': self.user_names, 'comment_ratings': self.comment_ratings, 'comment_dates': self.comment_dates, 'comment_contents': self.comment_contents}
        # logging.log(logging.INFO, comment_dic)
        logging.log(logging.INFO, len(self.user_names))
        logging.log(logging.INFO, len(self.comment_ratings))
        logging.log(logging.INFO, len(self.comment_dates))
        logging.log(logging.INFO, len(self.comment_contents))
        # 转换成 DataFrame 格式
        comment_df = pd.DataFrame(comment_dic)
        # 保存数据
        comment_df.to_csv('data.csv')

        if len(self.comment_contents)>0:
            self.jieba_()
            self.world_cloud()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # logging.log(logging.WARNING, adapter.get('user_name'))

        if adapter.get('user_name') != None:
            self.user_names = self.user_names + adapter.get('user_name')
            self.comment_ratings = self.comment_ratings + adapter.get('comment_rating')
            self.comment_dates = self.comment_dates + adapter.get('comment_date')
            self.comment_contents = self.comment_contents + adapter.get('comment_content')

        logging.log(logging.INFO, len(self.user_names))
        logging.log(logging.INFO, len(self.comment_ratings))
        logging.log(logging.INFO, len(self.comment_dates))
        logging.log(logging.INFO, len(self.comment_contents))

        return item

    # jieba 分词处理
    def jieba_(self):
        csv_data = pd.read_csv('data.csv')
        # csv_list = csv.reader(open('data.csv', 'r', encoding='utf-8'))
        # print('csv_list',csv_list)
        comments = csv_data['comment_contents']
        # for i,line in enumerate(csv_list):
        #     if i != 0:
        #         comment = line[2]
        #         comments += comment
        # print("comment-->",comments)
        # logging.log(logging.INFO, comments[0:3])
        # jieba 分词
        # '##'.join(map(str,li))
        words = jieba.lcut(" ".join(map(str,comments)))
        new_words = []
        # 要排除的词
        remove_words = ['以及', '在于', '一些', '一场', '只有',
                        '不过', '东西', '场景', '所有', '这么',
                        '但是', '全片', '之前', '一部', '一个',
                        '作为', '虽然', '一切', '怎么', '表现',
                        '人物', '没有', '不是', '一种', '个人'
                        '如果', '之后', '出来', '开始', '就是',
                        '电影', '还是', '不是', '武汉', '镜头']
        for word in words:
            if word not in remove_words:
                new_words.append(word)
        global word_cloud
        # 用逗号分隔词语
        word_cloud = '，'.join(new_words)

        logging.log(logging.INFO, 'fdafdafdafdfhtrytryt')
        # logging.log(logging.INFO, " ".join(map(str,comments)))
        logging.log(logging.INFO, len(new_words))
        logging.log(logging.INFO, '，'.join(words))
        # logging.log(logging.INFO, new_words)

    # 生成词云
    def world_cloud(self):
        # 背景图
        # cloud_mask = np.array(Image.open('crown2.jpg'))
        cloud_mask = np.array(Image.open('wire.jpg'))
        wc = WordCloud(
            # 背景图分割颜色
            background_color='white',
            # 背景图样
            width=800,
            height=800,
            mask=cloud_mask,
            # 显示最大词数
            max_words=600,
            # 显示中文
            font_path='./fonts/FZZBHJW.ttf',
            # 字的尺寸限制
            min_font_size=8,
            max_font_size=100,
            margin=5
        )
        global word_cloud
        x = wc.generate(word_cloud)
        # 生成词云图片
        image = x.to_image()
        # 展示词云图片
        image.show()
        # 保存词云图片
        wc.to_file('wc.png')
