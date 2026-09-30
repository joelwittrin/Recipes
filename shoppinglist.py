import sqlite3

class ShoppingList:

    # Class that manages the shopping list

    def __init__(self, db):

        # Initialize class

        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        
    def create_list(self):

        # Creates shopping list

        query = """
                CREATE TABLE IF NOT EXISTS shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                quantity INTEGER DEFAULT 1
                )
                """
        self.cursor.execute(query)
        self.conn.commit()
        
    def add_item(self, item, quantity):

        # Adds item shopping_list
        # add_item('milk', 2) inserts milk into the item-column and 2 into the quantity-column

        self.cursor.execute("INSERT INTO shopping_list (item, quantity) VALUES (?,?)", (item, quantity))
        self.conn.commit()

        print(f'Added {item} with id: {self.cursor.lastrowid}')

    def remove_item(self, id):
        
        # Removes item in shopping_list
        # remove_item(X) removes item with id X

        self.cursor.execute("DELETE FROM shopping_list WHERE id = ?", (id))
        self.conn.commit()

        print(f'removed item with id {id}')

    def edit_quantity(self, id, quantity):

        # Edits quantity in shopping_list

        # Fetches quantity for id from shopping_list as qty
        self.cursor.execute("SELECT quantity FROM shopping_list WHERE id = ?", (id, ))
        qty = self.cursor.fetchone()[0]

        updated_quantity = qty + quantity
        self.cursor.execute("UPDATE shopping_list SET quantity = ? WHERE id = ?", (updated_quantity, id))
        self.conn.commit()

        print(f'Edited quantity item with id {id} to {quantity}')

    def check_item(self, item, quantity):
        
        # Adds item to shopping list, if item already exists, quantity is edited

        # Fetches id for item
        query = "SELECT id FROM shopping_list WHERE item = ?"
        self.cursor.execute(query, (item, ))
        result = self.cursor.fetchone()

        if result != None:
            id = result[0]
            self.edit_quantity(id, quantity)

        else:
            self.add_item(item, quantity)

    def show_list(self):

        # Shows shopping_list

        self.cursor.execute("SELECT * FROM shopping_list")
        return self.cursor.fetchall()
    
    def clear_list(self):

        # Empties shopping_list
        
        ans = input("Are you sure you want to delete the shopping list?")

        if ans in ["yes", "Yes", "ye", "Ye", "Ja", "ja", "yep", "Yep"]:
            self.cursor.execute("DELETE FROM shopping_list")
            self.conn.commit()
            print('Cleared list!')
        else:
            print('Action canceled')

    def remove_item_by_name(self, item):

        # Removes item in shopping_list by name

        self.cursor.execute("DELETE FROM shopping_list WHERE item = ?",(item,))
        self.conn.commit()

        print(f'Removed item with name {item}')

