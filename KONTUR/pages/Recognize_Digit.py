import streamlit as st
import cv2
import numpy as np

def binarize_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return binary
    

def get_contours(binary):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        print("Error: No contour found")
        return None
    return contours[0]


def get_freeman_chaincode(contour):
    # Freeman Chain Code 

    #  Representasi chain code:
    # 3  2  1 
    # \ | /
    # 4--P--0
    # / | \
    # 5  6  7
    # 
    # Representasi chain code berdasarkan ketetanggaan terhadap titik P
    # Deltax      Deltay      code
    # 0             +1          6 
    # +1            +1          7
    # +1            0           0
    # +1            -1          1
    # 0             -1          2
    # -1            -1          3
    # -1            0           4
    # -1            +1          5
    # 

    chaincode = []
    for i in range(len(contour)):
        if i == len(contour)-1:
            next = 0
        else:
            next = i+1
        x = contour[next][0][0] - contour[i][0][0]
        y = contour[next][0][1] - contour[i][0][1]
        if x == 1 and y == 0:
            chaincode.append(0)
        elif x == 1 and y == -1:
            chaincode.append(1)
        elif x == 0 and y == -1:
            chaincode.append(2)
        elif x == -1 and y == -1:
            chaincode.append(3)
        elif x == -1 and y == 0:
            chaincode.append(4)
        elif x == -1 and y == 1:
            chaincode.append(5)
        elif x == 0 and y == 1:
            chaincode.append(6)
        elif x == 1 and y == 1:
            chaincode.append(7)
    return chaincode

def recognize_digit(chaincode):
    # 0
    if chaincode == [6, 6, 6, 6, 6, 0, 0, 0, 0, 2, 2, 2, 2, 2, 4, 4, 4, 4]:
        return '0'
    # 1
    elif chaincode == [5, 1, 7, 6, 6, 6, 6, 2, 2, 2, 2, 2, 4]:
        return '1'
    # 2
    elif chaincode == [5, 1, 0, 0, 7, 5, 5, 5, 5, 0, 0, 0, 0, 4, 4, 3, 1, 1, 1, 3, 4, 4]:
        return '2'
    # 3
    elif chaincode == [5, 1, 0, 0, 7, 6, 5, 4, 0, 7, 5, 4, 4, 3, 7, 0, 0, 0, 2, 2, 2, 2, 2, 4, 4, 4]:
        return '3'
    # 4
    elif chaincode == [6, 6, 6, 0, 0, 0, 7, 6, 2, 2, 2, 2, 2, 6, 6, 5, 4, 4, 3, 2, 2]:
        return '4'
    # 5
    elif chaincode == [5, 6, 7, 0, 0, 7, 5, 4, 4, 4, 0, 0, 0, 0, 2, 3, 4, 4, 3, 2, 1, 0, 0, 0, 4, 4, 4]:
        return '5'
    # 6
    elif chaincode == [6, 6, 6, 6, 6, 0, 0, 0, 2, 2, 4, 4, 3, 2, 1, 0, 0, 4, 4, 4]:
        return '6'
    # 7
    elif chaincode == [0, 0, 7, 6, 5, 6, 6, 2, 2, 1, 2, 2, 4, 4, 4]:
        return '7'
    # 8
    elif chaincode == [6, 6, 6, 6, 6, 0, 0, 0, 0, 2, 2, 2, 2, 2, 4, 4, 4, 4]:
        return '8'
    # 9
    elif chaincode == [6, 6, 6, 0, 0, 0, 7, 5, 4, 0, 1, 2, 2, 2, 2, 4, 4, 4, 4]:
        return '9'
    else:
        return None

st.title("Digit Recognizer")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(img, channels="BGR")

    binary = binarize_image(img)
    st.write(binary)
    contour = get_contours(binary)
    chaincode = get_freeman_chaincode(contour)
    digit = recognize_digit(chaincode)

    if digit is not None:
        st.write(f"Recognized Digit: {digit}")
