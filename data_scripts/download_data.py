"""This file will download the data we need from the NHS website 

This uses the NHS Covid data available on: ..........

  Typical usage example:

  TODO: add info here
"""

from datetime import datetime, date, timedelta
import urllib.request
import shutil
import glob
import os
import os.path
import pandas as pd
import plotly.graph_objs as go
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=logging.INFO)


class CovidUKData(object):
    """Covid Data we want to analyse

    Attributes:
        data_df: Covid data
    """
    def __init__(self):
        """Initialises the covid data on most recent data.

        It downloads todays data first, if that is not available, it will download yesterdays data.
        
        Args:
            """
        self.build_dates(True)
        self.url = f'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/{self.year}/{self.month}/COVID-19-total-announced-deaths-{self.fulldate}.xlsx'
        self.filename = 'data/COVID-19-total-announced-deaths-' + self.fulldate + '.xlsx'
        self.filename = self.get_nhs_covid_data()
        #self.load_total_deaths_by_region = self.load_total_deaths_by_region()
        logging.info('CovidUKData object created.') 

    def __str__(self):
        string_to_return = f'We will be downloading the data for: {self.fulldate}. \nWe will be fetching the data from: {self.url} \nWhich we will store with the filename: {self.filename}'
        return string_to_return

    def build_dates(self, isToday):
        """Builds urls"""
        if isToday:
            # Todays date
            self.fulldate = datetime.strftime(datetime.now(), '%-d-%B-%Y')
            self.month = datetime.now().strftime("%m")
            self.year = datetime.now().strftime("%Y")
            logging.info(f'Found the date: {self.fulldate}, {self.month}, {self.year}'
)
        else:
            # yesterdays date
            self.fulldate = datetime.strftime(datetime.now() - timedelta(1), '%-d-%B-%Y')
            self.month = datetime.strftime(datetime.now() - timedelta(1), '%m')
            self.year = datetime.strftime(datetime.now() - timedelta(1), '%Y')
            logging.info(f'We are looking for the date: {self.fulldate}'
)

    def set_to_yesterday(self):
        """Changes the state of our object to refer to yesterdays data
        """
        self.build_dates(isToday = False)
        self.url = f'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/{self.year}/{self.month}/COVID-19-total-announced-deaths-{self.fulldate}.xlsx'
        self.filename = 'data/COVID-19-total-announced-deaths-' + self.fulldate + '.xlsx'
        logging.info(f'The url and files to download have been changed to:')
        logging.info(f'url: {self.url}')
        logging.info(f'filename: {self.filename}')
    
    def get_last_file_downloaded(self):
        """
        This returns the last file downloaded to our data folder
        
        Returns:
            filename (str) - name of last downloaded file
        """
        data_files = glob.glob('../data/*.xlsx')
        last_downloaded = max(data_files, key=os.path.getctime)
        return last_downloaded
        logging.info(f'Last file uploaded to server set as: {self.filename}')
    
    def get_nhs_covid_data(self):
        """
        Downloads the latest NHS data from the NHS website.
        
        Args:
            None
        Returns:
            nhs_data (str): location of file
        """
        try:
            logging.info("Attempting to download from the NHS website...")
            # Download the file from `url` and save it locally under `filename`:
            with urllib.request.urlopen(self.url) as response, open(self.filename, 'wb') as filename_to_write:
                shutil.copyfileobj(response, filename_to_write)
            logging.info(f'New File downloaded: {str(self.filename)}')
            return self.filename
        except:
            logging.warning('Todays file is not available - attempting to downloads yesterdays file...') 
            logging.info('url: {str(self.url)}') 
            self.set_to_yesterday()
            try:
                with urllib.request.urlopen(self.url) as response, open(self.filename, 'wb') as filename_to_write:
                    shutil.copyfileobj(response, filename_to_write)
                logging.info(f'New File downloaded: {str(self.filename)}')
                return self.filename
            except:
                logging.warning('Today and yesterday files are not available. We will use the last available file stored on the server.')
                self.filename = self.get_last_file_downloaded()
                return self.filename
 
    def load_total_deaths_by_region(self):
        """This returns total deaths by region
        Returns:
            df: DataFrame of our data
        """
        # store output as dataframe
        df = pd.read_excel(
                            self.filename,
                            #sheet_name='COVID19 total deaths by region', - old sheet name
                            sheet_name='Tab1 Deaths by region',
                            header=15, 
                            index_col=[1]
                )
        
        # Remove empty columns
        df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
        df = df.iloc[2:]
        self.df_total_deaths_by_region = df
        return self.df_total_deaths_by_region

    def load_total_deaths_by_age_group(self):
        """This returns total deaths by age group
        Returns:
            df: DataFrame of our data
        """
        # store output as dataframe
        df = pd.read_excel(
                            self.filename,
                            #sheet_name='COVID19 total deaths by age', - old sheet name
                            sheet_name='Tab3 Deaths by age',
                            header=15, 
                            index_col=[1]
        )
        
        # Remove empty columns
        df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
        df = df.iloc[2:]
        self.df_total_deaths_by_age = df
        return self.df_total_deaths_by_age
    
    def load_deaths_byregion_bytrust(self):
        """This returns total deaths per region by trust
        Returns:
            df: DataFrame with death data per region per trust
        """
        df = pd.read_excel(
                            self.filename,
                            sheet_name='Tab4 Deaths by trust',
                            header=15, 
                            index_col=[1]
        )

        # Remove empty columns
        df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
        df = df.iloc[2:]
        self.df_death_per_region_and_trust = df
        return self.df_death_per_region_and_trust

def scrape_data_from_nhs():
    """
    This method will scrape all links that exist on the NHS website. 

    TODO: Fix this.
    """
    options = Options()
    driver = webdriver.Safari(executable_path = '/usr/bin/safaridriver') 
    driver.get("https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily-deaths/")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by.ID, "chat"))
        )

        links = driver.find_elements_by_partial_link_text("COVID 19 daily")
        for i in links:
            print(i)
            i2 = i.get_attribute("href")
            print(i2)

    except:
        driver.quit()

