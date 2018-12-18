from vizualisartion.graph_decorator import RegisterDecorator
import pandas as pnd

'''
Brief: In this file are located user-defined graph decoratros
'''

class ExampleDecorator(RegisterDecorator):

    def get_brief(self):
        return 'Example graph decorator 1'

    def get_dataframe(self):
        query = 'select count(*) from '
        return pnd.DataFrame({'a':[1, 1], 'b':[2, 2]})


class ExampleDecorator1(RegisterDecorator):

    def get_brief(self):
        return 'Example graph decorator 1'

    def get_dataframe(self):
        return pnd.DataFrame({'a':[1, 1], 'b':[2, 2]})
