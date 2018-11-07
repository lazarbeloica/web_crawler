import logging
from disscoz_crawler.spiders.utils.error_report import ErrorReport

class ErrorRecorder():

    def __init__(self):
        self._error_reports = []

    def report_possible_error(self, url, component):
        '''
        Brief:      Reports suspitious data parsing value

        Param[in]:  url - Which page was being parsed

        Param[in]: component - What data was being extracted
        '''
        logging.warning("Possible error reported: URL = " + url + "; var = " + component)
        self._error_reports.append(ErrorReport(url, component))

    def get_error_reports(self):
        return self._error_reports
