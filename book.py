import  constant as C
from    response import Response
from    firebase import Firebase
from    sql import Sql

class Book:

    @staticmethod
    def accept(driver_number):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            booking_details                 = Firebase.get_current_request(driver_number)
            if len(booking_details) == 0:
                raise ValueError('booking details is empty')
            user_number                     = booking_details["user_number"]
            fare                            = booking_details["fare"]
            booking_id                      = booking_details["booking_id"]
            from_lon                        = booking_details["from_lon"]
            from_lat                        = booking_details["from_lat"]
            to_lon                          = booking_details["to_lon"]
            to_lat                          = booking_details["to_lat"]
            status                          = Firebase.confirm_driver_booking(driver_number)
            status                          = Firebase.confirm_user_booking(user_number, driver_number)
            
            sql_query                       = "insert into user_booking(booking_id, user_number, status, driver_number, fare, activity, from_lon, from_lat, to_lon, to_lat) values('{0}', '{1}', {2}, '{3}', {4}, '{5}', {6}, {7}, {8}, {9})"
            cur.execute(sql_query.format(booking_id, user_number, C.USER_BOOKED, driver_number, fare, "user_booked|", from_lon, from_lat, to_lon, to_lat))
            conn.commit()

            sql_query   = "update driver_status set status = {0} where driver_number = '{1}'"
            cur.execute(sql_query.format(C.DRIVER_ACCEPT, driver_number))
            conn.commit()
            
            conn.close()
            result = Response.make_result(200, "Driver accepted", "Driver has accepted your request", fare = fare, bookingId = booking_id)
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in accepting request: " + str(e)):
            return Response.default_error
    
    @staticmethod
    def reject(driver_number):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            status                          = Firebase.reject(driver_number)
            
            sql_query                       = "update driver_status set status = {0} where driver_number = '{1}'"
            cur.execute(sql_query.format(C.DRIVER_FREE, driver_number))
            conn.commit()
            conn.close()
            result = Response.make_result(200, "Driver rejected", "Request rejected")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in rejecting request: " + str(e))
            return Response.default_error

    @staticmethod
    def cancel(driver_number):
        conn    = None
        try:
            conn, cur                       = Sql.get_connection()
            booking_details                 = Firebase.get_current_request(driver_number)
            if len(booking_details) == 0:
                raise ValueError('booking details is empty')
            user_number                     = booking_details["user_number"]
            booking_id                      = booking_details["booking_id"]
            status                          = Firebase.reset_driver(driver_number)
            status                          = Firebase.reset_user(user_number)
            
            sql_query                       = "update user_booking set activity = concat(activity, '|', 'driver_cancelled') where booking_id = '{0}'"
            cur.execute(sql_query.format(booking_id))
            conn.commit()
            
            sql_query                       = "update driver_status set status = '{0}' where driver_number = '{1}'"
            cur.execute(sql_query.format(C.DRIVER_FREE, driver_number))
            conn.commit()

            conn.close()
            result  = Response.make_result(200, "Cancelled", "Request has been successfully cancelled")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in cancelling request: " + str(e)):
            return Response.default_error
