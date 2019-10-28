# open-data-ph-scraper
Downloads datasets from https://data.gov.ph.
Written and tested with **Python 3.7**.

## How to run:
Install requirements:
```
pip install -r requirements.txt
```
Run the spider *(search keyword required)*:
```
scrapy runspider open_data_ph_spider.py -a keyword=agriculture
```
Datasets are saved in `/tmp/opendataph`

## Warning:
This does not have throttling or user-agent rotation as of the moment so use this sparingly.
