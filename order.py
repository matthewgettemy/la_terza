
from datetime import datetime, timedelta
import time


class Order:

    def __init__(self, order_json):
        self.order_json = order_json
        self.items = {}
        self.shipping = None

        self.customer_id = self.order_json['customer_id']
        self.customer_note = self.order_json['customer_note']
        self.date_completed = self.order_json['date_completed']
        self.date_created = self.order_json['date_created']
        self.date_paid = self.order_json['date_paid']
        self.id = self.order_json['id']
        self.number = self.order_json['number']
        self.order_key = self.order_json['order_key']
        self.status = self.order_json['status']
        self.total = self.order_json['total']
        self.transaction_id = self.order_json['transaction_id']

        self.date_ordered = datetime.strptime(self.date_created, '%Y-%m-%dT%H:%M:%S')
        print(self.id)

    def parse_items(self):
        self.items = {}
        for item_json in self.order_json['line_items']:
            self.items[item_json['id']] = Item(item_json, self.date_ordered)

    def get_shipping_info(self):
        self.shipping = Shipping(self.order_json['shipping'])


class Item:

    def __init__(self, item_json, date_ordered):
        self.item_json = item_json
        self.date_ordered = date_ordered.date()

        self.id = self.item_json['id']
        self.meta_data = self.item_json['meta_data']
        self.name = self.item_json['name']
        self.price = self.item_json['price']
        self.product_id = self.item_json['product_id']
        self.quantity = self.item_json['quantity']
        self.sku = self.item_json['sku']
        self.subtotal = self.item_json['subtotal']
        self.subtotal_tax = self.item_json['subtotal_tax']
        self.tax_class = self.item_json['tax_class']
        self.taxes = self.item_json['taxes']
        self.total = self.item_json['total']
        self.total_tax = self.item_json['total_tax']
        self.variation_id = self.item_json['variation_id']

        self.recurring = False
        self.frequency = None
        self.roast_dates = []
        self.get_frequency()

    def get_frequency(self):
        if self.name.lower().startswith('bi-weekly'):
            self.frequency = timedelta(weeks=2)
            self.recurring = True
        elif self.name.lower().startswith('monthly'):
            self.frequency = timedelta(weeks=4)
            self.recurring = True
        else:
            if self.date_ordered.weekday() == 4:
                offset = 3
            elif self.date_ordered.weekday() == 5:
                offset = 2
            else:
                offset = 1
            self.roast_dates.append(self.date_ordered + timedelta(days=offset))

        if self.recurring:
            self.calculate_recurring_roasts()

        print(self.id, self.name, self.date_ordered, self.roast_dates)

    def calculate_recurring_roasts(self, number_roasts=1000):

        tmp_roast_date = self.date_ordered
        for i in range(number_roasts):
            if tmp_roast_date.weekday() == 5:
                tmp_roast_date - timedelta(days=1)
            elif tmp_roast_date.weekday() == 6:
                tmp_roast_date + timedelta(days=1)
            self.roast_dates.append(tmp_roast_date)
            tmp_roast_date += self.frequency


class Shipping:

    def __init__(self, shipping_json):
        self.shipping_json = shipping_json

        self.address_1 = self.shipping_json['address_1']
        self.address_2 = self.shipping_json['address_2']
        self.city = self.shipping_json['city']
        self.company = self.shipping_json['company']
        self.country = self.shipping_json['country']
        self.first_name = self.shipping_json['first_name']
        self.last_name = self.shipping_json['last_name']
        self.postcode = self.shipping_json['postcode']
        self.state = self.shipping_json['state']
