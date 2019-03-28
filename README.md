This application will provide Pollen indexes forecasted in an hourly fashion for the location specified in the flask application as latitude and longitude.
The API is provide by api.breezometer.com

About:
A python flask based web app leveraging on google cloud and kubernetes engine. The app is implements Pollen API lets you request pollen information including types, plants, and indexes for a specific location. The API provides endpoints that let you query. 
1) Current Conditions
2) Daily Forecast

Running the application:
The following fields have to be edited for the need latitude, longitude, start time, end time, api key

How To Install and Run the Project :
Install the Dependencies using pip install -r requirements.txt.

Run the project using python pollen.py.

App can be viewed at http://0.0.0.0:8080/


Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
