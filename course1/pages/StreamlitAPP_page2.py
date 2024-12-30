import numpy as np
import pandas as pd
import seaborn as sns
import random
from pathlib import Path
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st
from views import Visualize

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
 )

#层级设置
page = st.sidebar.selectbox(
    '选择视图',
    ('2020年各地区性别构成', )
)

if page == '2020年各地区性别构成':
    # 第二级菜单
    setting_option = st.sidebar.radio(
        "选择图片展示", 
        [
            "人口性别构成条形图", 
            "人口性别构成竖向条形图",
            "人口性别构成直方图"
        ]
    )


#设置plt字体
plt.rcParams['font.sans-serif'] = ['SimHei']

data_gender = pd.read_excel(r"..\data\2020年各地区性别构成.xlsx")
data_gender.head()

data_gender.isnull().sum()
data_gender['地区'] = data_gender['地区'].str.replace(' ', '')

if __name__ == '__main__':
    v1 = Visualize()
    if page == '2020年各地区性别构成':

        if setting_option == "人口性别构成条形图":
            st.title("2020年各地区性别构成条形图")
            fig1 = v1.visualize_bar(
                data_gender,
                x = "地区",
                y = ["男性占比", "女性占比"],
                ylabel = '人口性别占比',
                legend = '性别'
            )
            st.plotly_chart(fig1, use_container_width = True)
            
            #显示数据帧
            st.header('数据帧')
            st.dataframe(data_gender, use_container_width = False, width = 1400, height = 600)
        elif setting_option == "人口性别构成竖向条形图":
            st.title("2020年各地区性别构成竖向条形图")
            
            fig2 = v1.visualize_bar(
                data_gender,
                y = "地区",
                x = ["男性占比", "女性占比"],
                ylabel = '人口性别占比',
                legend = '性别',
                dir = 'h'
            )
            st.plotly_chart(fig2, use_container_width = True)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(data_gender, use_container_width = False, width = 1400, height = 600)
        elif setting_option == "人口性别构成直方图":
            st.title("2020年各地区性别构成直方图")
            fig3 = v1.visualize_hist(
                data_gender,
                x="地区",
                y= ["男性占比", "女性占比"],
                barmode = 'group',
                ylabel = '占比',
                legend = '性别比'
            )
            st.plotly_chart(fig3, use_container_width = False)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(data_gender, use_container_width = False, width = 1400, height = 600)