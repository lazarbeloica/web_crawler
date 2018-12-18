from vizualisartion.graph_decorator import GraphRegistry
from vizualisartion.plotter import Plotter
from common.db.dizcoz_db_driver import DiscozDBDriver
from vizualisartion import user_graph_decorator


class Vizualizer():
    '''
    Breif: Class used to visualize the data from the db
    '''

    def __init__(self, plotter, db_driver):
        self._plotter = plotter
        self._db = db_driver


    def process_all_diagrams(self):
        self._db._connect()
        for decorator in GraphRegistry.get_available_graphs():
            self._plotter.plot_graph((decorator)(self._db).get_dataframe())

        self._db._disconnect()
