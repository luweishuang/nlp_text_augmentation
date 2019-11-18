# -*- coding: utf-8 -*-

from eda import *
import argparse
from os.path import join, dirname


def gen_eda(train_orig, output_file, alpha, num_aug=9):
    writer = open(output_file, 'w')
    lines = open(train_orig, encoding="utf-8").readlines()

    print("正在使用EDA生成增强语句...")
    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')    #使用[:-1]是把\n去掉了
        label = parts[0]
        sentence = parts[1]
        aug_sentences = eda(sentence, alpha_sr=alpha, alpha_ri=alpha, alpha_rs=alpha, p_rd=alpha, num_aug=num_aug)
        for aug_sentence in aug_sentences:
            writer.write(label + "\t" + aug_sentence + '\n')

    writer.close()
    print("已生成增强语句!")
    print(output_file)


def main():
    ap = argparse.ArgumentParser()
    # ap.add_argument("--input", required=True, type=str, help="原始数据的输入文件目录")
    ap.add_argument("--input", default="sample.txt", type=str, help="原始数据的输入文件目录")
    ap.add_argument("--output", default="sample_augmented.txt", required=False, type=str, help="增强数据后的输出文件")
    ap.add_argument("--num_aug", default=4, required=False, type=int, help="每条原始语句增强的语句数")
    ap.add_argument("--alpha_sr", default=0.1, required=False, type=float, help="每条语句中替换同义词数占比")
    ap.add_argument("--alpha_ri", default=0.1, required=False, type=float, help="每条语句中随机插入单词数占比")
    ap.add_argument("--alpha_rs", default=0.1, required=False, type=float, help="每条语句中随机互换位置单词数占比")
    ap.add_argument("--alpha_rd", default=0.1, required=False, type=float, help="每条语句中随机删除单词数占比")

    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as fi, \
            open(join(dirname(args.input), args.output), "w", encoding="utf-8") as fo:
        for line in fi:
            label, text = line.strip().split("\t", 2)
            aug_texts = eda(text, alpha_sr=args.alpha_sr, alpha_ri=args.alpha_ri, alpha_rs=args.alpha_rs,
                            p_rd=args.alpha_rd, num_aug=args.num_aug)
            for aug_text in aug_texts:
                fo.write(f"{label}\t{aug_text}\n")


if __name__ == "__main__":
    main()
