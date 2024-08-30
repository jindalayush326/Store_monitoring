# Store_Monitoring System
Loop oversees numerous restaurants across the US and needs to ensure that each location remains online during its operational hours. Occasionally, some restaurants may go offline for a period due to unforeseen issues. Restaurant owners need to receive reports detailing how often this has occurred historically.

# This system offers two key APIs:

/trigger_report Endpoint:

This endpoint initiates the process of generating a report based on the data stored in the database. It does not require any input and returns a unique report ID (a randomly generated string). This ID can be used to check the progress of the report generation.
/get_report Endpoint:

This endpoint is used to check the status of the report or to retrieve the final CSV file. It takes the report ID as input and returns:
"Running" if the report is still being generated.
"Complete" if the report is finished, along with the CSV file containing the following columns: store_id, uptime_last_hour (in minutes), uptime_last_day (in hours), uptime_last_week (in hours), downtime_last_hour (in minutes), downtime_last_day (in hours), and downtime_last_week (in hours).
The uptime and downtime figures in the CSV file reflect only the periods during business hours. The system estimates the uptime and downtime based on the periodic data it receives.
Data Sources
The system utilizes the following three data sources:

# Store Status Data:

A CSV file containing columns for store_id, timestamp_utc, and status (either active or inactive). All timestamps are recorded in UTC.
Business Hours Data:

A CSV file detailing the business hours for each store, with the following schema: store_id, dayOfWeek (0=Monday, 6=Sunday), start_time_local, and end_time_local. These times are in the store's local time zone. If business hours data is missing for a store, it is assumed to be open 24/7.
Timezone Data:

A CSV file listing the time zone for each store with columns store_id and timezone_str. If the timezone information is missing, it defaults to America/Chicago. This ensures that the store status and business hours can be accurately compared.
Note: The data files cannot be uploaded due to LFS (Large File Storage) issues.

# Directory Structure
kotlin
data/
├── business_hours.csv
├── stores.csv
└── timezones.csv

# System Requirements
The data sources are dynamic, meaning the system should not rely on precomputed answers. It must update the data on an hourly basis.
The system should store the CSV data in a suitable database and provide API endpoints to retrieve this information.
Installation
To install the necessary packages, navigate to the project directory and run:

bash
pip install -r requirements.txt
Usage
To start the server, use the following command in the project directory:

bash
python run.py
The server will run on http://localhost:5000. Make sure to include the URL prefix in API calls, for example: http://localhost:5000/api.

API Documentation
/trigger_report
This endpoint initiates the report generation process using the data stored in the database.

Request:

http
POST /api/trigger_report HTTP/1.1
Response:

json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "message": "Success", 
    "error_code": 200,
    "report_id": "random_string"
}
/get_report
This endpoint checks the status of the report or provides the generated CSV file.

Request:

http
GET /api/get_report?report_id=random_string HTTP/1.1
Response:

csv
HTTP/1.1 200 OK
Content-Type: text/csv

store_id, uptime_last_hour(in minutes), uptime_last_day(in hours), uptime_last_week(in hours), downtime_last_hour(in minutes), downtime_last_day(in hours), downtime_last_week(in hours)
1, 60, ...
