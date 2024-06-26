import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Kanban Board",
    page_icon=":clipboard:",
    layout="wide"
)


df = pd.read_json('items.json') # load content

title = st.title('Kanban Board')

col1, col2, col3, col4 = st.columns(4) # initialize columns
pop = st.popover(label='Add Item') # initialize new-item-button


# change position of item on the board

for key in st.session_state:
    if st.session_state[key]: # button behaviour
        if key.startswith('next'):
            for index, row in df[df['name'] == key[4:]].iterrows():
                print(row)
                if row['category'] < 4:
                    df.at[index, 'category'] += 1

        if key.startswith('back'):
            for index, row in df[df['name'] == key[4:]].iterrows():
                if row['category'] > 1:
                    df.at[index, 'category'] -= 1

        if key.startswith('remv'):
            for index, row in df[df['name'] == key[4:]].iterrows():
                df.drop(index=index, inplace=True)

    df.to_json('items.json')


# edit function for name and description of individual item

def edit_c(i):
    head_e = 'ed_h' + str(i)
    text_e = 'ed_t' + str(i)
    for key in st.session_state:
        if key == head_e and st.session_state[key] != '':
            df.at[i, 'name'] = st.session_state[head_e]
            df.at[i, 'desc'] = st.session_state[text_e]
            print(i, key, st.session_state[head_e], st.session_state[text_e])
            df.to_json('items.json')
            st.rerun()

# frontend of individual container

def get_cont(head_i=None, text_i=None, ind=None):
    cont = st.container(border=True)
    with cont:
        st.subheader(head_i) # content
        st.text(text_i)
        n_button = 'next' + head_i
        b_button = 'back' + head_i
        r_button = 'remv' + head_i
        e_form = 'edit' + head_i
        head_e = 'ed_h' + str(ind)
        text_e = 'ed_t' + str(ind)
        edit = st.popover(label=':pencil2:') # dropdown for all edit functions
        with edit:
            e_form = st.form(key=e_form, clear_on_submit=True)
        with e_form:
            st.text_input(label='edit name', label_visibility='hidden', placeholder=head_i,
                          key=head_e)
            st.text_area(label='edit text', label_visibility='hidden', placeholder='Description',
                         key=text_e)
            st.form_submit_button(label='submit', on_click=edit_c(ind))

        with edit:
            c_col1, c_col2, c_col3 = st.columns(3) # columns for separate buttons
        with c_col3:
            st.button(label=':arrow_forward:', key=n_button)
        with c_col1:
            st.button(label=':arrow_backward:', key=b_button)
        with c_col2:
            st.button(label=':x:', key=r_button)

    return cont

# create a new item in column 1 of the Kanban board

def new_cont(data=df):
    head_n = st.session_state['head']
    text_n = st.session_state['text']
    cont = {'category': 1, 'name': head_n, 'desc': text_n}
    data = pd.concat([data, pd.DataFrame([cont])], ignore_index=True)
    data.to_json('items.json')

# define columns

with col1:
    st.header('Idea', divider='blue')
    for index, row in df[df['category'] == 1].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text, index)

with col2:
    st.header('In Progress', divider='violet')
    for index, row in df[df['category'] == 2].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text, index)

with col3:
    st.header('Testing', divider='red')
    for index, row in df[df['category'] == 3].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text, index)

with col4:
    st.header('Done', divider='green')
    for index, row in df[df['category'] == 4].iterrows():
        head = row['name']
        text = row['desc']
        get_cont(head, text, index)

# define new-item-menu
with pop:
    new_item = st.form(key='new', clear_on_submit=True)

with new_item:
    st.text_input(label='Project name', label_visibility='hidden', placeholder='Title',
                  key='head')
    st.text_area(label='Project text', label_visibility='hidden', placeholder='Description',
                 key='text')
    st.form_submit_button(label='submit', on_click=new_cont)

