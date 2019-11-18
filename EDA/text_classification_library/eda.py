import jieba
import synonyms
import random
from random import shuffle

random.seed(2019)


# 停用词列表，默认使用哈工大停用词表
with open('stopwords/HIT_stop_words.txt', encoding="utf-8") as fi:
    stopwords = set([line.strip() for line in fi])


# 同义词替换
# 替换一个语句中的n个单词为其同义词
def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stopwords]))
    random.shuffle(random_word_list)
    num_replaced = 0  
    for random_word in random_word_list:          
        syn_words = synonyms.nearby(random_word)[0]
        if len(syn_words) >= 1:
            synonym = random.choice(syn_words)
            new_words = [synonym if word == random_word else word for word in new_words]   
            num_replaced += 1
        if num_replaced >= n: 
            break
    return new_words


# 随机插入
# 随机在语句中插入n个词
def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words


def add_word(new_words):
    syn_words = []
    counter = 0    
    while len(syn_words) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        syn_words = synonyms.nearby(random_word)[0]
        counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(syn_words)
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)


# Random swap
# Randomly swap two words in the sentence n times
def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words


def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words)-1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1] 
    return new_words


# 随机删除
# 以概率p删除语句中的词
def random_deletion(words, p):
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words)-1)
        return [words[rand_int]]

    return new_words


# EDA函数
def eda(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
    seg_list = jieba.cut(sentence)
    seg_list = " ".join(seg_list)
    words = list(seg_list.split())
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug/4)+1
    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    # 同义词替换sr
    for _ in range(num_new_per_technique):
        a_words = synonym_replacement(words, n_sr)
        augmented_sentences.append(''.join(a_words))

    # 随机插入ri
    for _ in range(num_new_per_technique):
        a_words = random_insertion(words, n_ri)
        augmented_sentences.append(''.join(a_words))

    # 随机交换rs
    for _ in range(num_new_per_technique):
        a_words = random_swap(words, n_rs)
        augmented_sentences.append(''.join(a_words))

    # 随机删除rd
    for _ in range(num_new_per_technique):
        a_words = random_deletion(words, p_rd)
        augmented_sentences.append(''.join(a_words))

    shuffle(augmented_sentences)

    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    return augmented_sentences
