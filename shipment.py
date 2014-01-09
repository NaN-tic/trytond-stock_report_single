# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView
from trytond.pool import Pool, PoolMeta
from trytond.rpc import RPC
from trytond.transaction import Transaction
from trytond.wizard import (Wizard, StateView, StateTransition, StateAction,
    Button)

__all__ = ['PrintShipmentWarning', 'PrintDeliveryNote', 'DeliveryNote']
__metaclass__ = PoolMeta


class PrintShipmentWarning(ModelView):
    '''Print Shipment Report Warning'''
    __name__ = 'stock.shipment.print.warning'


class PrintDeliveryNote(Wizard):
    'Print Delivery Note Report'
    __name__ = 'stock.shipment.out.print'
    start = StateTransition()
    warning = StateView('stock.shipment.print.warning',
        'stock_report_single.print_shipment_warning_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Print', 'print_', 'tryton-print', default=True),
            ])
    print_ = StateAction('stock.report_shipment_out_delivery_note')

    def transition_start(self):
        if len(Transaction().context['active_ids']) > 1:
            return 'warning'
        return 'print_'

    def do_print_(self, action):
        data = {}
        data['id'] = Transaction().context['active_ids'].pop()
        data['ids'] = [data['id']]
        return action, data

    def transition_print_(self):
        if Transaction().context['active_ids']:
            return 'print_'
        return 'end'


class DeliveryNote:
    __name__ = 'stock.shipment.out.delivery_note'

    @classmethod
    def __setup__(cls):
        super(DeliveryNote, cls).__setup__()
        cls.__rpc__['execute'] = RPC(False)

    @classmethod
    def execute(cls, ids, data):
        ShipmentOut = Pool().get('stock.shipment.out')

        res = super(DeliveryNote, cls).execute(ids, data)
        if len(ids) > 1:
            res = (res[0], res[1], True, res[3])
        else:
            shipment = ShipmentOut(ids[0])
            if shipment.code:
                res = (res[0], res[1], res[2], res[3] + ' - ' + shipment.code)
        return res

    @classmethod
    def _get_records(cls, ids, model, data):
        with Transaction().set_context(language=False):
            return super(DeliveryNote, cls)._get_records(ids[:1], model, data)
