import streamlit as st
import os
import sqlite3
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

Token='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'


## Function To Load Google Gemini Model and provide queries as response

def get_response(question,prompt):
    llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    groq_api_key=Token,
    # other params...
)
    chain = prompt | llm 
    response=chain.invoke(input={'question':question})
    return response

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

prompt = PromptTemplate.from_template(
        """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output \n\n
    convert now this {question} to SQL query        
            
        """
)

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("MLL App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_response(question,prompt)
    st.header(response.content)
    response=read_sql_query(response.content,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)