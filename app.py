
import streamlit as st
from streamlit import delta_generator
from streamlit.elements import image, text
from notion import *
from plots import *
from statistics import mean
import plotly.graph_objects as go
from modulefinder import ModuleFinder
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


st.set_page_config(layout="wide")
st.title("Life Tracker")
st.caption("Enter your notion api info up there to get started!")

user_dataId=st.sidebar.text_input("Enter your DataBaseID:").strip('"')
integration_token=st.sidebar.text_input("Enter your integration token:").strip('"')


if len(integration_token and user_dataId):
    def load_data():
        nsync = NotionSync()
        data = nsync.query_databases(integration_token,user_dataId)
        metrics = nsync.get_metrics_titles(data)
        metrics_data = nsync.get_metrics_data(data,metrics)
        df = setupProjectsDf(metrics_data)
        return df

    df = load_data()
   
    
    st.dataframe(df.tail())
    
   
    st.header("Ticker")
    

    with st.expander("See how your ticker is calculated:"):
        st.latex("\displaystyle\sum_{i=1}^5x_i *k^n = (x_1 + x_2 + x_3 + x_4) * 1.01^{n})")
        st.markdown("""
            * $$x1, x2, x3, x4, x5$$: metrics, rated from 0 to 5.           
            * $k$: constant, $1.01$ is the growth rate
            * $n$: the number of days you have tracked
            """)
        
    row1_col1,row1_col2 = st.columns(2)
    row1_col1.plotly_chart(ticker_plot(df))
    row1_col2.plotly_chart(metric_plot(df))

    st.markdown("---")
#Metrics
    st.header("Average Metric Scores:")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Satisfaction", value=round(mean(df["Satisfaction"]), 2), delta= metric_calc(df["Satisfaction"]))
    col2.metric(label="Personal Development", value=round(mean(df["Personal Development"])), delta= metric_calc(df["Personal Development"]))
    col3.metric(label="Professional Development", value=round(mean(df["Professional Development"])), delta= metric_calc(df["Professional Development"]))
    col4.metric(label="Health", value=round(mean(df["Health"]), 2), delta= metric_calc(df["Health"]))

#indicator gauge might remove
    st.header("Indicator Gauge")
    col1, col2, col3, col4 = st.columns(4)
    col1.plotly_chart(metric_dash(df['Satisfaction']))
    col2.plotly_chart(metric_dash(df['Personal Development']))
    col3.plotly_chart(metric_dash(df['Professional Development']))
    col4.plotly_chart(metric_dash(df['Health']))

else:
    pass

        


