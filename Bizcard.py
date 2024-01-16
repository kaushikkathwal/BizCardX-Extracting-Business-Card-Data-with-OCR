#IMPORTING NECESSARY LIBRARIES

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import easyocr
import mysql.connector as sql
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re
import json



#STREAMLIT SETUP ALONG WITH EXTRACTION FUNCTION SETUP

st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR",layout= "wide")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
col1,col2=st.columns(2)
with col1:
        filepath=load_lottiefile("E:\data science\Bizcard card data extraction\B.json")
        st.lottie(filepath,speed=1,reverse=False,loop=True,height=100,width=100,quality="highest")
        
with col2:
    st.markdown("<h1 style='text-align:right; color:white;'>BizCardX</h1>", unsafe_allow_html=True)
    
selected=option_menu(
        menu_title="Extracting Business Card Data with OCR",
        options=["HOME","UPLOAD AND EXTRACT","EDIT","ADDITIONAL INFORMATION"],
        icons=["house-fill","credit-card-2-front-fill","pencil-square","book-half"],
        menu_icon="wallet-fill",
        orientation="horizontal",
        styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "15px"},
                               "container" : {"max-width": "14000px"},
                               "nav-link-selected": {"background-color": "#121010"}})

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

# CONNECTING WITH MYSQL DATABASE

mydb = sql.connect(host="localhost",
                   user="root",
                   password="your password",
                   database= "bizcard"
                  )
mycursor = mydb.cursor(buffered=True)

#TABLE CREATION

mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

# HOME MENU



