import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df = pd.read_excel(
                    'data/COVID-19-total-announced-deaths-23-May-2020.xlsx',
                    sheet_name='Tab4 Deaths by trust',
                    header=15, 
                    index_col=[1]
        )

# Remove empty columns
df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
df = df.iloc[2:]
df_trust = df[['Name', 'Total']]
df_trust.reset_index(inplace=True)
df = df_trust.copy()
df = df.rename(columns={'NHS England Region': 'Region', 'Name': 'Trust'})
df = df.replace('London ', 'London')

df_agg = df.groupby(['Region','Trust']).max()
df_agg = df_agg['Total'].groupby(level=0, group_keys=False).nlargest(3)
df_agg = df_agg.reset_index()

# create lists
sources = df_agg['Region'].tolist()
targets = df_agg['Trust'].tolist()
value = df_agg['Total'].tolist()

sources_distinct = df_agg['Region'].drop_duplicates().tolist()
targets_distinct = df_agg['Trust'].drop_duplicates().tolist()
print(sources_distinct)
# combine to one list
full_list = [*sources, *targets]
source_and_target_distinct_list = [*sources_distinct, *targets_distinct]

# create dictionary
full_map = {value: index for (index, value) in enumerate(source_and_target_distinct_list)}

print('-'*30)
# Copy list
source_list = [full_map.get(i) for i in sources]
target_list = [full_map.get(i) for i in targets]


def assign_colour(df):

    if (df['Region'] == 'East Of England'):
        return 'brown'
    elif (df['Region'] == 'London'):
        return 'seagreen'
    elif (df['Region'] == 'Midlands'):
        return 'crimson'
    elif (df['Region'] == 'North East And Yorkshire'):
        return 'blue'
    elif (df['Region'] == 'North West'):
        return 'indigo'
    elif (df['Region'] == 'South East'):
        return 'darkviolet'
    elif (df['Region'] == 'South West'):
        return 'tomato'

df['color'] = df.apply(assign_colour, axis = 1)

color_map_region = dict(zip(df.Region,df.color))
color_map_trust = dict(zip(df.Trust,df.color))

colors = []
for region_or_trust in source_and_target_distinct_list:
    if region_or_trust in color_map_region:
        colors.append(color_map_region.get(region_or_trust))
    else:
        colors.append(color_map_trust.get(region_or_trust))
print(colors)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = source_and_target_distinct_list,
      color = colors
    ),
    link = dict(
      source = source_list,
      target = target_list,
      value = value,
      hovertemplate = 'Total Deaths from this trust: %{value}'
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()



# df = df.rename(columns={'NHS England Region': 'source', 'Name': 'platform', 'Total': 'count'})

# # First, we get a list of all of sources, remove duplicates, and make this a list
# sources = df["source"].drop_duplicates().tolist()

# # Then, we get a list of all of platforms (our targets), remove duplicates, and make this a list
# platforms = df["platform"].drop_duplicates().tolist()

# # Finally, create a list of all our nodes. We will use this for giving an id to each node for plot.ly
# all_nodes = sources + platforms

# # Keeping the size of our dataframes, this would be useful for applying the same color for each "node" and "link" of our sankey diagram, if we so choose to do so
# n = len(all_nodes)
# n2 = len(df["source"])

# # Create a dataframe that has all of the node ids. We will join this to the original data frame to reference later
# df1 = pd.DataFrame(all_nodes, columns = ['node'])
# df1 = df1.reset_index()
# df2 = pd.merge(pd.merge(df, df1, how = 'inner', left_on = "source", right_on ="node"), df1, how = 'inner', left_on = "platform", right_on ="node", suffixes = ('_source','_target'))



# Setting up the data in the plotly "data" argument.
# The nodes are described in the "node" dictionary (these are the vertical rectangles in the diagram)
# The links are described in the "link" dictionary. These have 3 attributes, the "source" (the index of the node they start at), the "target" (the index of the node they end at), and the "value" the thickness of the band. Additional attributes, such as color can also be specified.
# data = dict(
#     type='sankey',
#     node = dict(
#       pad = 15,
#       thickness = 20,
#       line = dict(
#         color = "#435951",
#         width = 0.5
#       ),
#       label = all_nodes,
#       color = ["#84baa6"] * n
#     ),
#     link = dict(
#       source = df2["index_source"],
#       target = df2["index_target"],
#       value = df2["count"],
#       color = ['#bdf9e5'] * n2
#   ))

# # Setting up the layout settings in the "layout" argument
# layout =  dict(
#     title = "An Example Sankey Diagram",
#     font = dict(
#       size = 12
#     )
# )

# fig = dict(data=[data], layout=layout)

# fig.show()





# fig = go.Figure(data=[go.Sankey(
#     valueformat = ".0f",
#     valuesuffix = "TWh",
#     # Define nodes
#     node = dict(
#       pad = 15,
#       thickness = 20,
#       line = dict(
#         color = "#435951",
#         width = 0.5
#       ),
#       label = all_nodes,
#       color = ["#84baa6"] * n
#     ),
#     link = dict(
#       source = df2["index_source"],
#       target = df2["index_target"],
#       value = df2["count"],
#       color = ['#bdf9e5'] * n2
#   ))
# ])

# fig.show()























def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig

#total_deaths_per_region_dict = df['Total'].to_dict()


# df.drop(['Awaiting verification', 'Total'], axis=1,inplace=True)
# # melt the table
# df.reset_index(inplace=True)
# df = pd.melt(df, id_vars='NHS England Region', var_name='Date', value_name='Deaths')
# df.rename(columns={'NHS England Region': 'NHS_England_Region'}, inplace=True)

# # filter out values before 1st March
# df = df[df.Date != 'Up to 01-Mar-20']
# df['Date'] =pd.to_datetime(df.Date)


# # --------------
# # Time to build bar chart
# list_of_nhs_regions = df.index.unique()
# y_d = list(total_deaths_per_region_dict.keys())
# x_d = list(total_deaths_per_region_dict.values())


# fig = go.Figure(
#     [
#         go.Bar(
#             y=y_d,
#             x=x_d,
#             orientation='h',
#             name='Total Deaths by Region (UK)'
#         )
#     ]
# )

# # ----------------


# if __name__ == '__main__':
#     fig.update_layout(
#         title='Total Deaths by region - UK',
#         xaxis=dict(
#             zeroline=False,
#             showline=False,
#             showticklabels=True,
#             showgrid=True
#         ),
#     )

#     annotations = []

#     for yd, xd in zip(y_d, x_d):
#         annotations.append(dict(xref='x1', yref='y1',
#                                 y=yd, x=xd + 200,
#                                 text=str(xd),
#                                 font=dict(family='Arial', size=12),
#                                 showarrow=False
#                                 ))
#     fig.update_layout(annotations=annotations)
#     fig.show()
    
