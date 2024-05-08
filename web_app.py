import streamlit as st
from container import get_cont
import pandas as pd
import json

col1, col2, col3 = st.columns(3)

container = [{'category': 1, 'name': 'Project A', 'desc': 'description A'},
             {'category': 1, 'name': 'Project B', 'desc': 'description B'}]
df = pd.read_json('items.json')


pop = st.popover(label='Add Item')


def new_cont(data=df):
    head_n = st.session_state['head']
    text_n = st.session_state['text']
    cont = {'category': 1, 'name': head_n, 'desc': text_n}
    data = pd.concat([data, pd.DataFrame([cont])], ignore_index=True)
    data.to_json('items.json')



with col1:
    st.header('Idea', divider=True)
    for index, row in df[df['category'] == 1].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text)

with col2:
    st.header('In Progress', divider=True)
    for index, row in df[df['category'] == 2].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text)

with col3:
    st.header('Done', divider=True)
    for index, row in df[df['category'] == 3].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text)

with pop:
    new_item = st.form(key='new', clear_on_submit=True)

with new_item:
    st.text_input(label='Project name', label_visibility='hidden', placeholder='Title',
                  key='head', )
    st.text_input(label='Project text', label_visibility='hidden', placeholder='Description',
                  key='text')
    st.form_submit_button(label='submit', on_click=new_cont)
