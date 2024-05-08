import streamlit as st



def get_cont(head=None, text=None):
    cont = st.container(border=True)
    with cont:
        st.subheader(head)
        st.write(text)
    return cont

