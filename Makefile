PYTHON=`which python`
WEB_CRAWLER=disscoz_crawler

test:
	@cd ${WEB_CRAWLER}; ${PYTHON} -m unittest discover

runSerb:
	@cd ${WEB_CRAWLER}; scrapy crawl -a country_to_scrape=Serbia discoz_spider

runYugo:
	@cd ${WEB_CRAWLER}; scrapy crawl -a country_to_scrape=Yugoslavia discoz_spider