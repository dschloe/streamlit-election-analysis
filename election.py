# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium, folium_static

plt.rcParams['axes.unicode_minus'] = False       # 마이너스 부호 깨짐 현상
plt.rc('font', family='S-Core Dream')

def run_election():

    st.markdown("# 지도관련 데이터 확인")
    kr_sido = gpd.read_file('data/TL_SCCO_CTPRVN',
                            encoding="cp949")  ## 원본 shape 파일의 한글코드: cp949 (not utf8)
    st.write(kr_sido.head())

    st.markdown("# 대선득표율 데이터 확인")
    vote = pd.read_excel("data/대선득표율.xlsx")
    vote['sido_id'] = vote['sido_id'].apply(str)
    vote['이재명_득표율'] = vote['이재명'] / vote['투표수'] * 100
    vote['윤석열_득표율'] = vote['윤석열'] / vote['투표수'] * 100
    st.dataframe(vote.head())

    st.markdown("# GeoDataFrame과 DataFrame 병합")
    kr_sido.rename(columns={"CTPRVN_CD": "sido_id"}, inplace=True)
    kr_sido = kr_sido.merge(vote, on='sido_id')
    kr_sido.drop(columns={"CTP_ENG_NM", "CTP_KOR_NM"}, inplace=True)
    st.write(kr_sido.head())

    st.markdown("# 후보자의 시도별 득표율")
    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(15, 10))
    kr_sido.plot(ax=ax[0], column="이재명_득표율", cmap="OrRd", legend=False, alpha=0.9)
    kr_sido.plot(ax=ax[1], column="윤석열_득표율", cmap="OrRd", legend=False, alpha=0.9)
    patch_col = ax[0].collections[0]
    fig.colorbar(patch_col, ax=ax, shrink=0.5)
    ax[0].set_title('이재명')
    ax[1].set_title('윤석열')
    ax[0].set_axis_off();
    ax[1].set_axis_off();
    st.pyplot(fig)

    m = kr_sido.explore(column="선거인수", zoom_start=6, width=350, height=400)
    st_folium(m, width=700)

