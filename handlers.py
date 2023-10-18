# for HTTP requesthanders ( to map the request to request handlers)
import base64
import json
import urllib.parse

import tornado.web
from vininfo import Vin
import dac
import os

VIN_LENGTH = 17
dac = dac.DAC()

def kwattsHalf(k):
    return '{0:.1f}'.format(k/2)
    
def amperes(k, v):
    return '{0:.2f}'.format(k/v)

def decFormat(n, d):
    fmt = f"{{0:.{d}f}}"
    return fmt.format(n)
    
class GetVINInfo():
    """Handles VIN search for user input
       given VIN and submodel, returns tbl with vehicle information"""
    def __init__(self, vin, submodel):
        self.retmsg = ""
        self.error = False
        try:
            self.EV = Vin(vin)
        except:
            self.error = True
            self.retmsg = "Unknown VIN"
            return
            
        if (submodel == 'All'):
            submodel = '%'

        manufacturer = self.EV.manufacturer
        modelshortname = self.EV.vds[0]
        year = self.EV.years[0]
        self.tbl = dac.vehicleFromVINData(manufacturer, modelshortname, year, submodel)
        self.urls = dac.vehicleUrlFromVINData(manufacturer, modelshortname, year, submodel)
        self.guides = dac.vehicleGuidesFromVINData(manufacturer, modelshortname, year, submodel)
        if (len(self.tbl) == 0):
            self.error = True
            self.retmsg = f"Sorry, no info on this<br>{year} {manufacturer}"

class GetVehicleInfo():
    """Handles MMY search for user input
       given make, model, year and submodel, returns tbl with vehicle information"""
    def __init__(self, make, model, year, submodel):
        self.tbl = dac.vehicleFromMMYData(make, model, year, submodel)
        self.urls = dac.vehicleUrlFromMMYData(make, model, year, submodel)
        self.guides = dac.vehicleGuidesFromMMYData(make, model, year, submodel)

# class GetVINSubModels():
#     def __init__(self, vin):
#         self.EV = Vin(vin)
#         manufacturer = self.EV.manufacturer
#         modelshortname = self.EV.vds[0]
#         year = self.EV.years[0]
#         self.submodelList = dac.submodelListFromVINData(manufacturer, modelshortname, year)

class validateFormHandler(tornado.web.RequestHandler):
    def post(self, *args):
        vin = tornado.escape.json_decode(self.request.body)['vin']
        submodellist = tornado.escape.json_decode(self.request.body)['submodellist']
        if vin == '':
            self.write(json.dumps({'status': 'error', 'object': '#vin', 'errmsg': 'VIN is empty' }))
        else:
            self.write(json.dumps({'status': 'ok', 'object': '#vin', 'errmsg': '' }))
        self.finish()

class getDischargeData():
    def __init__(self):
        dischargetimes = dac.dischargeData()
        darray = []
        for i in range(len(dischargetimes)):
            dd = [r for r in dischargetimes[i]]
            dd = str(dd).replace('[\'','').replace('\']', '')
            darray.append(dd)
        self.data =  json.dumps(darray).replace('"{', '{').replace('}"','}')

