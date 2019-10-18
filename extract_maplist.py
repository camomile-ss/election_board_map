# coding: utf-8
'''
所沢用
'''
import argparse
from bs4 import BeautifulSoup
import re
import sys

if __name__ == '__main__':

    psr = argparse.ArgumentParser()
    psr.add_argument('infn')
    psr.add_argument('outfn')
    psr.add_argument('city')
    args = psr.parse_args()
    infn = args.infn
    outfn = args.outfn
    city = args.city

    with open(infn, 'r', encoding='utf-8') as inf:
        res = inf.read()
    soup = BeautifulSoup(res, 'html.parser')

    soup = soup.html.body.table.tbody

    points = []

    # 1か所1行
    tr_list = soup.find_all('tr')
    for tr in tr_list:
        # 見出し飛ばす
        if tr.find('th'):
            continue

        # td内の文字列取得
        td_list = tr.find_all('td')
        texts = []
        for td in td_list:
            texts.append(td.text)

        # 目標の行(長さ1)は, 前の行にくっつける
        if len(td_list) == 1:
            points[-1].extend(texts)
        # 番号・住所は新しい行 ('MAP'は除く)
        else:
            points.append(texts[:-1])

    ptn = re.compile(r'^(\d+)-(\d+)$')

    for i in range(len(points)):
        # 1カラム目は、投票区と設置番号に分ける
        mob = ptn.search(points[i][0])
        if not mob:
            print('[err]', points[i])
            sys.exit()
        tohyoku = mob.group(1)
        settino = mob.group(2)
        # 2カラム目は市区町村を入れる
        address = city + points[i][1]
        points[i] = [tohyoku, settino, address] + points[i][2:]

    with open(outfn, 'w', encoding='utf-8') as outf:
        outf.write('\n'.join(['\t'.join(x) for x in points]) + '\n')

