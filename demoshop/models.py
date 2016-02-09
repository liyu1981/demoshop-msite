import urllib2
import xmltodict
from django.db.models.base import ModelBase

def formatEntries(entries):
    results = []
    for entry in entries:
        newentry = {}
        for key in entry:
            # remove 'g:'
            newentry[key[2:]] = entry[key]
        results.append(newentry)
    return results

def getCategoryFromTitle(title):
    return title.split()[-1]

def getAllProducts():
    print 'init all products ...'
    resp = urllib2.urlopen(
        'http://104.236.187.180/magento/fbdpafeed.xml'
    )
    c = resp.read()
    resp.close()
    xmldoc = xmltodict.parse(c)
    print 'done'
    return formatEntries(xmldoc['feed']['entry'])

def getAllCategories(products):
    print 'start collecting all categories ...'
    c = {}
    for product in products:
        c[getCategoryFromTitle(product['title'])] = True
    print 'done'
    return ['ALL'] + c.keys()


class Shop(ModelBase):
    _products = None
    _categories = None
    _current_category = 'ALL'
    _cart = []

    @classmethod
    def getProducts(cls):
        if cls._products == None:
            cls._products = getAllProducts()
        return cls._products

    @classmethod
    def getCategories(cls):
        if cls._categories == None:
            cls._categories = getAllCategories(cls.getProducts())
        return cls._categories
