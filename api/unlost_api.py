# Airport data management API

import mysql.connector

class Unlost:
    # Constructor, creates a connection to the db
    def __init__(self, host, username, password, db_name, flights_table):
        self.con = mysql.connector.connect(host = host,
                                      user=username,
                                      passwd=password,
                                      database=db_name)
        self.flights_table = flights_table

    # Fetches a flight row
    def unlost_get_flight(self, extra):
        query = "SELECT * FROM "+self.flights_table+" WHERE " + extra
        #print(query)
        cursor = self.con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    # Adds a flight to the db
    def unlost_add_flight(self, tag, passport, first_name, last_name, departure, destination, flight):
        query = 'INSERT INTO '+self.flights_table+' VALUES (NULL, %s,%s,%s,%s,%s,%s,%s, current_timestamp(),0)'
        #print(query)
        cursor = self.con.cursor()
        cursor.execute(query,[tag, passport, first_name, last_name, departure, destination, flight])
        self.con.commit()

    # Modify a flight
    def unlost_modify_flight(self, set, where):
        query = 'UPDATE '+self.flights_table+' SET '+set+' WHERE '+where
        #print(query)
        cursor = self.con.cursor()
        cursor.execute(query)
        self.con.commit()

    # Sets the status of a flight
    def unlost_flight_set_status(self, where, status):
        self.unlost_modify_flight("status='"+str(status)+"'", where)

    # Used to get the updated results, if the rows are changed with an external source
    def unlost_refresh(self):
        self.con.commit()

    # Closes the connection
    def unlost_disconnect(self):
        self.con.close()
