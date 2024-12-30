import numpy as np
import pandas as pd
import seaborn as sns
import random
from pathlib import Path
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st
import networkx as nx
import matplotlib as mpl



if __name__ == '__main__':

    # mpl.rcParams['figure.facecolor'] = 'none'
    
    st.set_page_config(
        page_title="主视图",
        page_icon="👋",
        layout = 'wide'
    )
    col1, col2 = st.columns([1, 4])
    
    # facebook = pd.read_csv(
    #     "../data/facebook_combined.txt.gz",
    #     compression="gzip",
    #     sep=" ",
    #     names=["start_node", "end_node"]
    # )
    # G = nx.from_pandas_edgelist(facebook.head(5000), "start_node", "end_node")

    # plot_options = {"node_size": 18, 
    #             "with_labels": False, 
    #             "width": 0.15, 
    #             "edge_color": '0.18',
    #             "alpha": 0.6}

    # pos = nx.spring_layout(G, iterations=15, seed=1721)

    # fig, ax = plt.subplots(figsize=(18, 18))
    # # ax.set_facecolor('none')
    # ax.axis("off")
    # nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)
    
    col2.image(r'./Plot_figure/social_networks.svg', use_column_width = True)
    
    col1.page_link(r"StreamlitAPP_home_strat.py", label="Home", icon="🏠")
    col1.page_link(r"./pages/StreamlitAPP_page1.py", label="各类受教育程度人数", icon="1️⃣")
    col1.page_link(r"./pages/StreamlitAPP_page2.py", label='2020年各地区性别构成', icon="2️⃣")
    col1.page_link(r"./pages/StreamlitAPP_page3.py", label=r'2020年各地区/全国人口年龄构成', icon="3️⃣")
    # st.page_link("http://www.google.com", label="Google", icon="🌎")