import  logging
import  requests
import  json
from    flask   import Flask
from    flask   import request
from    book    import Book
from authorize  import Authorize
from    urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


logging.basicConfig(level=logging.DEBUG)
app             = Flask(__name__)

default_error   = json.dumps({"error_code": 500, "error_message": "Internal server error", "display_message": ""})

print("driver-booking started")
@app.route("/v1")
def working():
    return "driver-booking service running"


@app.route("/v1/accept", methods=["POST"])
def accept():
    try:
        jwt_token = request.headers["token"]
        stat, tok = Authorize.verify_jwt(jwt_token)
        if stat == 0:
            raise ValueError("Not authorized")
        if request.method == "POST":
            driver_number   = request.args["number"]
            response        = Book.accept(driver_number)
            if len(tok) > 0:
                response["data"]["tokenStatus"]    = "new"
                response["data"]["token"]           = tok
            else:
                response["data"]["tokenStatus"]    = "same"
                response["data"]["token"]           = jwt_token
            response        = json.dumps(response)
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/accept with error: " + str(e))
        return default_error


@app.route("/v1/reject", methods=["POST"])
def reject():
    try:
        jwt_token = request.headers["token"]
        stat, tok = Authorize.verify_jwt(jwt_token)
        if stat == 0:
            raise ValueError("Not authorized")
        if request.method == "POST":
            driver_number   = request.args["number"]
            response        = Book.reject(driver_number)
            if len(tok) > 0:
                response["data"]["tokenStatus"]    = "new"
                response["data"]["token"]           = tok
            else:
                response["data"]["tokenStatus"]    = "same"
                response["data"]["token"]           = jwt_token
            response        = json.dumps(response)
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/reject with error: " + str(e))
        return default_error


@app.route("/v1/cancel", methods=["POST"])
def cancel():
    try:
        jwt_token = request.headers["token"]
        stat, tok = Authorize.verify_jwt(jwt_token)
        if stat == 0:
            raise ValueError("Not authorized")
        if request.method == "POST":
            user_number     = request.args["userNumber"]
            booking_id      = request.args["bookingId"]
            response        = Book.cancel(user_number, booking_id)
            if len(tok) > 0:
                response["data"]["tokenStatus"]    = "new"
                response["data"]["token"]           = tok
            else:
                response["data"]["tokenStatus"]    = "same"
                response["data"]["token"]           = jwt_token
            response        = json.dumps(response)
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/cancel with error: " + str(e))
        return default_error


@app.route("/v1/startTrip", methods=["POST"])
def start_trip():
    try:
        jwt_token = request.headers["token"]
        stat, tok = Authorize.verify_jwt(jwt_token)
        if stat == 0:
            raise ValueError("Not authorized")
        if request.method == "POST":
            user_number     = request.args["userNumber"]
            booking_id      = request.args["bookingId"]
            response        = Book.start_trip(user_number, booking_id)
            if len(tok) > 0:
                response["data"]["tokenStatus"]    = "new"
                response["data"]["token"]           = tok
            else:
                response["data"]["tokenStatus"]    = "same"
                response["data"]["token"]           = jwt_token
            response        = json.dumps(response)
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/startTrip with error: " + str(e))
        return default_error


@app.route("/v1/endTrip", methods=["POST"])
def end_trip():
    try:
        jwt_token = request.headers["token"]
        stat, tok = Authorize.verify_jwt(jwt_token)
        if stat == 0:
            raise ValueError("Not authorized")
        if request.method == "POST":
            user_number     = request.args["userNumber"]
            booking_id      = request.args["bookingId"]
            response        = Book.end_trip(user_number, booking_id)
            if len(tok) > 0:
                response["data"]["tokenStatus"]    = "new"
                response["data"]["token"]           = tok
            else:
                response["data"]["tokenStatus"]    = "same"
                response["data"]["token"]           = jwt_token
            response        = json.dumps(response)
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/endTrip with error: " + str(e))
        return default_error


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7003, debug=True, ssl_context='adhoc')
