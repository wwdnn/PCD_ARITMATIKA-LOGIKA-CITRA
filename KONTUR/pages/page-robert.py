import streamlit as st
import numpy as np
import cv2

st.set_page_config(page_title="Roberts Edge Detection")

st.title("Edge Detection Robert👋")
# add subtitle 
st.markdown("""
    ©Created by Jebret Team - 2023
    """)

uploaded_file = st.file_uploader("Choose an image", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    # Load the image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply the Roberts operator
    kernelx = np.array([[1, 0], [0, -1]])
    kernely = np.array([[0, 1], [-1, 0]])
    robertsx = cv2.filter2D(gray, -1, kernelx)
    robertsy = cv2.filter2D(gray, -1, kernely)
    roberts = cv2.add(robertsx, robertsy)

    # Display the images using Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Original Image')
        st.image(img, channels='BGR')

    with col2:
        st.subheader('Roberts Edge Detection')
        st.image(roberts, channels='GRAY')
