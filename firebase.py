import constant as C
class Firebase:

    @staticmethod
    def get_current_request(driver_number):
        try:
            response        = requests.get(config.FIREBASE_DRIVER + driver_number + ".json")
            logging.debug("Status code is " + str(response.status_code))
            if response.status_code == 200:
                if response.json() is None:
                    payload                 = {}
                    payload["status"]       = C.DRIVER_FREE
                    payload["user"]         = C.USER_FREE
                    payload["bookingId"]    = C.NO_BOOKING
                    payload["fare"]         = C.NO_FARE
                    payload["from_lon"]     = C.NO_FROM
                    payload["from_lat"]     = C.NO_FROM
                    payload["to_lon"]       = C.NO_TO
                    payload["to_lat"]       = C.NO_TO
                    payload                 = json.dumps(payload)
                    response                = requests.put(config.FIREBASE_DRIVER + driver_number + ".json", data  = payload)
                response    = dict(response.json())
                return response
            else:
                logging.warning("Firebase request status is " + str(response.status_code))
                return []
        except Exception as e:
            logging.error("Error while getting driver data from firebase database of drivers: " + str(e))
            return []
    
    @staticmethod
    def confirm_user_booking(user_number, driver_number)):
        try:
            payload                     = {}
            payload["status"]           = C.USER_BOOKED
            payload                     = json.dumps(payload)
            response                    = requests.put(config.FIREBASE_USER + user_number + "/status.json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in confirming user booking")
                return 0
            payload                     = {}
            payload["driver"]           = driver_number
            payload                     = json.dumps(payload)
            response                    = requests.put(config.FIREBASE_USER + user_number + "/driver.json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in confirming user booking")
                return 0
        except Exception as e:
            logging.error("Error while confirming user booking in firebase database of users: " + str(e))
            return 0

    @staticmethod
    def confirm_driver_booking(driver_number):
        try:
            payload                     = {}
            payload["status"]           = C.DRIVER_ACCEPT
            payload                     = json.dumps(payload)
            response                    = requests.put(config.FIREBASE_DRIVER + driver_number + "/status.json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in confirming driver booking")
                return 0
        except Exception as e:
            logging.error("Error while confirming driver booking in firebase database of drivers: " + str(e))
            return 0

    @staticmethod
    def reject(driver_number):
        payload                     = {}
        payload["status"]           = C.DRIVER_FREET
        payload                     = json.dumps(payload)
            response                = requests.put(config.FIREBASE_DRIVER + driver_number + "/status.json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in rejecting booking")
                return 0
        except Exception as e:
            logging.error("Error while rejecting booking in firebase database of drivers: " + str(e))
            return 0

    @staticmethod
    def reset_user(user_number):
        try:
            payload                     = {}
            payload["driver"]           = C.DRIVER_FREE
            payload["status"]           = C.USER_FREEE
            payload["bookingId"]        = C.NO_BOOKING
            payload["requester"]        = []
            payload["fare"]             = C.NO_FARE
            payload["from_lon"]         = C.NO_FROM
            payload["from_lat"]         = C.NO_FROM
            payload["to_lon"]           = C.NO_TO
            payload["to_lat"]           = C.NO_TO

            payload                     = json.dumps(payload)
            response                    = requests.put(config.FIREBASE_USER + user_number + ".json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in resetting user")
                return 0
        except Exception as e:            
            logging.error("Error while resetting user in firebase users: " + str(e))
            return 0

    # Resets status of a driver
    @staticmethod
    def reset_driver(driver_number):
        try:
            payload                 = {}
            payload["status"]       = C.DRIVER_FREE
            payload["user"]         = C.USER_FREE
            payload["bookingId"]    = C.NO_BOOKING
            payload["fare"]         = C.NO_FARE
            payload["from_lon"]     = C.NO_FROM
            payload["from_lat"]     = C.NO_FROM
            payload["to_lon"]       = C.NO_TO
            payload["to_lat"]       = C.NO_TO
            payload                 = json.dumps(payload)
            response                = requests.put(config.FIREBASE_DRIVER + driver_number + ".json", data  = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.warning("Firebase request status is " + str(response.status_code))
                return 0
        except Exception as e:
            logging.error("Error while resetting status of driver in firebase drivers: " + str(e))
            return 0

