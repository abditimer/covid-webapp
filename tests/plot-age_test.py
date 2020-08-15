import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df = pd.read_excel(     
                            'data/COVID-19-total-announced-deaths-20-May-2020.xlsx',
                            sheet_name='COVID19 total deaths by age',
                            header=15, 
                            index_col=[1]
                )
        
# Remove empty columns
df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
df = df.iloc[2:]

total_deaths_per_age_group_dict = df['Total'].to_dict()

age_groups_labels = list(total_deaths_per_age_group_dict.keys())
age_group_deaths_values = list(total_deaths_per_age_group_dict.values())

fig = go.Figure(
    data = [
        go.Pie(
            labels=age_groups_labels,
            values=age_group_deaths_values,
            textinfo='label+percent',
        )
    ]
)

# ----------------


if __name__ == '__main__':
    fig.update_layout(
        title='Total Deaths by Age Group - UK'
    )

    # annotations = []

    # for yd, xd in zip(y_d, x_d):
    #     annotations.append(dict(xref='x1', yref='y1',
    #                             y=yd, x=xd + 200,
    #                             text=str(xd),
    #                             font=dict(family='Arial', size=12),
    #                             showarrow=False
    #                             ))
    # fig.update_layout(annotations=annotations)
    fig.show()
    

