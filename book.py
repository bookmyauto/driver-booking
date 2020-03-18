import  constant as C
import  logging
from    response import Response
from    firebase import Firebase
from    datetime import datetime
from    sql import Sql

class Book:
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                                   ACCEPT A REQUEST                                                                                        #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def accept(driver_number):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            booking_details                 = Firebase.get_current_request(driver_number)
            if booking_details["bookingId"] == -1:
                raise ValueError('There is no booking for this driver')
            if len(booking_details) == 0:
                raise ValueError('Booking details is empty')
            user_number                     = int(booking_details["user"])
            fare                            = float(booking_details["fare"])
            booking_id                      = booking_details["bookingId"]
            from_lon                        = float(booking_details["from_lon"])
            from_lat                        = float(booking_details["from_lat"])
            to_lon                          = float(booking_details["to_lon"])
            to_lat                          = float(booking_details["to_lat"])
            seats                           = int(booking_details["seats"])
            now_time                        = datetime.timestamp(datetime.now())

            sql_query                       = "select name, vehicle from drivers where number = '{0}'"
            cur.execute(sql_query.format(driver_number))
            d                               = cur.fetchone()
            driver_name                     = str(d[0])
            vehicle                         = str(d[1])
            sql_query                       = "insert into driver_history (booking_id, driver_number, timestamp) values ('{0}', {1}, {2})"
            cur.execute(sql_query.format(booking_id, driver_number, now_time))
            conn.commit()

            sql_query = "insert into distance(booking_id, status, dist, driver, from_lon, from_lat) values('{0}', 1, -1.0, '{1}', {2}, {3})"
            cur.execute(sql_query.format(booking_id, driver_number, from_lon, from_lat))
            conn.commit()

            sql_query                       = "insert into user_history (booking_id, user_number, timestamp) values ('{0}', {1}, {2})"
            cur.execute(sql_query.format(booking_id, user_number, now_time))
            conn.commit()

            status                          = Firebase.confirm_user_booking(user_number, driver_number, driver_name, vehicle)
            
            sql_query                       = "insert into user_booking(booking_id, user_number, status, driver_number, fare, activity, from_lon, from_lat, to_lon, to_lat, seats) values('{0}', '{1}', {2}, '{3}', {4}, '{5}', {6}, {7}, {8}, {9}, {10})"
            cur.execute(sql_query.format(booking_id, user_number, C.USER_BOOKED, driver_number, fare, "user_booked", from_lon, from_lat, to_lon, to_lat, seats))
            conn.commit()
 
            conn.close()
            result = Response.make_response(200, "Driver accepted", "Request accepted successfully", fare = fare, bookingId = booking_id)
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in accepting request: " + str(e))
            return Response.default_error
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                                   REJECT A REQUEST                                                                                        #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def reject(driver_number):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            status                          = Firebase.reset_driver(driver_number)
            conn.close()
            if status == 1:
                result  = Response.make_response(200, "Driver rejected", "Request rejected")
                return result
            else:
                raise ValueError("Error in rejecting")
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in rejecting request: " + str(e))
            return Response.default_error

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                                   CANCEL A BOOKING                                                                                        #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def cancel(user_number, booking_id):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            status                          = Firebase.reset_user(user_number)
            if status == 0:
                raise ValueError("Error in cancelling")

            sql_query                       = "update user_booking set activity = concat(activity, '|', 'driver_cancelled'), status = {0} where booking_id = '{1}'"
            cur.execute(sql_query.format(C.DRIVER_CANCELLED, booking_id))
            conn.commit()

            sql_query = "update distance set status = 0 where booking_id = '{0}'"
            cur.execute(sql_query.format(booking_id))
            conn.commit()

            conn.close()
            result  = Response.make_response(200, "Cancelled", "Request has been successfully cancelled")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in cancelling request: " + str(e))
            return Response.default_error

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                                   START TRIP                                                                                              #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def start_trip(user_number, booking_id):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            
            status                          = Firebase.start_trip(user_number)
            if status == 0:
                raise ValueError("Error in starting trip")
            
            sql_query                       = "update user_booking set activity = concat(activity, '|', 'user_in_ride'), status = {0} where booking_id = '{1}'"
            cur.execute(sql_query.format(C.USER_IN_RIDE, booking_id))
            conn.commit()

            sql_query = "update distance set status = 0 where booking_id = '{0}'"
            cur.execute(sql_query.format(booking_id))
            conn.commit()

            conn.close()
            result  = Response.make_response(200, "Started", "Trip started")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in start trip request: " + str(e))
            return Response.default_error

    @staticmethod
    def end_trip(user_number, booking_id):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            
            status                          = Firebase.reset_user(user_number)
            if status == 0:
                raise ValueError("Error in ending trip")
            
            sql_query                       = "update user_booking set activity = concat(activity, '|', 'driver_end_trip'), status = {0} where booking_id = '{1}' and status != {2}"
            cur.execute(sql_query.format(C.USER_END_TRIP, booking_id, C.USER_END_TRIP))
            conn.commit()
             
            conn.close()
            result  = Response.make_response(200, "Ended", "Trip ended")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in end trip request: " + str(e))
            return Response.default_error
