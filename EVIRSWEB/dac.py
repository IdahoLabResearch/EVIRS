import sqlite3


vinqry = """
    select ID, Make, Year, Model, ModelShortName, SubModel, BodyType, 
           FuelType, EVRange_miles, kWhRated, ModulePackCapacity_Ah, 
           NominalPackVoltage, MaxPackVoltage, MinPackVoltage, chemistry,
           i.imgSetID, i.imgfigure, i.imgstructure, i.imgtransport
    from v_VehicleInfo v
    left join VehicleImages i
    on i.imgSetID = v.imgSetID
    where make = ? 
    and modelshortname = ? 
    and year = ? 
    and SubModel like ?
    order by EVRange_miles"""

vinUrlqry = """
	select distinct i.imgSetID, j.key, j.value
	from v_VehicleInfo v
	inner join VehicleImages i
	on i.imgSetID = v.imgSetID
	inner join json_each(urlStructure) j
    where make = ?
    and modelshortname = ?
    and year = ?
    and SubModel like ?"""

vinGuidesqry = """
    select distinct r.guideID, r.documentName, r.localPath
    from VehicleResponseGuides r
    inner join VehicleGuideIndex i
    on r.guideID = i.guideID
    inner join v_VehicleInfo v
    on v.ID = i.VehicleID
    where v.make = ?
    and v.modelshortname = ?
    and v.year = ?
    and v.SubModel like ?"""

mmyqry = """
    select ID, Make, Year, Model, ModelShortName, SubModel, BodyType, 
           FuelType, EVRange_miles, kWhRated, ModulePackCapacity_Ah, 
           NominalPackVoltage, MaxPackVoltage, MinPackVoltage, chemistry,
           i.imgSetID, i.imgfigure, i.imgstructure, i.imgtransport
    from v_VehicleInfo v
    left join VehicleImages i
    on i.imgSetID = v.imgSetID
    where make = ? 
    and model = ? 
    and year = ? 
    and SubModel like ?
    order by EVRange_miles"""

mmyUrlqry = """
	select distinct i.imgSetID, j.key, j.value
	from v_VehicleInfo v
	inner join VehicleImages i
	on i.imgSetID = v.imgSetID
	inner join json_each(urlStructure) j
    where make = ?
    and model = ?
    and year = ?
    and SubModel like ?"""

mmyGuidesqry = """
    select distinct r.guideID, r.documentName, r.localPath
    from VehicleResponseGuides r
    inner join VehicleGuideIndex i
    on r.guideID = i.guideID
    inner join v_VehicleInfo v
    on v.ID = i.VehicleID
    where v.make = ?
    and v.model = ?
    and v.year = ?
    and v.SubModel like ?"""

mmqry = """
	select min(ID) ID, min(Year) || '-' || Max(Year) yearRange, Make, Model, 0 Year, ModelShortName, SubModel, BodyType, FuelType, chemistry,
           null imgfigure, null imgstructure, null imgtransport,
		   avg(EVRange_miles) EVRange_miles, avg(kWhRated) kWhRated, avg(ModulePackCapacity_Ah) ModulePackCapacity_Ah, 
		   avg(NominalPackVoltage) NominalPackVoltage, avg(MaxPackVoltage) MaxPackVoltage, avg(MinPackVoltage) MinPackVoltage
    from v_VehicleInfo v
    where make = ?
    and model = ?
	group by  Make, Model, ModelShortName, SubModel, BodyType, FuelType, chemistry
    order by SubModel"""

mmUrlqry = """
	select distinct i.imgSetID, j.key, j.value
	from v_VehicleInfo v
	inner join VehicleImages i
	on i.imgSetID = v.imgSetID
	inner join json_each(urlStructure) j
    where make = ?
    and model = ?"""

mmGuidesqry = """
    select distinct r.guideID, r.documentName, r.localPath
    from VehicleResponseGuides r
    inner join VehicleGuideIndex i
    on r.guideID = i.guideID
    inner join v_VehicleInfo v
    on v.ID = i.VehicleID
    where v.make = ?
    and v.model = ?"""

vinsubmodelsqry = 'select EVRange_miles, SubModel from v_VehicleInfo where make = ? and modelshortname = ? and year = ?'
makesqry = 'select distinct Make from v_VehicleInfo'
modelsqry = 'select distinct Model from v_VehicleInfo where Make = ?'
yearsqry = 'select distinct Year from v_VehicleInfo where Make = ? and Model = ?'
mmysubmodelqry = 'select distinct SubModel from v_VehicleInfo where Make = ? and Model = ? and Year = ?'

dischargeqry = """
    select 
        json_object('EV', make||' '||model, 'discharge1hr_kw', discharge1hr_kw, 'discharge30min_kw', discharge30min_kw, 'discharge10min_kw', discharge10min_kw)
    from v_DischargeTime"""


conn = sqlite3.connect('evis.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


class DAC:
    def dischargeData(self):
        c.execute(dischargeqry)
        return c.fetchall()

    def vehicleFromVINData(self, manufacturer, modelshortname, year, submodel):
        c.execute(vinqry, (manufacturer, modelshortname, year, submodel))
        return c.fetchall()

    def vehicleUrlFromVINData(self, manufacturer, modelshortname, year, submodel):
        c.execute(vinUrlqry, (manufacturer, modelshortname, year, submodel))
        return c.fetchall()

    def vehicleGuidesFromVINData(self, manufacturer, modelshortname, year, submodel):
        c.execute(vinGuidesqry, (manufacturer, modelshortname, year, submodel))
        return c.fetchall()

    def vehicleFromMMYData(self, make, model, year, submodel):
        # disregard vehicle year and return average values for all submodels available for vehicle make and model
        if year == 'All':
            c.execute(mmqry, (make, model))
            return c.fetchall()
        # return values for vehicles - if mutltiple submodels available, return them all
        else:
            if (submodel == 'All'):
                submodel = '%'
            c.execute(mmyqry, (make, model, year, submodel))
            return c.fetchall()

    def vehicleUrlFromMMYData(self, make, model, year, submodel):
        if (year == 'All'):
            c.execute(mmUrlqry, (make, model))
            return c.fetchall()
        else:
            if (submodel == 'All'):
                submodel = '%'
            c.execute(mmyUrlqry, (make, model, year, submodel))
            return c.fetchall()

    def vehicleGuidesFromMMYData(self, make, model, year, submodel):
        if (year == 'All'):
            c.execute(mmGuidesqry, (make, model))
            return c.fetchall()
        else:
            if (submodel == 'All'):
                submodel = '%'
            c.execute(mmyGuidesqry, (make, model, year, submodel))
            return c.fetchall()

    def submodelListFromVINData(self, manufacturer, modelshortname, year):
        c.execute(vinsubmodelsqry, (manufacturer, modelshortname, year))
        tbl = c.fetchall()
        return [row['SubModel'] for row in tbl]

    def makesList(self):
        c.execute(makesqry)
        tbl = c.fetchall()
        return [row['Make'] for row in tbl]

    def modelsListFromMake(self, make):
        c.execute(modelsqry, (make,))
        tbl = c.fetchall()
        return [row['Model'] for row in tbl]

    def yearsListFromMakeModel(self, make, model):
        c.execute(yearsqry, (make, model))
        tbl = c.fetchall()
        return [row['Year'] for row in tbl]

    def submodelListFromMakeModelYear(self, make, model, year):
        c.execute(mmysubmodelqry, (make, model, year))
        tbl = c.fetchall()
        return [row['SubModel'] for row in tbl]

