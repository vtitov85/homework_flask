#Flask


from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome to the Hawaii Climate App!<br/>"
        f"-------------------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        
        )

@app.route("/api/v1.0/precipitation/")
def precipitation():
    session = Session(engine)
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > "2010-01-01").\
    order_by(Measurement.date).all()
    prcp_dict = dict(date_prcp)
    print("Precipitation")
    return jsonify(prcp_dict)   

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_names = session.query(Station.station).all()
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs(): 
    # Get the latest date in the database
    date_1 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_1= date_1[0]
    # Calculate the date 1 year ago from the last data point in the database
    date_2= dt.datetime.strptime(date_1,"%Y-%m-%d")-dt.timedelta(days=365)
    #Query temperature data 
    tobs_query=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=date_2).all()
    tobs_list=list(tobs_query)
    #return JSON list 
    return jsonify(tobs_list)
 
@app.route("/api/v1.0/<start>")
def start(start=None):
    
    session = Session(engine)
    #Query for weather data 
    input_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    #Turn data into list
    input_start_list=list(input_start)
    #return JSON list
    return jsonify(input_start_list)

app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    
    session = Session(engine)
    #Query for weather data 
    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date<=end).group_by(Measurement.date).all()
    #Turn data into list
    start_end_list=list(start_end)
    #return JSON list
    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)



