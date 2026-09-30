from pantry import Pantry
from shoppinglist import ShoppingList
import sqlite3
from datetime import datetime

class Manager:

    def __init__(self, db):

        # Initialize class

        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.Pantry = Pantry
        self.ShoppingList = ShoppingList

    def add_recipe(self, recipe, threshold):

        # Add recipe to shopping list based on if items are in pantry, according to amount and if item is fresh

        # NOTE THAT THRESHOLD IS A PLACEHOLDER AND SHOULD BE REMOVED FOR CLEANER CODE. REBUILD DATABASE!!!

        query = """
                SELECT i.ingredient, i.amount, i.unit
                FROM ingredient_recipe i
                JOIN recipe r ON i.recipe_id = r.id
                WHERE r.name = ?
                """

        self.cursor.execute(query, (recipe, ))
        result = self.cursor.fetchall()         #item, qty, unit from the recipe for each ingredient

        for item, qty in result:

            fresh = self.pantry.freshness(item, threshold)
            qty_in_pantry = self.pantry.show_quantity(item)

            if qty_in_pantry == 0 or not fresh:
                self.shoppinglist.add_item(item, qty)
            elif qty_in_pantry < qty * 0.95:
                self.shoppinglist.add_item(item, qty)
            else:
                print(f"{item} is available in pantry (+/- 5%) and has not been added to the shopping list")
       
    def remove_recipe_shoppinglist(self, recipe):

        # Removes items in recipe from shopping list

        query = """
                SELECT i.ingredient, i.amount
                FROM ingredients_recipe i
                JOIN recipe r ON i.recipe_id = r.id
                WHERE r.name = ?
                """
        self.cursor.execute(query, (recipe, ))
        results = self.cursor.fetchall()

        for item, qty in results:
            self.shoppinglist.remove_item_by_name(item, qty)

    def remove_recipe_pantry(self, recipe):

        # Removes items in recipe from pantry

        query = """
                SELECT i.ingredient, i.amount
                FROM ingredients_recipe i
                JOIN recipe r ON i.recipe_id = r.id
                WHERE r.name = ?
                """
        self.cursor.execute(query, (recipe, ))
        results = self.cursor.fetchall()

        for item, qty in results:
            self.pantry.remove_item_by_name(item, qty)





### ==================== DEBUGGING AND NOTES ==================== ###

def test_setup():

    # Check if connection is made

    db = "database.sql"

    try:
        
        pantry = Pantry(db)
        list = ShoppingList(db)
        print("Import succesful!")
        
        pantry.create_pantry()
        list.create_list()
        
        print("Database connected")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_setup()

'''
Svårare idéer att jobba med:
    - Ladda ned data från Hemköp, Coop, Ica osv., själv och fr. kompisar för att beräkna
      genomsnittlig kostnad för diverse produkter
    - Beräkna kcal per maträtt, hämta från t.ex. livsmedelverket
    - Implementera egenskaper för varje maträtt; hur dyrt, antal ingredienser, antal kcal, snabbhet mm.
'''