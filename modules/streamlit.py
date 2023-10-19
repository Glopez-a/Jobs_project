import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules import chatgpt as chat
from modules import scrapping as scrp
from modules import utils as utl
from PIL import Image
from io import StringIO



def streamlit(df):
    st.title('JobConnect+')
    st.header("Your Gateway to New Opportunities")
    info_columns = ['Name','Overall','Culture','Diversity','Conciliation','Managers','Salaries','Opportunitys','FriendRecomendation','CEO','Outlook']

    tab1, tab2, tab3 = st.tabs(["General Information", "Companies Comparison", "Job"])

    with tab1:
        sizing = st.radio("Global Company Size you are looking for\n",
    ('ALL','+10000','5001 - 10000','1001 - 5000','501 - 1000','201 - 500','51 - 200','1 - 50'))
        my_dict = {'1 - 50': '1 to 50 Employees', '51 - 200': '51 to 200 Employees', '201 - 500': '201 to 500 Employees', '501 - 1000': '501 to 1000 Employees', '1001 - 5000': '1001 to 5000 Employees', '5001 - 10000': '5001 to 10000 Employees', '+10000': '10000+ Employees','ALL': ''}
        st.header("Companies information")
        if sizing == 'ALL':    
            st.dataframe(df[info_columns], use_container_width=True)
        else:
            filtered_df = df[df['Sizing'] == my_dict[sizing]]
            st.dataframe(filtered_df[info_columns], use_container_width=True)

        #if st.button("CLICK HERE TO ADD 10 MORE COMPANIES TO THE DATABASE! :sunglasses:"):
        #    scrp.get_info(10, conn, df)
        # st.write("If you cant find the companie you are looking for, tell me its name and i will do my best to get some info:)")
        # title = st.text_input('Companie name', 'Here')
        # if title:
        #     scrp.get_companie_by_name(title, conn)


    with tab2:
        columns_99 = ['FriendRecomendation','CEO','Outlook']
        df1 = pd.DataFrame()
        df1 = df.loc[:, ['Name','Overall','Culture','Diversity','Conciliation','Managers','Salaries','Opportunitys','FriendRecomendation','CEO','Outlook']]
        df1[columns_99] = df1[columns_99].applymap(utl.range_it)
        st.header("Companies comparison")
        st.write("Add two companies names\n")
        options = []
        options = st.multiselect('Lets compare some companies',list(df1['Name']))
        df_lines = pd.DataFrame()
        df_lines = df1[df1['Name'].isin(options)]
        print("Options = " , options)
        print(df_lines)
        line_traces = []
        for _, row in df_lines.iterrows():
            # Extract the row values
            line_values = row.values[1:]

            # Create a line trace for the row
            line_trace = go.Scatter(x=df_lines.columns[1:], y=line_values, mode='lines', name=row['Name'])

            # Add the line trace to the list
            line_traces.append(line_trace)

        # Create the layout for the plot
        layout = go.Layout(title='')

        # Create the figure and add the line traces
        figure = go.Figure(data=line_traces, layout=layout)

        # Display the plot
        st.plotly_chart(figure, use_container_width=True)




    with tab3:
        st.header("Dear Human Resources...")
        uploaded_file = st.file_uploader("Add your Curriculum Vitae")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            #st.write(bytes_data)


        col1, col2 = st.columns([2, 2])
        offer_id = col1.text_input('Insert the linkedin offer id')
        if offer_id:
            print("OFFER ID IS " + offer_id + "\n\n\n")
            offer_text = scrp.get_text(offer_id)
        image = Image.open('example.jpeg')
        col2.image(image, caption='offer id example')
        if offer_id and uploaded_file:
            response = chat.get_response(bytes_data, offer_text)
            offer_id = None
            col1.write(response)