if selected == "HOME":
    filepath=load_lottiefile("E:\data science\Bizcard card data extraction\A.json")
    st.lottie(filepath,speed=1,reverse=False,loop=True,height=400,width=1200,quality="highest")
    selected=option_menu( menu_title="",
        options=["About Project","Technologies Used"],
        icons=["distribute-vertical","code"],
        menu_icon="play-fill",
        orientation="horizontal",
        styles={"nav-link": {"font-size": "12px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "4x"},
                               "container" : {"max-width": "800px"},
                               "nav-link-selected": {"background-color": "#121010"}})
    
    if selected =="About Project":
        st.header(":white[**Objective**]")
        st.markdown(":white[**The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.**]")
        st.markdown(":white[**This is a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using  easyOCR. The extracted information should include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state,and pin code. The extracted information should then be displayed in the application's graphical user interface (GUI).**]")
                        
    if selected=="Technologies Used":
        st.header(":white[**1.Python**]")
        st.markdown("Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured particularly, procedural and functional programming, object-oriented, and concurrent programming.Python is widely used for web development, software development, data science, machine learning and artificial intelligence, and more. It is free and open-source software.")                  
        st.header(":white[**2.EasyOCR**]")
        st.markdown(":white[**EasyOCR is a font-dependent printed character reader based on a template matching algorithm. It has been designed to read any kind of short text part numbers, serial numbers, expiry dates, manufacturing dates, lot codes, printed on labels or directly on parts.In EasyOCR OCR stands for Optical Character Recognition. It is a widespread technology to recognize text inside images, such as scanned documents and photos. OCR technology is used to convert virtually any kind of image containing written text (typed, handwritten, or printed) into machine-readable text data.**]")
        st.header(":white[**3.SQL**]")
        st.markdown(":white[**Structured query language (SQL) is a programming language for storing and processing information in a relational database. A relational database stores information in tabular form, with rows and columns representing different data attributes and the various relationships between the data values.**]")                  
        st.header(":white[**4.Pandas**]")
        st.markdown(":white[**Pandas is a Python library used for working with data sets. It has functions for analyzing, cleaning, exploring, and manipulating data. The name Pandas has a reference to both Panel Data, and Python Data Analysis**]")
        st.header(":white[**5.Plotly**]")
        st.markdown(":white[**Plotly is a free and open-source Python library for creating interactive, scientific graphs and charts. It can be used to create a variety of different types of plots, including line charts, bar charts, scatter plots, histograms, and more. Plotly is a popular choice for data visualization because it is easy to use and produces high-quality graphs. It is also very versatile and can be used to create a wide variety of different types of plots.**]")             
        st.header(":white[**6.Streamlit**]")
        st.markdown(":white[**Streamlit is an open-source app framework in python language. It helps us create beautiful web apps for data science and machine learning in a little time. It is compatible with major python libraries such as scikit-learn, keras, PyTorch, latex, numpy, pandas, matplotlib, etc.**]")               
    

# Create the 'uploaded_cards' directory or folder to store images of cards in our system.
if not os.path.exists("uploaded_cards"):
    os.makedirs("uploaded_cards")

if selected=="UPLOAD AND EXTRACT":
    filepath=load_lottiefile("E:\data science\Bizcard card data extraction\d.json")
    st.lottie(filepath,speed=1,reverse=False,loop=True,height=150,width=1200,quality="highest")

    st.subheader(":white[Upload a Business Card]")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    def image_preview(image, res):
            for (bbox, text, prob) in res:
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)
    
    selected=option_menu(menu_title="",
        options=["CARD PREVIEW","EXTRACTION AND STORING"],
        icons=["card-image","postcard-fill"],
        orientation="horizontal",
        styles={"nav-link": {"font-size": "10px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "2x"},
                               "container" : {"max-width": "800px"},
                               "nav-link-selected": {"background-color": "#121010"}})
    
    if selected=="CARD PREVIEW":
        #DISPLAYING THE UPLOADED CARD
        st.markdown("#     ")
        st.markdown("#     ")
        st.markdown("### Card Uploaded")
        st.image(uploaded_card,width=700)
    
    if selected=="EXTRACTION AND STORING":
            if uploaded_card is not None:
                def save_card(uploaded_card):
                    uploaded_cards_dir = os.path.join(os.getcwd(), "uploaded_cards")
                    with open(os.path.join(uploaded_cards_dir, uploaded_card.name), "wb") as f:
                        f.write(uploaded_card.getbuffer())
                save_card(uploaded_card)

                # DISPLAYING THE UPLOADED CARD
                col1, col2 = st.columns(2, gap="large")
                with col1:
                    st.markdown("#     ")
                    st.markdown("#     ")
                    st.markdown("### You have uploaded the card")
                    st.image(uploaded_card)
                # DISPLAYING THE CARD WITH HIGHLIGHTS
                with col2:
                    st.markdown("#     ")
                    st.markdown("#     ")
                    with st.spinner("Please wait processing image..."):
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                        image = cv2.imread(saved_img)
                        res = reader.readtext(saved_img)
                        st.markdown("### Image Processed and Data Extracted")
                        st.pyplot(image_preview(image, res))

                #EASY OCR Extraction
                saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                result = reader.readtext(saved_img, detail=0, paragraph=False)


                # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
                def img_to_binary(file):
                    # Convert image data to binary format
                    with open(file, 'rb') as file:
                        binaryData = file.read()
                    return binaryData


                data = {"company_name": [],
                        "card_holder": [],
                        "designation": [],
                        "mobile_number": [],
                        "email": [],
                        "website": [],
                        "area": [],
                        "city": [],
                        "state": [],
                        "pin_code": [],
                        "image": img_to_binary(saved_img)
                        }


                def get_data(res):
                    for ind, i in enumerate(res):

                        # To get WEBSITE_URL
                        if "www " in i.lower() or "www." in i.lower():
                            data["website"].append(i)
                        elif "WWW" in i:
                            data["website"] = res[4] + "." + res[5]

                        # To get EMAIL ID
                        elif "@" in i:
                            data["email"].append(i)

                        # To get MOBILE NUMBER
                        elif "-" in i:
                            data["mobile_number"].append(i)
                            if len(data["mobile_number"]) == 2:
                                data["mobile_number"] = " & ".join(data["mobile_number"])

                        # To get COMPANY NAME
                        elif ind == len(res) - 1:
                            data["company_name"].append(i)

                        # To get CARD HOLDER NAME
                        elif ind == 0:
                            data["card_holder"].append(i)

                        # To get DESIGNATION
                        elif ind == 1:
                            data["designation"].append(i)

                        # To get AREA
                        if re.findall('^[0-9].+, [a-zA-Z]+', i):
                            data["area"].append(i.split(',')[0])
                        elif re.findall('[0-9] [a-zA-Z]+', i):
                            data["area"].append(i)

                        # To get CITY NAME
                        match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                        match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                        match3 = re.findall('^[E].*', i)
                        if match1:
                            data["city"].append(match1[0])
                        elif match2:
                            data["city"].append(match2[0])
                        elif match3:
                            data["city"].append(match3[0])

                        # To get STATE
                        state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                        if state_match:
                            data["state"].append(i[:9])
                        elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                            data["state"].append(i.split()[-1])
                        if len(data["state"]) == 2:
                            data["state"].pop(0)

                        # To get PINCODE
                        if len(i) >= 6 and i.isdigit():
                            data["pin_code"].append(i)
                        elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                            data["pin_code"].append(i[10:])


                get_data(result)


                # FUNCTION TO CREATE DATAFRAME
                def create_df(data):
                    df = pd.DataFrame(data)
                    return df


                df = create_df(data)
                st.success("### Data Extracted!")
                st.write(df)

                if st.button("Upload to Database"):
                    for i, row in df.iterrows():
                        # here %S means string values
                        sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        mycursor.execute(sql, tuple(row))
                        # the connection is not auto committed by default, so we must commit to save our changes
                        mydb.commit()
                        st.success("#### Uploaded to database successfully!")

if selected=="EDIT":
    
    select = option_menu(None,
                         options=["Make Changes", "Deletion"],
                         default_index=0,
                         icons=["file-minus-fill","trash3-fill"],
                         orientation="horizontal",
                         styles={"nav-link": {"font-size": "12px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "5x"},
                               "container" : {"max-width": "800px"},
                               "nav-link-selected": {"background-color": "#121010"}})
                         

    if select == "Make Changes":
        st.markdown(":white[Make changes in Data Here]")

        try:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.markdown("#### Update or modify any data below")
                mycursor.execute(
                "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=%s",
                (selected_card,))
                result = mycursor.fetchone()

                # DISPLAYING ALL THE INFORMATIONS
                company_name = st.text_input("Company_Name", result[0])
                card_holder = st.text_input("Card_Holder", result[1])
                designation = st.text_input("Designation", result[2])
                mobile_number = st.text_input("Mobile_Number", result[3])
                email = st.text_input("Email", result[4])
                website = st.text_input("Website", result[5])
                area = st.text_input("Area", result[6])
                city = st.text_input("City", result[7])
                state = st.text_input("State", result[8])
                pin_code = st.text_input("Pin_Code", result[9])


                if st.button(":white[Commit changes to DB]"):
                    mycursor.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code,
                    selected_card))
                    mydb.commit()
                    st.success("Information updated in database successfully.")

        except:
            st.warning("There is no data available in the database")

    if select == "Deletion":
        st.subheader(":white[Delete the data]")
        try:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.write(f"### You have selected :white[**{selected_card}'s**] card to delete")
                st.write("#### Do You Really Want to Delete this Card?")
                if st.button("Yes,Proceed to delete this Information from Data"):
                    mycursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                    mydb.commit()
                    st.success("Card Information has been deleted from database.")
        except:
            st.warning("There is no data available in the database")              
  
if selected == "ADDITIONAL INFORMATION":
    filepath=load_lottiefile("E:\data science\Bizcard card data extraction\C.json")
    st.lottie(filepath,speed=1,reverse=False,loop=True,height=100,width=100,quality="highest")
    if st.button(":white[CARD DATABASE]"):
        mycursor.execute(
            "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(mycursor.fetchall(),
                                  columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                           "Email",
                                           "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_df)



