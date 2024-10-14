import streamlit as st
import pandas as pd
import mysql.connector as db
import plotly.express as px
from streamlit_option_menu import option_menu


import pymysql

mydb = pymysql.connect(
    host='localhost',
    user='root',
    password='Ke$hw0rd-12345',
    database='gitdata'
)
mycursor = mydb.cursor()

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM reposit")
data = mycursor.fetchall()

column_names = [i[0] for i in mycursor.description]
df = pd.DataFrame(data, columns=column_names)
mycursor.close()
mydb.close()


with st.sidebar:
      opt = option_menu("Menu",  
             ['HOME','EXPLORE','INSIGHTS'])


if opt=="HOME":

        st.title(''':red[_GITHUB DATA DIVE_]''')
    
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[DOMAIN :] OPEN SOURCE SOFTWARE ANALYTICS ")
        st.write(" ")
        col1,col2 = st.columns([6,7],gap="medium")
        with col1:
          st.markdown("""
                     ### :violet[TECHNOLOGIES USED :]
                    
                        - GITHUB API
                        - PYTHON
                        - PANDAS
                        - MYSQL
                        - STREAMLIT
                        - DATA ANALYSIS
                        - DATA VISUALIZATION
                    
                    """)
        st.markdown("### :violet[OVERVIEW :]  This project aims to extract and analyze data from GitHub repositories focused on specific topics,to uncover patterns and trends in repository characteristics, popularity, and technology usage. By leveraging the GitHub API, the project seeks to provide a comprehensive overview of repository dynamics, including metrics like stars, forks, programming languages, and creation dates.")
        with col2:
          st.write(" ")
          st.write(" ")
          st.write(" ")
    

       
if opt=="EXPLORE":
        
        # Filter by Programming Language
        languages = df['Programming_Language'].unique()
        selected_language = st.selectbox("Select Programming Language", languages)
        filtered_df = df[df['Programming_Language'] == selected_language]
        
        col,coll,col2 = st.columns([2,2,2],gap="small")
        with col:
        # Display basic metrics

          st.write(f"Total Repositories for {selected_language}: {filtered_df.shape[0]}")
        with coll:

          st.write(f"Total Stars for {selected_language}: {filtered_df['Number_of_Stars'].sum()}")
        with col2:

           st.write(f"Total Forks for {selected_language}: {filtered_df['Number_of_Forks'].sum()}")

        
        # Top repositories by stars
        st.subheader(f"Top 10 Starred Repositories in {selected_language}")
        top_repos = filtered_df[['Repository_Name', 'Number_of_Stars', 'URL']].rename(columns={"Repository_Name":"Repository Name", 'Number_of_Stars': 'Number of Stars'}).sort_values(by='Number of Stars', ascending=False).head(10)
        st.table(top_repos)


        st.subheader(f"Top 10 Forked Repositories in {selected_language}")   #10 Fork
        top_repos1 = filtered_df[['Repository_Name', 'Number_of_Forks', 'URL']].rename(columns={"Repository_Name":"Repository Name", 'Number_of_Forks': 'Number of Forks'}).sort_values(by='Number of Forks', ascending=False).head(10)
        st.table(top_repos1)

        st.subheader(f"Top 10 Recently Updated Repositories in {selected_language}")      #  10 Recently Updated    
        top_repos2 = filtered_df[['Repository_Name', 'Last_Updated_Date', 'URL']].rename(columns={"Repository_Name":"Repository Name", 'Last_Updated_Date': 'Recently Updated Date'}).sort_values(by='Recently Updated Date', ascending=False).head(10)
        st.table(top_repos2)

        st.subheader("Explore All The Repositories")       #All  Repositories
        all_repos = filtered_df[['Repository_Name', 'URL']]
        repo_count = all_repos.shape[0]
        st.write(all_repos)
        st.write("\nTotal number of repositories:", repo_count)






