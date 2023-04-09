import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Home Page",
    layout="centered",
    initial_sidebar_state="expanded",
)

def main():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ## Hi there, We Are [Jebret Team] 👋

            Names of group members:
            - Arief Rahman A
            - Muhamad Ardi Nur Insan
            - Wildan Setya N

            """, unsafe_allow_html=True)


    st.snow()

if __name__ == '__main__':
    main()
