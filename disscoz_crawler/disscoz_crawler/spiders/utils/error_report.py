
class ErrorReport():

    def __init__(self, url, component):
        '''
        Brief:      Stores error raport data

        Param[in]:  url - Which page was being parsed

        Param[in]:  component - What data was being extracted
        '''
        self._url = url
        self._component = component

    def get_url(self):
        return self._url

    def get_component(self):
        return self._component
