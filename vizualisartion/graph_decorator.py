from abc import ABC, abstractmethod

class GraphRegistry(type):
    '''
    Brief: Utility class to keep track of Graph Decorators
            that could be created in the system
    '''


    graph_registry = []


    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if name != 'RegisterDecorator':
            GraphRegistry.graph_registry.append(cls)
        return cls


    @staticmethod
    def get_available_graphs():
        '''
        Brief: Returns a list of graphs that can be plottet
        '''

        return GraphRegistry.graph_registry


class GraphDecorator():

    def __init__(self, db_driver):
        self.db = db_driver


    @abstractmethod
    def get_brief(self):
        '''
        Brief: A short description of the graph that
             the class plotts

        Returns: String containing the graph description
        '''
        pass


    @abstractmethod
    def get_dataframe(self):
        '''
        Brief: Method called to run processing on a
                particular decorator

        Returns: DataFrame with the date to be plotted
        '''
        pass


class RegisterDecorator(GraphDecorator, metaclass=GraphRegistry):
    '''
    Brief: Class to inherit when implementing a user-defined
            graph decorator
    '''
    pass
