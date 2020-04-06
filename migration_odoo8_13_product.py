__author__ = 'alan'

# encoding=utf8

import xmlrpclib
import datetime
import ssl
import sys
reload(sys)
user = ''
pwd = ''
bd = ''
bd2 = ''




##DECLARACION DE ID DE IVA, PRIMER VALOR ES EL ID QUE TIENE
##EN ODOO "A" Y SEGUNDO VALOR ID QUE TIENE EN ODOO "B"
##TANTO EL VALOR IVA21 VENTA E IVA COMPRA 21 SE ESTABLECERAN POR DEFECTO EN CASO DE NO EXISTIR NINGUN VALOR EN EL ODOO "A"

impuest ={
    #IVA 21 V
    False:19,
    1 : 19,
    #IVA 21 C
    False: 20,
    2 : 20,
    #IVA 10 V
    3 : 17,
    #IVA 10 C
    4 : 18,
    #IVA 0 V
    5:15,
    #IVA 0 C
    6:16,
    #IVA 27 V
    8:21,
    #IVA 27 C
    7:22,
}

user13 = ''
pwd13 = ''
user8=''
pwd8=''
bd13 = ''
bd8 = ''

url_odoo8 = ""
url_odoo13 = ""
common13 = xmlrpclib.ServerProxy(url_odoo13)
models13 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_odoo13))
common8 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url_odoo8),
                                ssl._https_verify_certificates(False))
models8 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_odoo8),
                                ssl._https_verify_certificates(False))

class Migration_Odoo8_13_Product:

    def __init__(self):
        args = [('&'), ('name', 'like', ''), ('active', '=', 'True')]
        ids = models8.execute(bd8, self.uid, pwd8, 'product.template', 'search', args)
        fields = ['id', 'name','sale_ok', 'purchase_ok', 'hr_expense_ok', 'type', 'default_code', 'description',
                  'standard_price', 'list_price', 'image_medium', 'taxes_id', 'supplier_taxes_id', 'seller_ids']
        data = models8.execute(bd8, self.uid, pwd8, 'product.template', 'read', ids, fields)
        x=0
        for item_product in data:
            x += 1
            print ("Productos cargados: ", x, "de", len(data))
            self.create_product(item_product)

    def create_product(self, product):

        if not self.product_already_load(product['id']):
            try:
                id = models13.execute_kw(bd13, 2, pwd13, 'product.product', 'create', [{
                    'name': product['name'],
                    'purchase_ok': product['purchase_ok'],
                    'sale_ok': product['sale_ok'],
                    'can_be_expensed': product['hr_expense_ok'],
                    'type': product['type'],
                    'default_code': product['default_code'],
                    'description': product['description'],
                    'standard_price': product['standard_price'],
                    'list_price': product['list_price'],
                    'image_1920': product['image_medium'],
                    'taxes_id': [impuest[product['taxes_id'][0]]],
                    'supplier_taxes_id': [int(impuest[product['supplier_taxes_id'][0]])],
                    'seller_ids': [],
                    'barcode': product['id'],
                }])

                if len(product['taxes_id']) > 1:
                    self.update_taxes_prd(product['taxes_id'],product['supplier_taxes_id'], product, id)
            except:
                print ("SE AH PRODUCIDO UN ERROR EN EL PRODUCTO:", product['id'])


    def update_taxes_prd(self,txes_ids,txes_suppl_ids, prd,id):
        tx_ids =[]
        tx_supp_ids =[]
        for item in txes_ids:
            tx_ids.append(impuest[item])
        for item in txes_suppl_ids:
            tx_supp_ids.append(impuest[item])
        txes_ids.clear()
        txes_suppl_ids.clear()
        models13.execute_kw(bd13, 2, pwd13, 'product.template', 'write', [[id], {
            'taxes_id': [[6, 0,tx_ids]],
            'supplier_taxes_id': [[6, 0,tx_supp_ids]],
        }])

    def product_already_load(self,barcode):
        ids = models13.execute_kw(bd13, 2, pwd,
                                'product.template', 'search',
                                [[['barcode', '=', int(barcode)]]])
        if len(ids) != 0:
            return True


Migration_Odoo8_13_Product()
