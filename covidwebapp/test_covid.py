from data_scripts import download_data, clean_data, return_figs

ts = download_data.CovidUKData()
ts.scrape_data_from_nhs()