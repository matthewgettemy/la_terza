
from datetime import datetime, timedelta
from order import Item, Shipping
import time


class Subscription:

    def __init__(self, subscription_json):
        self.order_json = subscription_json
        self.items = {}
        self.shipping = None

        self.customer_id = self.order_json['customer_id']
        self.customer_note = self.order_json['customer_note']
        self.date_completed = self.order_json['date_completed']
        self.date_created = self.order_json['date_created']
        self.date_paid = self.order_json['date_paid']
        self.next_payment_date = self.order_json['next_payment_date']
        self.id = self.order_json['id']
        self.parent_id = self.order_json['parent_id']
        self.number = self.order_json['number']
        self.order_key = self.order_json['order_key']
        self.status = self.order_json['status']
        self.total = self.order_json['total']
        self.transaction_id = self.order_json['transaction_id']

        self.date_ordered = datetime.strptime(self.date_created, '%Y-%m-%dT%H:%M:%S')

    def parse_items(self):
        self.items = {}
        for item_json in self.order_json['line_items']:
            self.items[item_json['id']] = Item(item_json, self.date_ordered, 'subscription')

    def get_shipping_info(self):
        self.shipping = Shipping(self.order_json['shipping'])