if opt=="INSIGHTS":
        
        st.write(" ")
        st.write(" ")
        st.write(" ")
        
        
        languages = df['Programming_Language'].unique()
        selected_language = st.selectbox("Select Programming Language", languages)
        filtered_df = df[df['Programming_Language'] == selected_language]


        st.subheader("Forks Distribution")
        #  donut chart with repository names and number of forks
        fig1 = px.pie(filtered_df, 
                    names='Repository_Name',      
                    values='Number_of_Forks',   
                    hole=0.3)                    

        fig1.update_traces(textinfo='percent+label')  
        fig1.update_layout(xaxis_title='Repository Name', 
                        yaxis_title='Number of Forks',  
                        height=700)                    
        st.plotly_chart(fig1, use_container_width=True) 
        
        
        st.subheader("Stars vs Forks: Repository Comparison")    #Stars vs Forks scatter plot
        fig = px.scatter(df, 
                        x='Number_of_Stars', 
                        y='Number_of_Forks', 
                       
                        labels={'Number_of_Stars': 'Number of Stars', 'Number_of_Forks': 'Number of Forks'},
                        hover_name='Repository_Name',  
                        color='Programming_Language',  
                        size='Number_of_Stars',       
                        size_max=20,                   
                        color_continuous_scale='Viridis')

        fig.update_layout(xaxis_title='Number of Stars',
                        yaxis_title='Number of Forks',
                        height=600,
                        showlegend=True)
        st.plotly_chart(fig)
                


        st.subheader("Last Updated Date Trend")       # Last Updated Date line plot
        filtered_df['Last_Updated_Date'] = pd.to_datetime(filtered_df['Last_Updated_Date'])
        repo_update_trend = filtered_df.groupby('Last_Updated_Date').size().reset_index(name='Repository Count')

        figg = px.line(repo_update_trend, 
                    x='Last_Updated_Date', 
                    y='Repository Count', 
                    markers=True)  
        figg.update_layout(xaxis_title='Last Updated Date', 
                        yaxis_title='Number of Repositories', 
                        height=600)  
        st.plotly_chart(figg, key='last_updated_trend_chart')  



        df['Programming_Language'] = df['Programming_Language'].fillna('Unknown')
        languages = df['Programming_Language'].unique()
        repo_count_by_lang = df['Programming_Language'].value_counts().reset_index()
        repo_count_by_lang.columns = ['Programming Language', 'Repository Count']


        st.subheader("Repository Count by Programming Language")   #Repository Count by Prog lang bar plot
        fig = px.bar(repo_count_by_lang, 
                    x='Programming Language', 
                    y='Repository Count',
                    
                    labels={'Programming Language':'Programming Language', 'Repository Count':'Number of Repositories'},
                    color='Repository Count',
                    color_continuous_scale='Blues')

        fig.update_layout(xaxis_title='Programming Language',
                        yaxis_title='Number of Repositories',
                        xaxis_tickangle=-45,
                        height=600,  
                        showlegend=False, 
                        bargap=0.1) 

        fig.update_xaxes(categoryorder='total descending')  
        st.plotly_chart(fig)


        st.subheader("Open Issues Distribution")  # Open Issues  bar plot
        fig2 = px.bar(filtered_df, 
                    x='Repository_Name',           
                    y='Number_of_Open_Issues',   
                    color_discrete_sequence=px.colors.sequential.Cividis,
                    labels={'Number_of_Open_Issues': 'Number of Open Issues'})  

        fig2.update_layout(xaxis_title='Repository Name', 
                        yaxis_title='Number of Open Issues',  
                        xaxis_tickangle=-45,                    
                        height=600,                            
                        showlegend=False)                      

        st.plotly_chart(fig2, use_container_width=True)  

        st.subheader("3D Scatter Plot of Repositories by License Type")   #3D Scatter Plot of Repositories by License Type
        filtered_df['License_Type'] = filtered_df['License_Type'].fillna('Unknown')

        # 3D scatter plot
        fig = px.scatter_3d(
            filtered_df,
            x='Number_of_Stars',           
            y='Number_of_Forks',            
            z='Number_of_Open_Issues',      
            color='License_Type',          
    
            labels={
                'Number_of_Stars': 'Number of Stars',
                'Number_of_Forks': 'Number of Forks',
                'Number_of_Open_Issues': 'Number of Open Issues',
                'License_Type': 'License Type'
            },
            hover_name='Repository_Name',    
            opacity=0.7                     
        )

        fig.update_layout(
            scene=dict(
                xaxis_title='Number of Stars',
                yaxis_title='Number of Forks',
                zaxis_title='Number of Open Issues',
            ),
            height=700  
        )
        st.plotly_chart(fig, use_container_width=True)  

        



        st.subheader("Repositories Created Over Time")
        filtered_df['Creation_Date'] = pd.to_datetime(filtered_df['Creation_Date'])   #Repositories Created Over Time hist
        fig4 = px.histogram(filtered_df, 
                        x='Creation_Date', 
                        labels={'Creation_Date': 'Creation Date'},
                        nbins=30,  
                        color_discrete_sequence=px.colors.qualitative.Set1)  

        fig4.update_layout(xaxis_title='Creation Date', 
                        yaxis_title='Number of Repositories', 
                        height=600)  

        st.plotly_chart(fig4, use_container_width=True) 


        # stars distribution
        st.subheader("Stars Distribution")
        st.bar_chart(data=filtered_df.set_index('Repository_Name')['Number_of_Stars'])

        st.subheader("Forks Distribution")   # Number_of_Forks 
        fig = px.line(filtered_df, y='Repository_Name', x='Number_of_Forks', color_discrete_sequence=px.colors.sequential.Greens)
        st.plotly_chart(fig)