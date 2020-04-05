# -*- coding: utf-8 -*-
import os
import sys
import re
import glob
from gensim import corpora, matutils
import MeCab
from collections import Counter
from natsort import natsorted

DATA_DIR_PATH = './utublog-utf8/'
DICTIONARY_FILE_NAME = 'livedoordic.txt'
mecab = MeCab.Tagger('mecabrc')


def get_class_id(file_name):
    '''
    ファイル名から、クラスIDを決定する。
    学習データを作るときに使っています。
    '''
    dir_list = get_dir_list()
    dir_name = next(filter(lambda x: x in file_name, dir_list), None)
    if dir_name:
        return dir_list.index(dir_name)
    return None


def get_dir_list():
    '''
    ライブドアコーパスが./text/ の下にカテゴリ別にあるからそのカテゴリ一覧をとってるだけ
    '''
    tmp = natsorted(os.listdir(DATA_DIR_PATH))
    if tmp is None:
        return None
    return natsorted([x for x in tmp if os.path.isdir(DATA_DIR_PATH + x)])
    #return sorted([x for x in tmp if os.path.isdir(DATA_DIR_PATH + x)])
#print(get_dir_list()) ['utsu1', 'utsu10', 'utsu11', 'utsu12', 'utsu13', 'utsu14', 'utsu15

def get_file_content(file_path):
    '''
    1つの記事を読み込み
    '''
    with open(file_path, encoding='utf-8') as f:
        return ''.join(f.readlines()[0:])  # ライブドアコーパスが3行目から本文はじまってるから


def tokenize(text):
    '''
    とりあえず形態素解析して名詞だけ取り出す感じにしてる
    '''
    node = mecab.parseToNode(text)
    while node:
        if node.feature.split(',')[0] == '名詞':
            yield node.surface.lower()
        node = node.next


def check_stopwords(word):
    '''
    ストップワードだったらTrueを返す
    '''
    if re.search(r'^[0-9]+$', word):  # 数字だけ
        return True
    return False

def get_words(contents):
    
    #記事群のdictについて、形態素解析して返す
    
    dic = {}
    ret=[]
    for k, content in contents.items():
        #ret.append(get_words_main(content))
        ret=get_words_main(content)
        dic[k]=ret
    return dic


def get_words_main(content):
    '''
    一つの記事を形態素解析して返す
    '''
    return [token for token in tokenize(content) if not check_stopwords(token)]


def filter_dictionary(dictionary):
    '''
    低頻度と高頻度のワードを除く感じで
    '''
    dictionary.filter_extremes(no_below=1, no_above=1.0)  # この数字はあとで変えるかも
    return dictionary


def get_contents():
    '''
    livedoorニュースのすべての記事をdictでまとめておく
    '''
    dir_list = get_dir_list()

    if dir_list is None:
        return None

    ret = {}
    i=1
    auth=1
    for dir_name in dir_list:
        #flist = glob.glob(DATA_DIR_PATH + dir_name+'/*')
        file_list = natsorted(os.listdir(DATA_DIR_PATH + dir_name))
        #file_list = os.listdir(flist)
        #print(dir_name) ken utsu
        if file_list is None:
            continue
        for file_name in file_list:
            #print(file_name) ken-20100330.txt
            #print(dir_name)
            if dir_name in file_name:  # LICENSE.txt とかを除くためです。。 多分いらない
                #print(dir_name) ken ken utsu utsu
                file_name_num = str(auth) + '-' + str(i) + '-' + file_name
                #file_name_num = str(i) + '-' + file_name
                ret[file_name_num] = get_file_content(DATA_DIR_PATH + dir_name + '/' + file_name)
                #print(file_name_num)
                if i == 30:
                    i=0
                i += 1
            '''
            file_name_num = file_name + str(i)
            ret[file_name_num] = get_file_content(DATA_DIR_PATH + dir_name + '/' + file_name)

            i += 1
            print(file_name_num)
            '''
        auth+=1
    return ret

#print(get_contents())


def get_vector(dictionary, content):
    '''
    ある記事の特徴語カウント
    '''
    tmp = dictionary.doc2bow(get_words_main(content))
    dense = list(matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0])
    return dense


def get_dictionary(create_flg=False, file_name=DICTIONARY_FILE_NAME):
    
    #辞書を作る
    
    if create_flg or not os.path.exists(file_name):
        # データ読み込み
        contents = get_contents()
        # 形態素解析して名詞だけ取り出す
        #words = get_words(contents)
        dictionary = get_words(contents)
        #print(words)
        # 辞書作成、そのあとフィルタかける

        for i, value in dictionary.items():
            #a = []
            #a.append(value)
            #dictionary = filter_dictionary(corpora.Dictionary(value))

            counter = Counter(value)
            for word, cnt in counter.most_common():
                with open('/Users/yasuhiko/PycharmProjects/bow 3.7 jp not lsi/result/' + i, mode='a') as f:
                    # print(str(value))
                    f.write(str(word)+','+str(cnt)+'\n')

            # 保存しておく
            if file_name is None:
                sys.exit()
            #dictionary.save_as_text('/Users/yasuhiko/PycharmProjects/bow 3.7 jp not lsi/result/'+i)
            #print('getcwd:      ', os.getcwd())
            #with open('/Users/yasuhiko/PycharmProjects/bow 3.7 jp not lsi/result/'+i, mode='w') as f:
                #print(str(value))
                #f.write(str(value))


        '''
        #words = get_words(contents)
        dictionary = get_words(contents)
        #print(words)
        # 辞書作成、そのあとフィルタかける
        for i in dictionary:
            #dictionary = filter_dictionary(corpora.Dictionary(i))

            # 保存しておく
            if file_name is None:
                sys.exit()
            #dictionary.save_as_text(file_name)
            with open(file_name, mode='w') as f:
                print(str(i))
                f.write(str(i))
        '''
    else:
        # 通常はファイルから読み込むだけにする
        dictionary = corpora.Dictionary.load_from_text(file_name)

    return dictionary

'''
def get_dictionary(create_flg=False, file_name=DICTIONARY_FILE_NAME):
    
    辞書を作る
    
    if create_flg or not os.path.exists(file_name):
        # データ読み込み
        contents = get_contents()
        # 形態素解析して名詞だけ取り出す
        words = get_words(contents)
        print(words)
        # 辞書作成、そのあとフィルタかける
        dictionary = filter_dictionary(corpora.Dictionary(words))
        # 保存しておく
        if file_name is None:
            sys.exit()
        dictionary.save_as_text(file_name)

    else:
        # 通常はファイルから読み込むだけにする
        dictionary = corpora.Dictionary.load_from_text(file_name)

    return dictionary
'''
if __name__ == '__main__':
    get_dictionary(create_flg=True)
