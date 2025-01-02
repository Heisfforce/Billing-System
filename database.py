import sqlite3

def create_tables():
    conn = sqlite3.connect('Products.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Meals (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL)''')  

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Drinks (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL)''')  

    conn.commit()
    conn.close()

def insert_products():
    conn = sqlite3.connect('Products.db')
    cursor = conn.cursor()

    meals_data = [
        ('M1', 'Risotto', 100.0),  
        ('M2', 'Braciole', 150.0),  
        ('M3', 'Arancini', 120.0)  
    ]

    drinks_data = [
        ('D1', 'Orange Juice', 25.0),  
        ('D2', 'Strawberry Juice', 30.0),  
        ('D3', 'Lemonade', 20.0)  
    ]

    cursor.executemany('INSERT OR REPLACE INTO Meals (id, name, price) VALUES (?, ?, ?)', meals_data)

    cursor.executemany('INSERT OR REPLACE INTO Drinks (id, name, price) VALUES (?, ?, ?)', drinks_data)

    conn.commit()
    conn.close()

def get_product_prices():
    conn = sqlite3.connect('Products.db')
    cursor = conn.cursor()

    cursor.execute('SELECT price FROM Meals')
    meals_prices = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT price FROM Drinks')
    drinks_prices = [row[0] for row in cursor.fetchall()]

    conn.close()
    return meals_prices, drinks_prices

create_tables()
insert_products()

meals_prices, drinks_prices = get_product_prices()
print("Meals Prices:", meals_prices)
print("Drinks Prices:", drinks_prices)
