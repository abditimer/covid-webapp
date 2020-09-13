"""This file will aim to take the cleaned data, and put it into a format for plotly.
"""
from data_scripts import download_data, clean_data
import plotly.graph_objs as go
import pandas as pd
import logging

class CovidFigures():
    """
    This class will return all the figures needed for the front end.
    """
    def __init__(self):
        logging.info('Creating CovidFigures object...')
        self.covid_cleaned_data = clean_data.CovidDataCleaned()

        self.figures = []
        self.figures_p2 = []
        
        self.totaldeaths_by_region()
        self.totaldeaths_by_age()
        self.totaldeaths_per_region_by_trusts()

        self.ids = ['figures-{}'.format(i) for i, _ in enumerate(self.figures)]
        self.ids_p2 = ['sankey-{}'.format(i) for i, _ in enumerate(self.figures_p2)]
        self.home_page_names = [f'figure-{figure_name}' for figure_name, _ in enumerate(self.home_page_figure)] 
        self.data_page_names = [f'figure-{figure_name}' for figure_name, _ in enumerate(self.data_page_figures)]
        

    def totaldeaths_by_region(self):
        """
        Bar Chart: Total Deaths by Region
        """
        # Get the data we need
        total_deaths_per_region_dict = self.covid_cleaned_data.get_total_deaths_by_region()
        region_names_lst = list(total_deaths_per_region_dict.keys())
        total_deaths_lst = list(total_deaths_per_region_dict.values())

        trace0 = go.Bar(
                            x = region_names_lst,
                            y = total_deaths_lst,
                        )

        layout1 = dict(
            #title='Total Deaths by Region (UK)',
            # xaxis=dict(
            #     zeroline=False,
            #     showline=False,
            #     showticklabels=True,
            #     showgrid=True
            # )
        )
        
        data=[trace0]
        self.figures.append(dict(data=data, layout=layout1))

        self.home_page_figure = []
        self.home_page_figure.append(dict(data=data, layout=layout1))

    def totaldeaths_by_age(self):
        """
        Pie Chart: Total deaths by Age Group
        """
        total_deaths_per_age_group_dict = self.covid_cleaned_data.get_total_deaths_by_age()
        age_groups_labels = list(total_deaths_per_age_group_dict.keys())
        age_group_deaths_values = list(total_deaths_per_age_group_dict.values())

        trace0 = go.Pie(
            labels = age_groups_labels,
            values = age_group_deaths_values,
            textinfo = 'label+percent',
        )
        layout1 = dict(
            #title = 'Total Deaths by Age Group - UK'
        )
        data = [trace0]
        self.figures.append(dict(data=data, layout=layout1))
        # send the data page
        self.data_page_figures = []
        self.data_page_figures.append(dict(data=data, layout=layout1))

    def totaldeaths_per_region_by_trusts(self):
        """
        Sankey Chart: Shows top three trusts that have highest deaths per region
        """
        source_and_target_distinct_list, source_list, target_list, value, colours = self.covid_cleaned_data.get_deaths_by_region_by_trust(3, ['London', 'Midlands'])

        data = [ 
                    go.Sankey(
                            node = dict(
                                pad = 15,
                                thickness = 20,
                                line = dict(color = "black", width = 0.5),
                                label = source_and_target_distinct_list,
                                #color = colours
                            ),
                            link = dict(
                                source = source_list,
                                target = target_list,
                                value = value
                            )
                    )
        ]
        layout1 = dict(
            #title = 'Trusts with the most deaths per region'
        )
        self.figures_p2.append(dict(data=data, layout=layout1))
        self.data_page_figures.append(dict(data=data, layout=layout1))