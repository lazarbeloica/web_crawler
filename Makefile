PYTHON=`which python`
WEB_CRAWLER=disscoz_crawler

test:
	@cd ${WEB_CRAWLER}; ${PYTHON} -m unittest discover

run:
	@cd ${WEB_CRAWLER}; scrapy crawl -a country_to_scrape=Serbia discoz_spider