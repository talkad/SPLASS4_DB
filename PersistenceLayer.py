import atexit
import sqlite3


# Data Transfer Objects:
class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand


class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Coffee_stand:
    def __init__(self, id_number, location, number_of_employees):
        self.id_number = id_number
        self.location = location
        self.number_of_employees = number_of_employees


class Activity:
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


# Data Access Objects:
class Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO Employees VALUES (?, ?, ?, ?)
           """, (employee.id, employee.name, employee.salary, employee.coffee_stand))

    def get_employee(self):
        cur = self._conn.cursor()
        employeeRecords = cur.execute("""
                    SELECT * FROM Employees
                    ORDER BY id ASC
                """).fetchall()
        return employeeRecords


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO Suppliers VALUES (?, ?, ?)
        """, (supplier.id, supplier.name, supplier.contact_information))

    def get_supplier(self):
        cur = self._conn.cursor()
        suppliersRecords = cur.execute("""
                    SELECT * FROM Suppliers
                    ORDER BY id ASC
                """).fetchall()
        return suppliersRecords


class Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
                INSERT INTO Products VALUES (?, ?, ?, ?)
        """, (product.id, product.description, product.price, product.quantity))

    def get_products(self):
        cur = self._conn.cursor()
        activitiesRecords = cur.execute("""
                    SELECT * FROM Products
                    ORDER BY id ASC
                """).fetchall()
        return activitiesRecords

    def get_quantity_of_id(self, product_id):
        cur = self._conn.cursor()
        cur.execute("""
            SELECT quantity FROM Products WHERE id = ?
            """, (product_id,))
        return cur.fetchone()

    def update_quantity_of_id(self, new_quantity, product_id):
        cur = self._conn.cursor()
        cur.execute("""
                        UPDATE Products SET quantity=? WHERE id=?
                        """, [new_quantity, product_id])



class Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
                INSERT INTO Coffee_stands VALUES (?, ?, ?)
        """, (coffee_stand.id_number, coffee_stand.location, coffee_stand.number_of_employees))

    def get_coffee_stand(self):
        cur = self._conn.cursor()
        standsRecords = cur.execute("""
                    SELECT * FROM Coffee_stands
                    ORDER BY id ASC
                """).fetchall()
        return standsRecords


class Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
                INSERT INTO Activities VALUES (?, ?, ?, ?)
        """, (activity.product_id, activity.quantity, activity.activator_id, activity.date))

    def get_activities(self):
        cur = self._conn.cursor()
        activitiesRecords = cur.execute("""
                    SELECT * FROM Activities
                    ORDER BY date ASC
                """).fetchall()
        return activitiesRecords


class PersistenceLayer(object):
    def get_total_sales(self):
        cur = self.conn.cursor()
        result = cur.execute("""SELECT Employees.name, Employees.salary, Coffee_stands.location, total
                                    FROM (Employees JOIN Coffee_stands ON Employees.coffee_stand=Coffee_stands.id)
                                    LEFT JOIN (SELECT Activities.activator_id as activate_id, (sum(Products.price*Activities.quantity))*(-1) as total
                                                FROM Activities JOIN Products ON Activities.product_id=Products.id
                                                WHERE Activities.quantity<0
                                                GROUP BY  Activities.activator_id) ON Employees.id=activate_id
                                    ORDER BY Employees.name   
                                    """).fetchall()
        return result

    def get_activities_join(self):
        cur = self.conn.cursor()
        result = cur.execute("""SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name
                                    FROM ((Activities JOIN Products ON Activities.product_id=Products.id)
                                    LEFT JOIN Employees ON Activities.activator_id=Employees.id)
                                    LEFT JOIN Suppliers ON Activities.activator_id=Suppliers.id 
                                    ORDER BY Activities.date
                                """).fetchall()
        return result

    def __init__(self):
        self.conn = sqlite3.connect('moncafe.db')
        self.employees = Employees(self.conn)
        self.suppliers = Suppliers(self.conn)
        self.products = Products(self.conn)
        self.coffee_stands = Coffee_stands(self.conn)
        self.activities = Activities(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
            DROP TABLE IF EXISTS  Employees;
            CREATE TABLE "Employees" (
    "id"	INTEGER,
    "name"	TEXT NOT NULL,
    "salary"	REAL NOT NULL,
    "coffee_stand"	INTEGER,
    FOREIGN KEY("coffee_stand") REFERENCES "Coffee_stands"("id"),
    PRIMARY KEY("id")
    );

            DROP TABLE IF EXISTS Suppliers;
    CREATE TABLE "Suppliers" (
    "id"	INTEGER,
    "name"	TEXT NOT NULL,
    "contact_information"	TEXT,
    PRIMARY KEY("id")
);

            DROP TABLE IF EXISTS Products;
    CREATE TABLE "Products" (
    "id"	INTEGER,
    "description"	TEXT NOT NULL,
    "price"	REAL NOT NULL,
    "quantity"	INTEGER NOT NULL,
    PRIMARY KEY("id")
    );

            DROP TABLE IF EXISTS Coffee_stands;
    CREATE TABLE "Coffee_stands" (
    "id"	INTEGER,
    "location"	TEXT NOT NULL,
    "number_of_employees"	INTEGER,
    PRIMARY KEY("id")
    );

            DROP TABLE IF EXISTS Activities;       
    CREATE TABLE "Activities" (
    "product_id"	INTEGER,
    "quantity"	INTEGER NOT NULL,
    "activator_id"	INTEGER NOT NULL,
    "date"	DATE NOT NULL,
    FOREIGN KEY("product_id") REFERENCES "Products"("id")
    );
        """)


# persistence layer is a singleton
psl = PersistenceLayer()
atexit.register(psl.close)

