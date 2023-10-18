# for HTTP requesthanders ( to map the request to request handlers)
import tornado.web

# imprting the main event loop
import tornado.ioloop

#import cv2
#from matplotlib import pyplot as plt
import os
import numpy as np
import itertools
import json
import random
from vininfo import Vin
import pandas as pd
import pyodbc

# 5YJ3GDEF2LFR00942, 220, 330, 322
# JN1AZ0CP7CT024420 (Nissan)
# 5YJ3GDEF2LFR00942
# 5YJYGDEE3MF071288

class GetVINInfo():
    def __init__(self, vin, range):
        self.EV = Vin(vin)
        # self.dbEV = GetVehicleInfo(self.EV.manufacturer, self.EV.vds[0], self.EV.years[0],range)
        con = pyodbc.connect("Driver={SQL Server};Server=AVTPROC.inl.gov,1433;Database=EVISWeb;Trusted_Connection=Yes;", autocommit = True)
        cur = con.cursor()
        cur.execute("select * from VehicleInfo where make = ? and modelshortname = ? and year = ? and EVRange_miles = ?", (self.EV.manufacturer, self.EV.vds[0], self.EV.years[0], range))
        self.dbEV = cur.fetchall()
        cur.close()
        con.close()

class GetVehicleInfo():
    def __init__(self, make, model, year, range):
        con = pyodbc.connect("Driver={SQL Server};Server=AVTPROC.inl.gov,1433;Database=EVISWeb;Trusted_Connection=Yes;", autocommit = True)
        cur = con.cursor()
        cur.execute("select * from VehicleInfo where make = ? and modelshortname = ? and year = ? and EVRange_miles = ?", (make, model, year, range))
        self.dbEV = cur.fetchall()
        cur.close()
        con.close()

class GetVINRanges():
    def __init__(self, vin):
        con = pyodbc.connect("Driver={SQL Server};Server=AVTPROC.inl.gov,1433;Database=EVISWeb;Trusted_Connection=Yes;", autocommit = True)
        cur = con.cursor()
        self.EV = Vin(vin)
        cur.execute("select EVRange_miles from VehicleInfo where make = ? and modelshortname = ? and year = ?", (self.EV.manufacturer, self.EV.vds[0], self.EV.years[0]))
        self.db = cur.fetchall()
        cur.close()
        con.close()

class tabbedRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("indextabbed.html", gotData=0)

    def post(self):
        vin = self.get_argument("vin")
        range = self.get_argument("vinrange")
        # if ((len(vin) == 0) or (range(vin) == 0)):
        #     print("error")
        #     pass
        # else:
        vinInfo = GetVINInfo(vin, range)
        dbEV = vinInfo.dbEV[0]
        self.render("indextabbed.html", gotData=1, vin=vin, range=range, vinInfo=vinInfo, dbEV=dbEV)

class checkVinRequestHandler(tornado.web.RequestHandler):
    def post(self, *args):
        vin = tornado.escape.json_decode(self.request.body)['vin']
        ranges = GetVINRanges(vin)
        # convert pyodbc row to list
        rangelist = [elem[0] for elem in ranges.db]
        self.write(json.dumps({'status': 'ok', 'rangelist': rangelist}))
        self.finish()

def validateForm(request):
    return "OK";

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", tabbedRequestHandler),
        (r"(/check_vin)$", checkVinRequestHandler)
    ])

    port = 8882
    app.listen(port)
    print(f"Web service is ready and listening on port {port}")

    # to start the server on the current thread
    tornado.ioloop.IOLoop.current().start()
