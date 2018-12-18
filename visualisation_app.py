from vizualisartion.vizualizer import Vizualizer
from vizualisartion.plotter import Plotter
from common.db.dizcoz_db_driver import DiscozDBDriver

plotter = Plotter()
db = DiscozDBDriver()
vzulizer = Vizualizer(plotter, db)

vzulizer.process_all_diagrams()

