# FastAPi_Project
to run the application run the command - 
uvicorn main:app --reload

to make a post request send this api call - 
curl -X POST "http://127.0.0.1:8000/addresses/" -H "accept: application/json" -H "Content-Type: application/json" -d '{"latitude": 40.7128, "longitude": -74.0060, "description": "New York City"}'

to make a get request send this API call -
curl -X GET "http://127.0.0.1:8000/addresses/?latitude=34.0522&longitude=-118.2437&distance=500" -H "accept: application/json"

to make a update request send this API call - 
curl -X PUT "http://127.0.0.1:8000/addresses/1" -H "accept: application/json" -H "Content-Type: application/json" -d '{"latitude": 34.0522, "longitude": -118.2437, "description": "Los Angeles"}'

to make a delete request send this API call -
curl -X DELETE "http://127.0.0.1:8000/addresses/1" -H "accept: application/json"

