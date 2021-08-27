import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network

# Read data
df_interactions = pd.read_csv('data/processed_drug_interactions.csv')

# Set header title
st.title('Network Visualization of Drug-Drug Interactions')

# Add sidebar
# st.sidebar.title('Sidebar Menu')

# Define list of selection options
drug_list = ['Metformin', 'Glipizide', 'Lisinopril', 'Simvastatin',
            'Warfarin', 'Aspirin', 'Losartan', 'Acetaminophen',
            'Ibuprofen']
drug_list.sort()

# Implement multiselect options for users (returns a list)
selected_drugs = st.multiselect('Select drug(s) to visualize', drug_list)

# Set display for initial state
if len(selected_drugs) == 0:
    # Show the following text upon initial site load
    st.text('Please choose at least 1 drug')

# Create network graph when user selects >= 1 item
else:
    df_selected = df_interactions.loc[df_interactions['drug_1_name'].isin(selected_drugs) | df_interactions['drug_2_name'].isin(selected_drugs)]
    df_selected = df_selected.reset_index(drop=True)

    # Pyvis graph settings
    layout='barnes_hut'
    central_gravity=0.33
    node_distance=420
    spring_length=110
    spring_strength=0.10
    damping=0.95
    bgcolor, font_color = '#222222', 'white'

    G = nx.from_pandas_edgelist(df_selected, 'drug_1_name', 'drug_2_name', 'weight')

    # Initiate PyVis network object
    drug_net = Network(
                       height='420px',
                       width='100%',
                       bgcolor=bgcolor,
                       font_color=font_color,
                       notebook=True
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout
    drug_net.repulsion(
                    node_distance=node_distance,
                    central_gravity=central_gravity,
                    spring_length=spring_length,
                    spring_strength=spring_strength,
                    damping=damping
                   )

    # Save and load graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and load graph as HTML file (locally)
    except:
        path = './tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Read and load HTML file for display on Streamlit page
    source_code = HtmlFile.read()
    components.html(source_code, height=500, width=695)

st.markdown(
    """
    <br>
    <h6><a href="https://kennethleungty.medium.com" target="_blank">Medium article</a></h6>
    <h6><a href="https://github.com/kennethleungty/Pyvis-Network-Graph-Streamlit" target="_blank">Project GitHub repo</a></h6>
    <h6><a href="https://github.com/kennethleungty" target="_blank">Created by Kenneth Leung</a></h6>
    """, unsafe_allow_html=True,
)