class mainRequestHandler(tornado.web.RequestHandler):
    def get(self):
        global eduButtons
        global eduimages
        global eduimagecaptions
        global disposeButtons
        eduButtons = ""
        edudir = tornado.web.StaticFileHandler.get_absolute_path(self.application.settings['static_path'], "Documents/Education")
        files = os.listdir(edudir)
        files = [f for f in files if os.path.isfile(f"{edudir}/{f}")] # only files, no directories
        for f in files:
            docName = os.path.splitext(f)[0]
            docPath =  tornado.web.StaticFileHandler.make_static_url(path=f"Documents/Education/{f}", settings=self.application.settings)
            eduButtons += f"<br><br><button class='edudocbutton' style='width:500px;' onclick='showGuide(\"{docPath}\", \"edudocframe\", \"edudocs-dialog\");'>{docName}</button>"

        eduimages = [tornado.web.StaticFileHandler.make_static_url(path="images/ModelXAccident.png", settings=self.application.settings), 
                     tornado.web.StaticFileHandler.make_static_url(path="images/ModelSAccident.png", settings=self.application.settings)]
        eduimagecaptions = ["2016 Tesla Model X accident in Lake Forest, California, August 2017","2014 Tesla Model S accident in Fort Lauderdale, Florida, May 2018"]

        f = "Emergency Response Guide  Ioniq Electric.pdf"
        disposepath= tornado.web.StaticFileHandler.make_static_url(path=f"Documents/BatteryDisposal/{f}", settings=self.application.settings)
        docName = os.path.splitext(f)[0]
        disposeButtons = f"<br><br><button class='disposebutton' style='width:450px;' onclick='showGuide(\"{disposepath}\", \"disposeframe\", \"dispose-dialog\");'>{docName}</button>"

        discharge = getDischargeData()
        self.render(template_name="index.html", gotData=0, dischargetimes=discharge.data, eduButtons=eduButtons, eduimages=eduimages, eduimagecaptions=eduimagecaptions, disposeButtons=disposeButtons)

    def post(self, *args):
        global eduButtons
        global eduimages
        global eduimagecaptions
        global disposeButtons
        params = dict(urllib.parse.parse_qsl(self.request.body.decode().strip('"')))
        idmode = params["vehicle"]
        if idmode == 'vinbtn':
            if ("vin" not in params):
                self.write({'status': 'vin_error', 'message': 'Please enter a VIN'})
                self.finish()
                return;
            vin = params["vin"]
            submodellist = params["vinsubmodellist"]
            vinInfo = GetVINInfo(vin, submodellist)
            if vinInfo.error:
                self.write({'status': 'vin_error', 'message': vinInfo.retmsg})
                self.finish()
                return
            make = vinInfo.tbl[0][1]
            year = vinInfo.tbl[0][2]
            model = vinInfo.tbl[0][3]
            submodel = vinInfo.tbl[0][5]
        else:
            make = params["makelist"]
            model = params["modellist"]
            year = params["yearlist"]
            submodellist = params["submodellist"]
            if make == '-' or model == '-':
                self.write({'status': 'mmy_error', 'message': 'Please select Make and Model'})
                self.finish()
                return
            vin = ""
            vinInfo = GetVehicleInfo(make, model, year, submodellist)
            submodel = vinInfo.tbl[0][5]

        discharge = getDischargeData()
        ids = [row['ID'] for row in vinInfo.tbl]
        rngs = [row['EVRange_miles'] for row in vinInfo.tbl]
        kWh = [row['kWhRated'] for row in vinInfo.tbl]
        amps = [round(1000.0 * row['kWhRated'] / row['NominalPackVoltage'], 2) for row in vinInfo.tbl]
        chem = [row['chemistry'] for row in vinInfo.tbl]
        submodel = [row['SubModel'] for row in vinInfo.tbl]
        # add kWhRated to function
        maxvolt = [row['MaxPackVoltage'] for row in vinInfo.tbl]
        minvolt = [row['MinPackVoltage'] for row in vinInfo.tbl]
        gotYearRange = False
        years = 0;
        if year == 'All':
            year = ""
            years = [row['yearRange'] for row in vinInfo.tbl]
            gotYearRange = True
        # add voltages to function
        
        imgfigure = 0 if vinInfo.tbl[0]['imgfigure'] == None else base64.b64encode(vinInfo.tbl[0]['imgfigure'])
        imgstructure = 0 if vinInfo.tbl[0]['imgstructure'] == None else base64.b64encode(vinInfo.tbl[0]['imgstructure'])
        imgtransport = 0 if vinInfo.tbl[0]['imgtransport'] == None else base64.b64encode(vinInfo.tbl[0]['imgtransport'])
        urllist = ""
        for i in vinInfo.urls: 
            url = i["value"]
            urlDesc = i["key"]
            urllist += f"<br><a href='{url}' target='_blank'>{urlDesc}</a>"
        guidebuttons = ""
        for i in vinInfo.guides: 
            docName = i["documentName"]
            docPath = i["localPath"]
            guidepath = tornado.web.StaticFileHandler.make_static_url(path=f"Documents/ResponseGuides/{docPath}", settings=self.application.settings)
            guidebuttons += f"<br><br><button class='guidebutton' style='width:450px;' onclick='showGuide(\"{guidepath}\", \"guideframe\", \"guides-dialog\");'>{docName}</button>"
            # guidelist += f"<iframe id='guide-frame' style='width:1200px; height:1000px;' src='{guidepath}'></iframe>"

        pg1 = self.render_string("static/html/page1.html", gotData=1, vin=vin, submodel=submodellist, gotYearRange=gotYearRange, year=year, dbEV=vinInfo.tbl, dbEVLength=len(vinInfo.tbl), ids=ids, rngs=rngs, kWh=kWh, chem=chem, maxvolt=maxvolt, minvolt=minvolt, decFormat=decFormat)
        pg2 = self.render_string("static/html/page2.html", gotData=1, year=year, make=make, model=model, imgfigure=imgfigure, imgstructure=imgstructure, urllist=urllist, guidebuttons=guidebuttons)
        pg3 = self.render_string("static/html/page3.html", gotData=1, dischargetimes=discharge.data, ids=ids, submodel=submodel, gotYearRange=gotYearRange, years=years, kWh=kWh, amps=amps, make=make, model=model, year=year, ) #kwattsHalf=kwattsHalf, amperes=amperes, 
        pg4 = self.render_string("static/html/page4.html", gotData=1, imgtransport=imgtransport)
        pgEducation = self.render_string("static/html/education.html", gotData=1, eduButtons=eduButtons, eduimages=eduimages, eduimagecaptions=eduimagecaptions )
        pgDispose = self.render_string("static/html/recycle.html", gotData=1, disposeButtons=disposeButtons)
        resp = {'status': 'ok', "page1": pg1.decode(), "page2": pg2.decode(), "page3": pg3.decode(), "page4": pg4.decode(), "recycle": pgDispose.decode(), "education": pgEducation.decode()}
        self.write(resp)
        self.finish()
        
