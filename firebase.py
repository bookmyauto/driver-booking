import constant as C
import json
import config
import requests
import logging


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
                    payload["fromLon"]     = C.NO_FROM
                    payload["fromLat"]     = C.NO_FROM
                    payload["toLon"]       = C.NO_TO
                    payload["toLat"]       = C.NO_TO
                    payload                 = json.dumps(payload)
                    response                = requests.put(config.FIREBASE_DRIVER + str(driver_number) + ".json", data  = payload)
                response    = dict(response.json())
                return response
            else:
                logging.warning("Firebase request status is " + str(response.status_code))
                return []
        except Exception as e:
            logging.error("Error while getting driver data from firebase database of drivers: " + str(e))
            return []
    
    @staticmethod
    def confirm_user_booking(user_number, driver_number, driver_name, vehicle):
        try:
            payload                     = {}
            payload["status"]           = C.USER_BOOKED
            payload["driver"]           = int(driver_number)
            payload["driver_name"]      = driver_name
            payload["vehicle"]          = vehicle
            payload["requester"]        = []
            payload                     = json.dumps(payload)
            response                    = requests.patch(config.FIREBASE_USER + str(user_number) + ".json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in confirming user booking")
                return 0
        except Exception as e:
            logging.error("Error while confirming user booking in firebase database of users: " + str(e))
            return 0

    @staticmethod
    def reset_user(user_number):
        try:
            payload                     = {}
            payload["driver"]           = C.DRIVER_FREE
            payload["status"]           = C.USER_FREE
            payload["bookingId"]        = C.NO_BOOKING
            payload["requester"]        = []
            payload["fare"]             = C.NO_FARE
            payload["seats"]            = C.NO_SEATS
            payload["fromLon"]          = C.NO_FROM
            payload["fromLat"]          = C.NO_FROM
            payload["toLon"]            = C.NO_TO
            payload["toLat"]            = C.NO_TO
            payload["driver_name"]      = C.NO_NAME
            payload["vehicle"]          = C.NO_VEHICLE

            payload                     = json.dumps(payload)
            response                    = requests.put(config.FIREBASE_USER + str(user_number) + ".json", data = payload)
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
            payload["seats"]        = C.NO_SEATS
            payload["fromLon"]     = C.NO_FROM
            payload["fromLat"]     = C.NO_FROM
            payload["toLon"]       = C.NO_TO
            payload["toLat"]       = C.NO_TO
            payload                 = json.dumps(payload)
            response                = requests.put(config.FIREBASE_DRIVER + str(driver_number) + ".json", data  = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.warning("Firebase request status is " + str(response.status_code))
                return 0
        except Exception as e:
            logging.error("Error while resetting status of driver in firebase drivers: " + str(e))
            return 0

    @staticmethod
    def start_trip(user_number):
        try:
            payload                     = {}
            payload["status"]           = C.USER_IN_RIDE
            payload                     = json.dumps(payload)
            response                    = requests.patch(config.FIREBASE_USER + str(user_number) + ".json", data = payload)
            if response.status_code == 200:
                return 1
            else:
                logging.debug("Error in starting user ride")
                return 0
        except Exception as e:
            logging.error("Error while starting user ride in firebase database of users: " + str(e))
            return 0 
