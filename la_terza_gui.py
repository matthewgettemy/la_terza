"""Subclass of LaTerzaFrame, which is generated by wxFormBuilder."""

import wx
import json
import pprint
import datetime
import woocommerce
import configparser
import wx.lib.mixins.listctrl as listmix
from requests.exceptions import ReadTimeout


import la_terza_gui_objects
import order
import subscription

class LaTerza(la_terza_gui_objects.LaTerzaFrame, listmix.ColumnSorterMixin):

    def __init__(self, parent):
        la_terza_gui_objects.LaTerzaFrame.__init__(self, parent)
        self.parse_config()
        self.wc_api = woocommerce.API(url=self.config['DEFAULT']['url'],
                                      consumer_key=self.config['DEFAULT']['ck'],
                                      consumer_secret=self.config['DEFAULT']['cs'],
                                      wp_api=True,
                                      version="wc/v3")
        self.wc_subs_api = woocommerce.API(url=self.config['DEFAULT']['url'],
                                           consumer_key=self.config['DEFAULT']['ck'],
                                           consumer_secret=self.config['DEFAULT']['cs'],
                                           wp_api=True,
                                           version="wc/v1")

        self.customer_orders = {}
        self.current_items = None
        self.initialize_order_table()
        listmix.ColumnSorterMixin.__init__(self, self.order_control.GetColumnCount())
        self.SetIcon(wx.Icon("icons/coffee_bag.ico"))

    def GetListCtrl(self):
        return self.order_control

    def parse_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('keys.ini')

    def initialize_order_table(self):
        self.clear_orders()
        self.get_orders()
        self.set_column_headers()
        self.current_items = self.get_all_items()
        self.add_items_to_control(self.current_items)

    def update_order_table(self, event):
        self.clear_orders()
        self.get_orders()
        #self.set_column_headers()
        self.current_items = self.get_all_items()
        self.add_items_to_control(self.current_items)

    def mark_complete(self, event):
        pass

    def mark_order_processing(self, event):
        pass

    def mark_order_complete(self, event):
        row_number = self.order_control.GetFirstSelected()
        order_id = self.order_control.GetItem(row_number, 7).GetText()

        # TODO: thread this
        for i in range(10):
            try:
                a = self.wc_api.put('orders/{}'.format(order_id), {'status': 'complete'})
                break
            except ReadTimeout:
                print(i)
        print(a.json())

        self.clear_orders()
        self.get_orders()
        self.current_items = self.get_all_items()
        self.add_items_to_control(self.current_items)

    def get_orders(self):
        # TODO: Need to handle 100+ orders, this can be tested by using per_page=10
        # TODO: thread this
        for i in range(3):
            try:
                raw_orders = self.wc_api.get('orders', params={'per_page': 100, 'page': 1})
                break
            except ReadTimeout:
                print(i)

        pp = pprint.PrettyPrinter()
        pp.pprint(raw_orders.json()[0])
        f1 = open('raw_data.txt', 'w')
        f1.write(pp.pformat(raw_orders.json()))
        f1.close()
        for order_json in raw_orders.json():
            self.customer_orders[order_json['id']] = order.Order(order_json)
        [self.customer_orders[order_id].parse_items() for order_id in self.customer_orders]
        [self.customer_orders[order_id].get_shipping_info() for order_id in self.customer_orders]

        # TODO: thread this
        for i in range(3):
            try:
                raw_subs = self.wc_subs_api.get("subscriptions", params={'per_page': 100, 'page': 1})
                break
            except ReadTimeout:
                print(i)

        subs = []
        for sub_json in raw_subs.json():
            a = subscription.Subscription(sub_json)
            subs.append(a)
            a.parse_items()

        # Add subscription stuff to order items...this is so janky...
        for sub in subs:
            for item_id in self.customer_orders[sub.parent_id].items:
                order_item_name = self.customer_orders[sub.parent_id].items[item_id].name
                for sub_item_id in sub.items:
                    sub_item_name = sub.items[sub_item_id].name
                    if order_item_name == sub_item_name and sub.status == 'active':
                        self.customer_orders[sub.parent_id].items[item_id].sub = True
                        self.customer_orders[sub.parent_id].items[item_id].date_paid = datetime.datetime.strptime(sub.date_paid, '%Y-%m-%dT%H:%M:%S').date()
                        self.customer_orders[sub.parent_id].items[item_id].next_payment_date = datetime.datetime.strptime(sub.next_payment_date, '%Y-%m-%dT%H:%M:%S').date()

        # update roast dates with subscription roasts
        for order_id in self.customer_orders:
            for item_id in self.customer_orders[order_id].items:
                self.customer_orders[order_id].items[item_id].add_subscription_roast_dates()


    def date_updated(self, event):

        def wx_to_datetime(date):
            if date.IsValid():
                ymd = map(int, date.FormatISODate().split('-'))
                return datetime.date(*ymd)
            else:
                return None

        chosen_date = self.calendar.GetDate()
        chosen_date = wx_to_datetime(chosen_date)
        self.clear_orders()
        self.current_items = self.get_items_due(chosen_date)
        self.add_items_to_control(self.current_items)

    def clear_orders(self):
        self.order_control.DeleteAllItems()

    def get_all_items(self):
        orders_items = {}
        for order_id in self.customer_orders:
            for item_id in self.customer_orders[order_id].items:
                if order_id in orders_items:
                    orders_items[order_id].append(item_id)
                else:
                    orders_items[order_id] = [item_id]
        return orders_items

    def get_items_due(self, date):
        orders_items = {}
        for order_id in self.customer_orders:
            for item_id in self.customer_orders[order_id].items:
                item = self.customer_orders[order_id].items[item_id]
                if date in item.roast_dates:
                    if order_id in orders_items:
                        orders_items[order_id].append(item_id)
                    else:
                        orders_items[order_id] = [item_id]
        return orders_items

    def add_items_to_control(self, orders_items):
        tmp = {}
        # TODO: need to clean up the way this is done, especially with the itemDataMap
        index = 0
        for order_id in orders_items:
            customer_order = self.customer_orders[order_id]
            for item_id in orders_items[order_id]:
                item = customer_order.items[item_id]
                item_id = str(item.id)
                name = str(item.name)
                ordered_date = str(' '.join(customer_order.date_created.split('T')))
                status = str(customer_order.status)
                customer_name = str(customer_order.shipping.first_name.lower() + ' ' + customer_order.shipping.last_name.lower())
                note = str(customer_order.customer_note)
                price = str(item.price)
                order_id = str(customer_order.id)

                tmp[index] = (item_id, name, ordered_date, status, customer_name, note, price, order_id)
                self.order_control.InsertItem(index, item_id)
                self.order_control.SetItem(index, 1, name)
                self.order_control.SetItem(index, 2, ordered_date)
                self.order_control.SetItem(index, 3, status)
                self.order_control.SetItem(index, 4, customer_name)
                self.order_control.SetItem(index, 5, note)
                self.order_control.SetItem(index, 6, price)
                self.order_control.SetItem(index, 7, order_id)
                self.order_control.SetItemData(index, index)
                index += 1
        self.itemDataMap = tmp

    def set_column_headers(self):
        self.order_control.InsertColumn(0, 'item id')
        self.order_control.InsertColumn(1, 'name')
        self.order_control.InsertColumn(2, 'date ordered')
        self.order_control.InsertColumn(3, 'status')
        self.order_control.InsertColumn(4, 'customer')
        self.order_control.InsertColumn(5, 'note')
        self.order_control.InsertColumn(6, 'total')
        self.order_control.InsertColumn(7, 'order id')

        self.order_control.SetColumnWidth(0, 50)
        self.order_control.SetColumnWidth(1, 150)
        self.order_control.SetColumnWidth(2, 150)
        self.order_control.SetColumnWidth(3, 100)
        self.order_control.SetColumnWidth(4, 120)
        self.order_control.SetColumnWidth(5, 50)
        self.order_control.SetColumnWidth(5, 50)
        self.order_control.SetColumnWidth(5, 50)

    def display_raw_order(self, event):
        target_order_id = None
        item_id = int(event.GetText())
        for order_id in self.current_items:
            if item_id in self.current_items[order_id]:
                target_order_id = order_id
        raw_order_frame = la_terza_gui_objects.RawOrderFrame(None)
        order_json = str(self.customer_orders[target_order_id].order_json)
        formatted_order = order_json.replace(',', ',\n')
        raw_order_frame.raw_order_text_control.AppendText(formatted_order)
        raw_order_frame.raw_order_text_control.SetScrollPos(0, 0)

        raw_order_frame.Show()


class LaTerzaGui(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = LaTerza(None)
        self.SetTopWindow(frame)
        frame.Show()
        return 1


if __name__ == "__main__":
    ltg = LaTerzaGui(0)
    ltg.MainLoop()
