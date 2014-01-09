# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .shipment import *


def register():
    Pool.register(
        PrintShipmentWarning,
        module='stock_report_single', type_='model')
    Pool.register(
        PrintDeliveryNote,
        module='stock_report_single', type_='wizard')
    Pool.register(
        DeliveryNote,
        module='stock_report_single', type_='report')
