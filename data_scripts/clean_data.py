"""This file will clean the data we downloaded from the NHS website

"""

from data_scripts import download_data
import plotly.graph_objs as go
import pandas as pd
import logging

class CovidDataCleaned:
    """
    This class will clean the data downloaded from the NHS website.
    """

    # Get the most recent data available to us
    def __init__(self):
        self.data = download_data.CovidUKData()

    def get_total_deaths_by_region(self):
        """
        This method returns data around the total deaths by region
        
        Returns:
            total_deaths_per_region_dict (dict):
                Dictionary mapping regions with total deaths
        """
        logging.info('Cleaning data to return total deaths by region...')
        df = self.data.load_total_deaths_by_region()
        total_deaths_per_region_dict = df['Total'].to_dict()

        # TODO: create cumsum dataset
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
        

        print('data has been cleaned.')
        return total_deaths_per_region_dict
         
    def get_total_deaths_by_age(self):
        """
        This method returns data around total deaths by age

        Returns:
            total_deaths_per_age_group_dict (dict)
                Dictionary mapping total deaths to age groups
        """
        print('Cleaning data to return total deaths by age group...')
        df = self.data.load_total_deaths_by_age_group()
        total_deaths_per_age_group_dict = df['Total'].to_dict()
        return total_deaths_per_age_group_dict

    def get_deaths_by_region_by_trust(self, split_by):
        """
        This method returns each regions death data for the UK.

        To understand the data format being returned, you will need to
        understand how Sankey charts are created.

        Google a picture of a Sankey chart in order to understand the need
        for the following three lists (or - visit plotly's docs).

        Returns:
            source_and_target_distinct_list (list)
                distinct list with all sankey chart node names
            source_list (list)
                lists that map to distinct list: for left node
            target_list (list)
                lists that map to distinct list: for right node
        """
        print("Cleaning data for Sankey chart...")
        df = self.data.load_deaths_byregion_bytrust()

        # filter df & rename columns
        df = df[['Name', 'Total']]
        df.reset_index(inplace=True)
        df = df.rename(columns={'NHS England Region': 'Region', 'Name': 'Trust'})
        df = df.replace('London ', 'London')
        # find three trusts per region with the highest deaths
        df_agg = df.groupby(['Region','Trust']).max()
        df_agg = df_agg['Total'].groupby(level=0, group_keys=False).nlargest(split_by)
        df_agg = df_agg.reset_index()
        # create lists for each column of interest
        sources = df_agg['Region'].tolist()
        targets = df_agg['Trust'].tolist()
        value = df_agg['Total'].tolist()
        sources_distinct = df_agg['Region'].drop_duplicates().tolist()
        targets_distinct = df_agg['Trust'].drop_duplicates().tolist()
        # combine to one list
        full_list = [*sources, *targets]
        source_and_target_distinct_list = [*sources_distinct, *targets_distinct]
        # create dictionary in order to create list with index placements instead of values
        full_map = {value: index for (index, value) in enumerate(source_and_target_distinct_list)}
        # Copy list
        source_list = [full_map.get(i) for i in sources]
        target_list = [full_map.get(i) for i in targets]
        # Create colours to return
        df['color'] = df.apply(self.sankey_assign_colour, axis = 1)
        color_map_region = dict(zip(df.Region,df.color))
        color_map_trust = dict(zip(df.Trust,df.color))
        colors = []
        for region_or_trust in source_and_target_distinct_list:
            if region_or_trust in color_map_region:
                colors.append(color_map_region.get(region_or_trust))
            else:
                colors.append(color_map_trust.get(region_or_trust))
        

        print("Data clean complete.")
        return source_and_target_distinct_list, source_list, target_list, value, colors

    def sankey_assign_colour(self, df):
        """
        helper function that creates colours for our df
        """

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

    