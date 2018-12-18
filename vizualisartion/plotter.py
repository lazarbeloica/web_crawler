import seaborn
import matplotlib.pyplot

class Plotter():
    '''
    Brief: Class used to plot the graphs
    '''

    def __init__(self):
        self.reset_graph()

    def plot_graph(self, data):
        '''
        Param [in]: X axsis tag

        Param [in]: Y axis tag

        Param [in]: data to plot
        '''
        pass
        self._graph.set(style="whitegrid")
        ax = self._graph.barplot(data=data)
        matplotlib.pyplot.show()

    def reset_graph(self):
        '''
        Brief: resets the current graph
        '''
        self._graph = seaborn
