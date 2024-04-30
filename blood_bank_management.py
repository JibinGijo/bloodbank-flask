import mysql.connector

class BloodBankManagement:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="bloodbank"
        )
        self.cursor = self.conn.cursor()

    def add_donor(self, name, blood_type, phone_number, city, state):
        query = "INSERT INTO Donors (name, blood_type, phone_number, city, state) VALUES (%s, %s, %s, %s, %s)"
        values = (name, blood_type, phone_number, city, state)
        self.cursor.execute(query, values)
        self.conn.commit()

    def add_recipient(self, name, blood_type, phone_number, city, state):
        query = "INSERT INTO Recipients (name, blood_type, phone_number, city, state) VALUES (%s, %s, %s, %s, %s)"
        values = (name, blood_type, phone_number, city, state)
        self.cursor.execute(query, values)
        self.conn.commit()

    def add_blood(self, blood_type, quantity):
        query = "INSERT INTO BloodInventory (blood_type, quantity) VALUES (%s, %s) ON DUPLICATE KEY UPDATE quantity = quantity + %s"
        values = (blood_type, quantity, quantity)
        self.cursor.execute(query, values)
        self.conn.commit()

    def search_donors(self, blood_type, city=None, state=None):
        query = "SELECT * FROM Donors WHERE blood_type = %s"
        params = [blood_type]

        if city:
            query += " AND city = %s"
            params.append(city)
        if state:
            query += " AND state = %s"
            params.append(state)

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def search_recipients(self, blood_type, city=None, state=None):
        query = "SELECT * FROM Recipients WHERE blood_type = %s"
        params = [blood_type]

        if city:
            query += " AND city = %s"
            params.append(city)
        if state:
            query += " AND state = %s"
            params.append(state)

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def get_blood_inventory(self):
        query = "SELECT * FROM BloodInventory"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def check_stock_availability(self, blood_type, quantity):
        query = "SELECT quantity FROM BloodInventory WHERE blood_type = %s"
        self.cursor.execute(query, (blood_type,))
        result = self.cursor.fetchone()
        if result:
            return result[0] >= quantity
        return False

    def remove_blood(self, blood_type, quantity):
        query = "UPDATE BloodInventory SET quantity = quantity - %s WHERE blood_type = %s AND quantity >= %s"
        values = (quantity, blood_type, quantity)
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_recipient_list(self):
        query = "SELECT * FROM Recipients"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_blood_exchange_table(self):
        query = """
            SELECT 
                d.name AS donor_name,
                r.name AS recipient_name,
                b.blood_type,
                b.quantity
            FROM 
                Donors d
            JOIN 
                BloodExchange be ON d.id = be.donor_id
            JOIN 
                Recipients r ON be.recipient_id = r.id
            JOIN 
                BloodInventory b ON be.blood_type = b.blood_type
        """
        self.cursor.execute(query)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

