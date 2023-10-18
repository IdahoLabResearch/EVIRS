import csv, sqlite3, pandas

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

conn = sqlite3.connect('evis.db')
c = conn.cursor()

c.execute("drop table VehicleInfo")
c.execute("""create table VehicleInfo (
    ID                          integer primary key, 
    Make                        text, 
    Year                        integer, 
    Model                       text, 
    ModelShortName              text, 
    SubModel                    text,
    BodyType                    text,
    FuelType                    text,
    EVRange_miles               integer,
--    CurrentRange_miles          integer,
    kWhRated                    real,
    ModulePackCapacity_Ah       real,
    NominalPackVoltage          integer,
    --Chemistry                   text,
    --FormFactor                  text,
    --NumOfSeriesModules          integer,
    --NumParallelStringsPerModule integer,
    --MaxCellVoltage              real,
    --MinCellVoltage              real,
    --SOC_pct                     real,
    --EnergyStranded_kWh          real,
    --CurrentPackVoltage          real,
    MaxPackVoltage              real,
    MinPackVoltage              real,
    --NominalCellVoltage          real,
    --CellCapacity_Ah             real,
    --MPGeCity                    real,
    --MPGeHighway                 real,
    --MPGeCombined                real,
    --Efficiency_kwhPerMile       real,
    --EfficiencyEst_kwhPerMile    real,
    --BatteryLocation             text
    imgSetID                    integer
    )
    """)

df = pandas.read_csv('database.csv')
df.to_sql("VehicleInfo", conn, if_exists='append', index=False)

c.execute("drop table VehicleImages")
c.execute("""create table VehicleImages (
   imgSetID integer
  ,imgfigure blob
  ,imgstructure blob
  ,imgtransport blob
  )
  """)

dbfigImg = convertToBinaryData("./Tesla_fig.jpg")
dbstrImg = convertToBinaryData("./Tesla_structure.png")
dbtraImg = convertToBinaryData("./Tesla_transport.png")
data_tuple = (1, dbfigImg, dbstrImg, dbtraImg)
insert_blob_cmd = "INSERT INTO VehicleImages (imgSetID, imgfigure, imgstructure, imgtransport) VALUES (?, ?, ?, ?)"
c.execute(insert_blob_cmd, data_tuple)

conn.commit()
c.close()
conn.close()


