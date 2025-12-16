
# Setup

## 1. Installation

Clone this repo locally and `cd` into the root of the repo:

```bash
git clone https://github.com/connordelacruz/restaurant-hours-exercise.git
cd restaurant-hours-exercise
```

Create a new virtual python environment and activate it:

```bash
python -m venv venv
. venv/bin/activate
```

Install the package and its dependencies:

```bash
pip install -e .
```

## 2. Initialize Database

Run the following command to initialize and populate the database:

```bash
flask --app restaurant_hours init-db
```

## 3. Start the Server

To start the server, you can either start the Flask server manually:

```bash
flask --app restaurant_hours run --debug
```

Or have python run the package's main module:

```bash
python -m restaurant_hours
```

Both of these example commands should run the server at http://127.0.0.1:5000 

# Using the API

_Note: examples are assuming the server is running on the default URL of http://127.0.0.1:5000_

**Usage:**

```
http://127.0.0.1:5000/<timestamp>
```

The API has a single endpoint at the root. It takes a single parameter, a timestamp in the format `YYYY-M-D-h:mmp` (e.g. "2025-12-16-10:40am") and returns a list of restaurants that are open at that date/time, e.g.:

```
$ curl http://127.0.0.1:5000/2025-12-16-10:33pm
[
    "Caffe Luna",
    "The Cheesecake Factory",
    "Glenwood Grill",
    "Page Road Grill",
    "Bonchon",
    "Seoul 116",
    "Stanbury",
    "Gringo a Gogo",
    "42nd Street Oyster Bar"
]
```

For valid requests, the HTTP response code will be 200.

If the timestamp formatting is invalid, an error message will be returned, and the HTTP response code will be 400, e.g.:

```
$ curl http://127.0.0.1:5000/bad-param
{
    "error": "Timestamp must be in format YYYY-M-D-h:mmp (e.g. \"2025-5-19-2:30pm\")"
}
~
$ curl -I http://127.0.0.1:5000/bad-param
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.4 Python/3.14.0
Date: Tue, 16 Dec 2025 16:47:12 GMT
Content-Type: application/json
Content-Length: 90
Connection: close
```


