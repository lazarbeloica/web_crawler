from dateutil import parser
import logging


def convert_to_date(date_str):
    dt = parser.parse(date_str)
    logging.debug(dt)
    return dt
