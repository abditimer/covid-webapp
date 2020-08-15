import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df_original = pd.read_excel(
                    'data/COVID-19-total-announced-deaths-23-May-2020.xlsx',
                    sheet_name='Tab1 Deaths by region',
                    header=15, 
                    index_col=[1]
        )

df = df_original.copy()
df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
df = df.iloc[0:1]
df.drop(['Awaiting verification', 'Total'], axis=1,inplace=True)
df = df.reset_index()
df.rename(columns={'NHS England Region': 'NHS_England_Region'}, inplace=True)
df = pd.melt(df, id_vars=['NHS_England_Region'], var_name='Date', value_name='Deaths')
df = df[df['Date'] != 'Up to 01-Mar-20']
df['Date'] =pd.to_datetime(df.Date)



df2 = df_original.copy()
df2.drop(df2.filter(regex="Unname"),axis=1, inplace=True)
df2 = df2.iloc[2:]
df2.drop(['Awaiting verification', 'Total'], axis=1,inplace=True)
df2 = df2.reset_index()
df2 = pd.melt(df2, id_vars=['NHS England Region'], var_name='Date', value_name='Deaths')
df2 = df2[df2['Date'] != 'Up to 01-Mar-20']
df2['Date'] =pd.to_datetime(df2.Date)

df2 = df2.groupby(['NHS England Region','Date']).sum().groupby(level=0).cumsum().reset_index()

# East Of England
df_east = df2[df2['NHS England Region'] == 'East Of England']
y_ne1 = df_east['Deaths'].to_list()
x_ne1 = df_east['Date'].to_list()
name1 = 'East Of England'
# London
df_east = df2[df2['NHS England Region'] == 'London']
y_ne2 = df_east['Deaths'].to_list()
x_ne2 = df_east['Date'].to_list()
name2 = 'London'
# Midlands
df_east = df2[df2['NHS England Region'] == 'Midlands']
y_ne3 = df_east['Deaths'].to_list()
x_ne3 = df_east['Date'].to_list()
name3 = 'Midlands'
# North East And Yorkshire
df_east = df2[df2['NHS England Region'] == 'North East And Yorkshire']
y_ne4 = df_east['Deaths'].to_list()
x_ne4 = df_east['Date'].to_list()
name4 = 'North East And Yorkshire'
# North West
df_east = df2[df2['NHS England Region'] == 'North West']
y_ne5 = df_east['Deaths'].to_list()
x_ne5 = df_east['Date'].to_list()
name5 = 'North West'

fig = go.Figure()

fig.add_trace(go.Scatter(x=x_ne1, y=y_ne1,
                    mode='lines+markers',
                    name=name1
                    ))
fig.add_trace(go.Scatter(x=x_ne2, y=y_ne2,
                    mode='lines+markers',
                    name=name2
                    ))
fig.add_trace(go.Scatter(x=x_ne3, y=y_ne3,
                    mode='lines+markers',
                    name=name3
                    ))
fig.add_trace(go.Scatter(x=x_ne4, y=y_ne4,
                    mode='lines+markers',
                    name=name4
                    ))
fig.add_trace(go.Scatter(x=x_ne5, y=y_ne5,
                    mode='lines+markers',
                    name=name5
                    ))        

fig.show()

fig = go.Figure([
    go.Scatter(
        x=df['Date'], 
        y=df['Deaths']
        )
    ]
)
#fig.show()

