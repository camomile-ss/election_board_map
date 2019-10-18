# coding: utf-8
'''
tokorozawa.txt -> tokorozawa_latlon.txt
'''

import googlemaps
import time
import argparse

def coordinate(address, apikey):

    googleapikey = apikey
    gmaps = googlemaps.Client(key=googleapikey)

    result = gmaps.geocode(address)
    if len(result):
        lat = result[0]["geometry"]["location"]["lat"]
        lon = result[0]["geometry"]["location"]["lng"]
    else:
        lat, lon = None, None

    return lat, lon

if __name__ == '__main__':

    psr = argparse.ArgumentParser()
    psr.add_argument('infn')
    psr.add_argument('outfn')
    args = psr.parse_args()
    infn = args.infn
    outfn = args.outfn

    with open('apikey.txt', 'r') as keyf:
        apikey = keyf.read().strip()

    with open(infn, 'r', encoding='utf-8') as inf, \
         open(outfn, 'w', encoding='utf-8') as outf:
        for i, l in enumerate(inf):
            if i % 10 == 0:
                print(i)
            ku, no, address, mark = [x.strip() for x in l.split('\t')]
            lat, lon = coordinate(address, apikey)
            outf.write('\t'.join([ku, no, address, mark, str(lat), str(lon)]) + '\n')
            time.sleep(0.2)
