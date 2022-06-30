from scraper import Scraper

print('This scraper has returned deals from hotdealsuk.com, the data is in a json file')

deals = Scraper()

deals.accecept_cookies()
deals.find_container()
deals.save_data()
deals.upload_file()
deals.upload_to_RDS()

