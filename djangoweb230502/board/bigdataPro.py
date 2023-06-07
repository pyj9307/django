'''
Created on 2023. 5. 3.

@author: ADMIN
'''
import folium
from folium import plugins
import pandas as pd
import os
from djangoweb230502.settings import TEMPLATE_DIR, STATIC_DIR
from konlpy.tag import Hannanum
from nltk import Text
import matplotlib.pyplot as plt
from matplotlib import rc, font_manager
from wordcloud import WordCloud
import matplotlib
matplotlib.use('agg')

def wordcloud():
    # 한글 처리를 위한 폰트 설정
    font_path='C:/Windows/Fonts/gulim.ttc'
    font_name=font_manager.FontProperties(fname=font_path).get_name()
    matplotlib.rc('font',family=font_name)
    
    path=os.path.join(STATIC_DIR,'data/word_data.txt')
    a=open(path,'r',encoding='utf-8').read()
    hannanum=Hannanum()
        
    yes24_fd=Text(hannanum.nouns(a),name='yes24')
    
    fd=yes24_fd.vocab()
    
    wc=WordCloud(width=800,height=600,background_color='white',font_path=font_path)
    plt.imshow(wc.generate_from_frequencies(fd))
    plt.axis('off') # 축 제거
    plt.savefig(os.path.join(STATIC_DIR,'images/wordcloud.png')) # 저장.

def cctv_map():
    popup=[]
    locations=[]
    
    path=os.path.join(STATIC_DIR,'data/CCTV_20190917.csv')
    
    df=pd.read_csv(path)
    
    for data in df.values:
        if data[4] > 0:
            popup.append(data[1])
            locations.append([data[10],data[11]])
            
    m = folium.Map(location=[35.1803305, 129.0516257], # 지도의 중심
    zoom_start=17, # zoom_start=0~18까지
    tiles='Open Street Map' # 지도의 모양, Open Street Map, Stamen Terrain, Stamen Toner, API키 필요[Mapbox Bright, Mapbox Control room tiles]
    )    
    plugins.MarkerCluster(locations,popups=popup).add_to(m)
    m.save(os.path.join(TEMPLATE_DIR,'map/map01.html')) # map/map01.html로 파일 만듬