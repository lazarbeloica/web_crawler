from vizualisartion.plotter import Plotter
from vizualisartion.graph_decorator import GraphDecorator, GraphRegistry
from vizualisartion import user_graph_decorator
import logging
import unittest
import pandas as pnd
import time

class TestPlotter(unittest.TestCase):

    def test_basic_plot(self):
        plotter = Plotter()
        data = pnd.DataFrame({'a':[1, 1], 'b':[2, 2]})
        plotter.plot_graph(data)


    def test_graph_decorator(self):
        for decorator in GraphRegistry.get_available_graphs():
            print(decorator)

        tmp = (GraphRegistry.get_available_graphs()[0])(None)
        print(tmp)
        print(tmp.get_dataframe())
