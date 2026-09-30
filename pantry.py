import sqlite3
from datetime import datetime

class Pantry:

    # Class that manages the pantry

    def __init__(self, db):

        # Initialize class

        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def create_pantry(self):

        # Creates pantry. Note that date must be inserted as YYYY-MM-DD

        query = """
                CREATE TABLE IF NOT EXISTS pantry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                date DATE 
                )
                """
        self.cursor.execute(query)
        self.conn.commit()

    def add_item(self, item, quantity, date):

        # Adds item to pantry
        # add_item('milk', 2) inserts milk into the item-column and 2 into the quantity-column

        self.cursor.execute("INSERT INTO pantry (item, quantity, date) VALUES (?,?,?)", (item, quantity, date))
        self.conn.commit()

        print(f'Added {item} with id: {self.cursor.lastrowid}')

    def remove_item(self, id):
        
        # Removes item in pantry
        # remove_item(X) removes item with id X

        self.cursor.execute("DELETE FROM pantry WHERE id = ?", (id))
        self.conn.commit()

        print(f'removed item with id {id}')

    def remove_item_by_name(self, item):

        # Removes item in pantry by name

        self.cursor.execute("DELETE FROM pantry WHERE item = ?",(item,))
        self.conn.commit()

        print(f'Removed item with name {item}')

    def edit_quantity(self, id, quantity):

        # Edits quantity in pantry

        # Fetches quantity for id from pantry as qty
        self.cursor.execute("SELECT quantity FROM pantry WHERE id = ?", (id, ))
        qty = self.cursor.fetchone()[0]

        updated_quantity = qty + quantity
        self.cursor.execute("UPDATE pantry SET quantity = ? WHERE id = ?", (updated_quantity, id))
        self.conn.commit()

        print(f'Edited quantity item with id {id} to {quantity}')

    def check_item(self, item, quantity):
        
        # Adds item to pantry, if item already exists, quantity is edited

        # Fetches id for item
        query = "SELECT id FROM pantry WHERE item = ?"
        self.cursor.execute(query, (item, ))
        result = self.cursor.fetchone()

        if result != None:
            id = result[0]
            self.edit_quantity(id, quantity)
        else:
            self.add_item(item, quantity)

    def show_list(self):

        # Shows pantry

        self.cursor.execute("SELECT * FROM pantry")
        return self.cursor.fetchall()
    
    def show_item(self, item):
        
        # Shows specific item in pantry

        self.cursor.execute("SELECT * FROM pantry WHERE item = ?", (item,))
        result = self.cursor.fetchone()
    
        if result != None:
            print(f'There is {result[2]} of {result[1]} in the pantry')
            return result
        else:
            print(f'No {item} found in pantry')
            return None

    def clear_list(self):

        # Empties pantry

        ans = input("Are you sure you want to delete THE ENTIRE pantry")

        if ans in ["yes", "Yes", "ye", "Ye", "Ja", "ja", "yep", "Yep"]:
            self.cursor.execute("DELETE FROM pantry")
            self.conn.commit()
            print('Cleared list!')
        else:
            print('Action canceled')

    def sort_by_date(self):

        # Sorts available items in pantry by date

        self.cursor.execute("SELECT * FROM pantry ORDER BY date ASC")
        return self.cursor.fetchall()

    def freshness(self, item, threshold):

        # Checks if item(s) in pantry is fresh. Returns True or False, i.e. fresh or not fresh

        all_fresh = True

        self.cursor.execute("SELECT item, date FROM pantry WHERE item = ?", (item, ))
        result = self.cursor.fetchall() # Returns tuple, e.g. [('mjölk', '2026-06-09')]

        for row in result:

            # Calculate the difference in dates by days. Requires stripping of the date added given as a string
            tdy        = datetime.today()
            date_added = datetime.strptime(row[1], "%Y-%m-%d")
            difference = tdy - date_added
            
            if difference.days >= threshold:
                print(f'{item} is {difference.days} days old. Check if fresh!')
                all_fresh = False
            else:
                print(f'{item} is {difference.days} days old and is still fresh!')

        return all_fresh
        
    def show_quantity(self, item):
        
        # Returns quantity of item in pantry

        self.cursor.execute("SELECT quantity FROM item WHERE item = ?", (item, ))
        qty = self.cursor.fetchone()

        if qty is None:
            return 0
        else:
            return qty[0]
        
