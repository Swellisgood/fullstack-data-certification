from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel, validator
from typing import  Union
import joblib
import json
import pandas as pd 

app = FastAPI(
title="Getaround API",
description="""You can use this API to estimate the rental price of a car.
The API is based on a dataset of cars from Getaround.
The dataset contains 10,000 rows and 9 columns.
The columns are:
- `model_key`: the brand of the car (Toyota, BMW, Ford, etc.)
- `mileage`: the mileage of the car (in km)
- `engine_power`: the engine power of the car (in horse power)
- `fuel`: the fuel type of the car (includes diesel, petrol, hybrid, electric)
- `paint_color`: the color of the car
- `car_type`: the type of car (includes sedan, hatchback, suv, van, estate, convertible, coupe, subcompact)
- `private_parking_available`: whether the car has a private parking or not (boolean)
- `has_gps`: whether the car has a GPS or not (boolean)
- `has_air_conditioning`: whether the car has air conditioning or not (boolean)
- `automatic_car`: whether the car is automatic or not (boolean)
- `has_getaround_connect`: whether the car has Getaround Connect or not (boolean)
- `has_speed_regulator`: whether the car has a speed regulator or not (boolean)
- `winter_tires`: whether the car has winter tires or not (boolean)
- `rental_price_per_day`: the rental price of the car (in $)
The API has 6 endpoints:
- **/preview**: returns a preview of the dataset (as a dictionary)
- **/predict**: returns the predicted price of a car
- **/unique-values**: returns the unique values of a column (as a list)
- **/groupby**: returns the grouped data of a column (as a dictionary)
- **/filter-by**: returns the filtered data of a column (as a dictionary)
- **/quantile**: returns the quantile of a column (as a float or string)
The API is based on the FastAPI framework.
"""

)

@app.get("/")
async def root():
    message = """Welcome to the Getaround API. Append /docs to this address to see the documentation for the API on the Pricing dataset."""
    return message



# Defining required input for the prediction endpoint
class Features(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool


# catching errors for all columns except booleans
    @validator('model_key')
    def model_key_must_be_valid(cls, v):
        assert v in ['Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford',
       'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors','Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati',
       'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT','Subaru', 'Toyota', 'Suzuki', 'Yamaha'], \
        f"model_key must be one of the following: ['Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford', \
       'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors','Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati', \
       'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT','Subaru', 'Toyota', 'Suzuki', 'Yamaha']"
        return v

    @validator('fuel')
    def fuel_must_be_valid(cls, v):
        assert v in ['diesel', 'petrol', 'hybrid_petrol', 'electro'], \
        f"fuel must be one of the following: ['diesel', 'petrol', 'hybrid_petrol', 'electro']"
        return v
    
    @validator('paint_color')
    def paint_color_must_be_valid(cls, v):
        assert v in ['black', 'white', 'red', 'silver', 'grey', 'blue', 'orange','beige', 'brown', 'green'], \
        f"paint_color must be one of the following: ['black', 'white', 'red', 'silver', 'grey', 'blue', 'orange','beige', 'brown', 'green']"
        return v
    
    @validator('car_type')
    def car_type_must_be_valid(cls, v):
        assert v in ['sedan', 'hatchback', 'suv', 'van', 'estate', 'convertible', 'coupe', 'subcompact'], \
        f"car_type must be one of the following: ['sedan', 'hatchback', 'suv', 'van', 'estate', 'convertible', 'coupe', 'subcompact']"
        return v

    @validator('mileage')
    def mileage_must_be_positive(cls, v):
        assert v >= 0, f"mileage must be positive"
        return v
    
    @validator('engine_power')
    def engine_power_must_be_positive(cls, v):
        assert v >= 0, f"engine_power must be positive"
        return v

# endpoint to predict the price of a car
@app.post("/predict")
async def predict(features:Features):
    """Get the predicted price of a car. 
Example of input:
{
  "model_key": "Toyota",
  "mileage": 25000,
  "engine_power": 130,
  "fuel": "diesel",
  "paint_color": "red",
  "car_type": "sedan",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": false,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": true
}
Should return : "prediction": 143.557057416081
All entries are case sensitive. List of possible values for categorical columns are available in the /unique-values endpoint.
Wrong values will return a specific error message."""

    features = dict(features)
    input_df = pd.DataFrame(columns=['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires'])
    input_df.loc[0] = list(features.values())
    # Load the model & preprocessor
    model = joblib.load('gbr_model.pkl')
    prep = joblib.load('preprocessor.pkl')
    X = prep.transform(input_df)
    pred = model.predict(X)
    return {"prediction" : pred[0]}


# Endpoints to explore the dataset

@app.get("/preview")
async def preview(rows: int):
    """ Get preview of dataset : Input number of preview rows as integer"""
    data = pd.read_csv('df_pricing.csv')
    preview = data.head(rows)
    return preview.to_dict()

@app.get("/unique-values")
async def get_unique(column: str):
    """ Get unique values by given column : Input name of column (string).
    Example suffix : /unique-values?column=model_key
    N.B.: Attempting to get unique values for the rental_price_per_day or mileage column will return an error."""
    data = pd.read_csv('df_pricing.csv')
    selection = data[column].unique()
    return list(selection)

@app.get("/groupby")
async def groupby_agg(column:str,parameter:str):
    """ Get data grouped by given column : Input parameters are 1) column (string), 2) aggregation parameter (string).
    Example suffix : /groupby?column=model_key&parameter=mean"""
    data = pd.read_csv('df_pricing.csv')
    data_group = data.groupby(column).agg(parameter)
    return data_group.to_dict()

@app.get("/filter-by")
async def get_filtered(column:str,category:str):
    """ Get filtered data for given column : Input parameters are 1) column (string), 2) category (string).
    Example suffix : /filter-by?column=model_key&category=Toyota"""
    data = pd.read_csv('df_pricing.csv')
    filtered = data.loc[data[column] == category]
    return filtered.to_dict()

@app.get("/quantile")
async def get_quantile(column:str,decimal:float):
    """Get quantile for given column : Input parameters are 1) column (string), 2) quantile (float between 0 and 1, ex : 0.2). 
    The interpolation method used when the desired quantile is between 2 data points is 'nearest' for categorical data and 'linear' for numerical data.
    Example suffix : /quantile?column=mileage&decimal=0.75"""
    data = pd.read_csv('df_pricing.csv')
    try:
        data_quantile = data[column].quantile(decimal,interpolation='linear')
    except:
        data_quantile = data[column].quantile(decimal,interpolation='nearest')
    return data_quantile




if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 4000, debug=True, reload=True)