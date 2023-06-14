# -*- coding:utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 환경 설정
plt.rc('font', family='S-Core Dream')


def run_gallup():

    st.markdown("# 데이터확인\n")

    df = pd.read_excel("data/이념적성향_변동.xlsx", )
    df['연도'] = df['연도'].astype('str')
    df['구분'] = df['구분'].replace({
        "매우보수적": "보수",
        "다소보수적": "보수",
        "매우진보적": "진보",
        "다소진보적": "진보",
        "중도적": "중도"
    })
    df2 = df.groupby(['세대', '연도', '구분'])['비율'].agg('sum').reset_index()
    st.dataframe(df2)

    st.markdown("# 20대와 30대의 비율 차이\n"
                "- 진보 지지 성향은 갈수록 줄어들고 있고, 반면에 보수는 계속 증가하고 있음\n"
                "- 데이터 출처 : 사회통합실태조사 한국행정연구원(KOSIS)\n"
                "- 데이터 보기 : https://kosis.kr/statHtml/statHtml.do?orgId=417&tblId=DT_417001_0030&conn_path=I3")
    df20s = df2[df2['세대'] == '19~29세']
    df30s = df2[df2['세대'] == '30~39세']

    col1, col2, col3 = st.columns(3)
    with col1:
        color1 = st.color_picker('보수 색상 Color 변경', '#E61E2B')
    with col2:
        color2 = st.color_picker('중도 색상 Color 변경', '#808080')
    with col3:
        color3 = st.color_picker('진보 색상 Color 변경', '#004EA1')

    custom_palette = [color1, color2, color3]

    fig, ax = plt.subplots(figsize=(10, 6), ncols=2)
    sns.lineplot(data=df20s, x='연도', y='비율', hue='구분', ax=ax[0], palette=custom_palette)
    ax[0].set_title("19~29세의 이념성향 추이", size=22)
    ax[0].set_ylim(0, 100)

    sns.lineplot(data=df30s, x='연도', y='비율', hue='구분', ax=ax[1], palette=custom_palette)
    ax[1].set_title("30대의 이념성향 추이", size=22)
    ax[1].set_ylim(0, 100)
    plt.legend(loc="best")
    st.pyplot(fig)

    st.markdown("# 정당 지지도 추이")
    df2 = pd.read_excel('data/정당지지도_데이터.xlsx')
    df2["date"] = pd.to_datetime(df2["연도"].astype(str) + "-" + df2["월"].astype(str))
    df2["date"] = df2["date"] + pd.to_timedelta(df2["주"] * 7 - 6, unit="D")
    st.dataframe(df2)

    custom_palette = ['#E61E2B', '#004EA1', '#FFED00', '#808080']

    fig2, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(df2, x='date', y='10~20', hue='정당', palette=custom_palette)
    ax.set_title("10-20대")
    st.pyplot(fig2)