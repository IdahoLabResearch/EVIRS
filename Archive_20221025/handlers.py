# for HTTP requesthanders ( to map the request to request handlers)
import tornado.web
from vininfo import Vin
import json
import sqlite3
import base64

conn = sqlite3.connect('evis.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

class GetVINInfo():
    def __init__(self, vin, submodel):
        self.EV = Vin(vin)
        if (submodel == 'All'):
            submodel = '%'
        qry = """
            select v.*, i.*
              from VehicleInfo v
              left join VehicleImages i
                on i.imgSetID = v.imgSetID
             where make = ? 
               and modelshortname = ? 
               and year = ? 
               and SubModel like ?"""
        c.execute(qry, (self.EV.manufacturer, self.EV.vds[0], self.EV.years[0], submodel))
        self.tbl = c.fetchall()

class GetVehicleInfo():
    def __init__(self, make, model, year, submodel):
        if (submodel == 'All'):
            submodel = '%'
        qry = """
            select v.*, i.*
            from VehicleInfo v
            left join VehicleImages i
            on i.imgSetID = v.imgSetID
            where make = ? 
            and model = ? 
            and year = ? 
            and SubModel like ?"""

        c.execute(qry, (make, model, year, submodel))
        self.tbl = c.fetchall()

class GetVINSubModels():
    def __init__(self, vin):
        self.EV = Vin(vin)
        c.execute('select EVRange_miles, SubModel from VehicleInfo where make = ? and modelshortname = ? and year = ?', (self.EV.manufacturer, self.EV.vds[0], self.EV.years[0]))
        self.tbl = c.fetchall()
        self.i = 1

class validateFormHandler(tornado.web.RequestHandler):
    def post(self, *args):
        vin = tornado.escape.json_decode(self.request.body)['vin']
        submodellist = tornado.escape.json_decode(self.request.body)['submodellist']
        if vin == '':
            self.write(json.dumps({'status': 'error', 'object': '#vin', 'errmsg': 'VIN is empty' }))
        else:
            self.write(json.dumps({'status': 'ok', 'object': '#vin', 'errmsg': '' }))
        self.finish()


class tabbedRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("indextabbed.html", gotData=0)

    def post(self, *args):
        # idmode = self.get_argument("vehicle")
        idmode = tornado.escape.json_decode(self.request.body)['vehicle']
        if idmode == 'vinbtn':
            vin = tornado.escape.json_decode(self.request.body)['vin']
            submodellist = tornado.escape.json_decode(self.request.body)['submodellist']
            # vin = self.get_argument("vin")
            # submodel = self.get_argument("vinsubmodellist")
            # if vin == '':
            #     self.write(json.dumps({'status': 'error', 'errmsg': 'VIN is blank'}))
            #     return;
            vinInfo = GetVINInfo(vin, submodellist)
        else:
            make = self.get_argument("makelist")
            model = self.get_argument("modellist")
            year = self.get_argument("yearlist")
            submodellist = self.get_argument("submodellist")
            vin = ""
            vinInfo = GetVehicleInfo(make, model, year, submodellist)
        ids = [row['ID'] for row in vinInfo.tbl]
        rngs = [row['EVRange_miles'] for row in vinInfo.tbl]
        kWh = [row['kWhRated'] for row in vinInfo.tbl]
        # add kWhRated to function
        maxvolt = [row['MaxPackVoltage'] for row in vinInfo.tbl]
        minvolt = [row['MinPackVoltage'] for row in vinInfo.tbl]
        # add voltages to function
        imgfigure=base64.b64encode(vinInfo.tbl[0]['imgfigure'])
        imgstructure=base64.b64encode(vinInfo.tbl[0]['imgstructure'])
        imgtransport=base64.b64encode(vinInfo.tbl[0]['imgtransport'])
        #imgfig=base64.b64encode(imgfig)
        #imgfig = imgfig.encode('hex')
        # self.render("indextabbed.html", gotData=0)
        self.render("indextabbed.html", gotData=1, vin=vin, submodel=submodellist, dbEV=vinInfo.tbl, ids=ids, rngs=rngs, kWh=kWh, maxvolt=maxvolt, minvolt=minvolt, imgfigure=imgfigure, imgstructure=imgstructure, imgtransport=imgtransport)
        
class getSubmodelsByVINHandler(tornado.web.RequestHandler):
    def post(self, *args):
        vin = tornado.escape.json_decode(self.request.body)['vin']
        vinDBData = GetVINSubModels(vin)
        # convert database row to list
        submodellist = [row['SubModel'] for row in vinDBData.tbl]
        self.write(json.dumps({'status': 'ok', 'submodellist': submodellist}))
        self.finish()

class getMakesHandler(tornado.web.RequestHandler):
    def get(self, *args):
        c.execute('select distinct Make from VehicleInfo')
        tbl = c.fetchall()
        makelist = [row['Make'] for row in tbl]
        self.write(json.dumps({'status': 'ok', 'makelist': makelist}))
        self.finish()

class getModelsHandler(tornado.web.RequestHandler):
    def post(self, *args):
        make = tornado.escape.json_decode(self.request.body)['make']
        c.execute('select distinct Model from VehicleInfo where Make = ?', (make,))
        tbl = c.fetchall()
        modellist = [row['Model'] for row in tbl]
        self.write(json.dumps({'status': 'ok', 'modellist': modellist}))
        self.finish()

class getYearsHandler(tornado.web.RequestHandler):
    def post(self, *args):
        model = tornado.escape.json_decode(self.request.body)['model']
        make = tornado.escape.json_decode(self.request.body)['make']
        c.execute('select distinct Year from VehicleInfo where Make = ? and Model = ?', (make, model))
        tbl = c.fetchall()
        yearlist = [row['Year'] for row in tbl]
        self.write(json.dumps({'status': 'ok', 'yearlist': yearlist}))
        self.finish()

class getSubmodelsHandler(tornado.web.RequestHandler):
    def post(self, *args):
        model = tornado.escape.json_decode(self.request.body)['model']
        make = tornado.escape.json_decode(self.request.body)['make']
        year = tornado.escape.json_decode(self.request.body)['year']
        c.execute('select distinct SubModel from VehicleInfo where Make = ? and Model = ? and Year = ?', (make, model, year))
        tbl = c.fetchall()
        submodellist = [row['SubModel'] for row in tbl]
        self.write(json.dumps({'status': 'ok', 'submodellist': submodellist}))
        self.finish()

