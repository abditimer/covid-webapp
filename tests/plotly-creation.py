import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df = pd.read_excel(
                    'data/COVID-19-total-announced-deaths-19-May-2020.xlsx',
                    sheet_name='COVID19 total deaths by region',
                    header=15, 
                    index_col=[1]
        )

# Remove empty columns
df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
df = df.iloc[2:]
total_deaths_per_region_dict = df['Total'].to_dict()
df.drop(['Awaiting verification', 'Total'], axis=1,inplace=True)
# melt the table
df.reset_index(inplace=True)
df = pd.melt(df, id_vars='NHS England Region', var_name='Date', value_name='Deaths')
df.rename(columns={'NHS England Region': 'NHS_England_Region'}, inplace=True)

# filter out values before 1st March
df = df[df.Date != 'Up to 01-Mar-20']
df['Date'] =pd.to_datetime(df.Date)


# --------------
# Time to build bar chart
list_of_nhs_regions = df.index.unique()
y_d = list(total_deaths_per_region_dict.keys())
x_d = list(total_deaths_per_region_dict.values())


fig = go.Figure(
    [
        go.Bar(
            y=y_d,
            x=x_d,
            orientation='h',
            name='Total Deaths by Region (UK)'
        )
    ]
)

# ----------------


if __name__ == '__main__':
    fig.update_layout(
        title='Total Deaths by region - UK',
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True
        ),
    )

    annotations = []

    for yd, xd in zip(y_d, x_d):
        annotations.append(dict(xref='x1', yref='y1',
                                y=yd, x=xd + 200,
                                text=str(xd),
                                font=dict(family='Arial', size=12),
                                showarrow=False
                                ))
    fig.update_layout(annotations=annotations)
    fig.show()
    
