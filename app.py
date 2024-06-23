import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

df  = pd.read_csv("startup_cleaned.csv")
df["date"]=pd.to_datetime(df["date"],errors="coerce")
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

st.set_page_config(layout = "wide",page_title="Startup Analysis")

def load_investor(investor):
    st.title(investor)
    
    st.subheader("Most Recent Investments:")
    last5_df = df[df["investors"].str.contains(investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Biggest Investments:")
        big_series = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        st.subheader("Sectors Invested in:")
        vertical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Cities Invested in:")
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        fig, ax = plt.subplots()
        ax.pie(city_series,labels=city_series.index,autopct="%0.01f%%")
        st.pyplot(fig)
    with col2:
        st.subheader("YoY Investment")
        year_series = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
        fig, ax = plt.subplots()
        ax.plot(year_series.index,year_series.values)
        st.pyplot(fig)


def load_overall():
    st.title("Overall Analysis")
  
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        total = round(df["amount"].sum())
        st.metric("Total Amount",str(total)+" Cr")
    with col2:
        maxAmount = df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
        st.metric("Max Amount",str(round(maxAmount))+" Cr")
    with col3:
        avgAmount = df.groupby("startup")["amount"].sum().mean()
        st.metric("Avg Amount",str(round(avgAmount))+" Cr")
    with col4:
        numStartup = df["startup"].nunique()
        st.metric("Funded Startups",str(round(numStartup)))
    st.header("MoM Graph")
    temp_df = df.groupby(["year","month"])["amount"].sum().reset_index()
    temp_df["x_axis"] = temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")
    fig, ax = plt.subplots()
    ax.plot(temp_df["x_axis"],temp_df["amount"])
    st.pyplot(fig)

st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select one",["Overall Analysis","Startup","Investor"])

def load_startup(startup):
    st.title(startup)
    
    st.subheader("Most Recent Funds:")
    last5_df = df[df["startup"].str.contains(startup)].head()[["date","investors","vertical","city","round","amount"]]
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Biggest Funds:")
        big_series = df[df["startup"].str.contains(startup)].groupby("investors")["amount"].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
       st.subheader("YoY Funds")
       year_series = df[df["startup"].str.contains(startup)].groupby("year")["amount"].sum()
       fig, ax = plt.subplots()
       ax.plot(year_series.index,year_series.values)
       st.pyplot(fig)
    
        

if option == "Overall Analysis":
    btn0 = st.sidebar.button("Show Overall Analysis")
    if btn0:
        load_overall()
elif option == "Startup":
    startup = st.sidebar.selectbox("Select startup",sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    if btn1:
        load_startup(startup)
else:
    investor = st.sidebar.selectbox("Select investor",sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor(investor)


