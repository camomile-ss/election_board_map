# coding: utf-8
'''
pointをマップに表示
'''
import numpy as np
import folium
import sys
import argparse
#sys.path.append('../common')
#from common_character import enc_detect

def make_map(ll_data, zoom_start=14):
    ''' マップを定義 '''

    # 緯度・経度の中心
    ll_data = np.array(ll_data)
    ll_max = ll_data.max(axis=0)
    ll_min = ll_data.min(axis=0)
    ll_center = (ll_max + ll_min) / 2

    osm = folium.Map(location=list(ll_center), zoom_start=zoom_start)
    return osm

def conc(data):

    conc_data = []
    for l in data:
        conc_addr = [x[3] for x in conc_data]
        ku, no, ku_no, addr, mark, lat, lon = l
        if addr in conc_addr:
            idx = conc_addr.index(addr)
            conc_data[idx][2] = conc_data[idx][2] + ', ' + ku_no
            conc_data[idx][4] = conc_data[idx][4] + ', ' + mark
        else:
            conc_data.append(l)

    return conc_data

def get_color(ku):
    ''' 色分け '''

    color_tbl = ['red','blue','green','purple','orange','darkred','lightred',
                 'beige','darkblue','darkgreen','cadetblue','darkpurple',
                 'pink','lightblue','lightgreen','gray','black','lightgray']  # 'white',

    i = ku % len(color_tbl)
    return color_tbl[i]

def draw_points(osm, data, radius=5):
    ''' 描画（marker） '''
    for l in data:
        ku, no, ku_no, add, mark, lat, lon = l

        #folium.Marker([lat, lon], popup=str(lat) + ',' + str(lon), tooltip='{0}({1},{2})'.format(snm, scd, sid), \
        #              icon = folium.Icon(color = 'red')).add_to(osm)

        popup=folium.Popup(mark + ' [' + add + ']', max_width=1000)
        tooltip=folium.Tooltip(ku_no, permanent=True)

        color = get_color(ku)

        folium.Marker(
            location=[lat, lon],
            radius=5,
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color=color)
        ).add_to(osm)

    return osm

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('infn', help='tokorozawa_latlon.txt')
    parser.add_argument('outfn', help='html file.')
    parser.add_argument('-z', help='default 14', type=int, default=14)

    args = parser.parse_args()
    infn = args.infn
    outfn = args.outfn
    zoom = args.z

    with open(infn, 'r', encoding='utf-8') as inf:
        data = [l.strip().split('\t') for l in inf.readlines()]

    data = [[int(x[0]), int(x[1]), '{0}-{1}'.format(x[0], x[1])] + x[2:4] + [float(x[4]), float(x[5])] for x in data]

    # 同じ住所のデータまとめる
    data = conc(data)

    ll_data = [[r[5], r[6]] for r in data]
    osm = make_map(ll_data, zoom_start=zoom)

    osm = draw_points(osm, data)

    osm.save(outfn)