class getSubmodelsByVINHandler(tornado.web.RequestHandler):
    def post(self, *args):
        vin = tornado.escape.json_decode(self.request.body)['vin']
        if len(vin) != VIN_LENGTH:
            message = "VIN must be 17 characters in length"
            if len(vin) == 0: message = "Please enter VIN"
            self.write(json.dumps({'status': 'error', 'message': message}))
            self.finish()
            return;

        EV = Vin(vin)
        manufacturer = EV.manufacturer
        modelshortname = EV.vds[0]
        year = EV.years[0]
        submodelList = dac.submodelListFromVINData(manufacturer, modelshortname, year)

        self.write(json.dumps({'status': 'ok', 'numsubmodels': len(submodelList),'submodellist': submodelList}))
        self.finish()

class getMakesHandler(tornado.web.RequestHandler):
    def get(self, *args):
        makelist = dac.makesList()
        self.write(json.dumps({'status': 'ok', 'makelist': makelist}))
        self.finish()

class getModelsHandler(tornado.web.RequestHandler):
    def post(self, *args):
        make = tornado.escape.json_decode(self.request.body)['make']
        modellist = dac.modelsListFromMake(make)
        self.write(json.dumps({'status': 'ok', 'nummodels': len(modellist), 'modellist': modellist}))
        self.finish()

class getYearsHandler(tornado.web.RequestHandler):
    def post(self, *args):
        model = tornado.escape.json_decode(self.request.body)['model']
        make = tornado.escape.json_decode(self.request.body)['make']
        yearlist = dac.yearsListFromMakeModel(make, model)
        self.write(json.dumps({'status': 'ok', 'numyears': len(yearlist), 'yearlist': yearlist}))
        self.finish()

class getSubmodelsHandler(tornado.web.RequestHandler):
    def post(self, *args):
        model = tornado.escape.json_decode(self.request.body)['model']
        make = tornado.escape.json_decode(self.request.body)['make']
        year = tornado.escape.json_decode(self.request.body)['year']
        submodellist = dac.submodelListFromMakeModelYear(make, model, year)
        self.write(json.dumps({'status': 'ok',  'numsubmodels': len(submodellist), 'submodellist': submodellist}))
        self.finish()

