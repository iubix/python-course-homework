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
    ('各类受教育程度人数', )
)

if page == '各类受教育程度人数':
    # 第二级菜单
    setting_option = st.sidebar.radio(
        "选择图片展示", 
        [
            "地区人口学历分布柱状图", 
            "地区人口学历分布竖柱状图", 
            "各地区人口大学比例直方图",
            "各地区人口大学比例玫瑰图",
            "各地区人口大学比例饼图"
        ]
    )

#设置plt字体
plt.rcParams['font.sans-serif'] = ['SimHei']

#导入数据1

data1 = pd.read_excel(r"../data/2020年各地区每10万人口中拥有的各类受教育程度人数.xlsx")

#处理数据
data1.isnull().sum()
data1['地区'] = data1['地区'].str.replace(' ', '')

edu_data = data1.copy()
edu_data['其他'] = 100000 - edu_data['小学'] - edu_data['初中'] - edu_data['高中'] - edu_data['大学']
edu_data.sort_values(by=['大学','高中','初中','小学'], ascending=False, inplace=True)


    
if __name__ == '__main__':
        
    #实例1
    v1 = Visualize()

    if page == '各类受教育程度人数' :
        if setting_option == "地区人口学历分布柱状图":
        
            st.title("各类受教育程度人数柱状图")
            
            fig1 = v1.visualize_pdbar(edu_data, num = 1000)
            
            st.pyplot(fig1, use_container_width = True)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(edu_data, use_container_width = False, width = 1400, height = 600)

        elif setting_option == "地区人口学历分布竖柱状图":
            st.title("各类受教育程度人数竖柱状图")

            fig2 = v1.visualize_pdbarh(edu_data, num = 1000)

            st.pyplot(fig2, use_container_width = True)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(edu_data, use_container_width = False, width = 1400, height = 600)

        elif setting_option == "各地区人口大学比例直方图":
            st.title("各地区人口大学比例直方图")

            fig3 = v1.visualize_hist(
                edu_data,
                x = '地区',
                y = ['大学', '高中', '初中', '小学', '其他'],
                barmode = 'group',
                ylabel = '各学历人数'
            )

            st.plotly_chart(fig3, use_container_width = True)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(edu_data, use_container_width = False, width = 1400, height = 600)

        elif setting_option == "各地区人口大学比例玫瑰图":
            st.title("各地区人口大学比例玫瑰图")
            col1, col2 = st.columns(2)

            new_data = v1.trans_polardata(edu_data)
            fig4 = v1.visualize_polar(new_data)

            col2.plotly_chart(fig4, use_container_width = False)
            #显示数据帧
            col1.dataframe(new_data, use_container_width=False, width = 600)
        
        elif setting_option == "各地区人口大学比例饼图":
            st.title("各地区人口大学比例饼图")
            
            col1, col2 = st.columns(2)

            new_data = v1.trans_polardata(edu_data)
            fig5 = v1.visualize_pie(
                new_data, 
                hole = 0.7,
                names = '学历', 
                values = '人数', 
            )

            col2.plotly_chart(fig5, use_container_width = True)
            #显示数据帧
            col1.dataframe(new_data, use_container_width = True)