
CREATE TABLE IF NOT EXISTS recipe(
    id  INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS ingredients_recipe(
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe(id),
    ingredient TEXT,
    amount REAL,    -- REAL = non integer, i.e. 1.45 etc
    unit TEXT
);

CREATE TABLE IF NOT EXISTS pantry(
    available_ingredient TEXT,
    amount REAL,
    unit TEXT
);

INSERT INTO recipe (name, description)
VALUES ('Tacos', 'Classic tacos with ground beef');
INSERT INTO ingredients_recipe (recipe_id, ingredient, amount, unit) VALUES
    (1, 'Ground beef',  500,  'g'),
    (1, 'Taco spice',   1,    'packet'),
    (1, 'Taco shells',  12,   'pcs'),
    (1, 'Salsa',        1,    'can'),
    (1, 'Grated cheese',200,  'g'),
    (1, 'Lettuce',      0.5,  'head'),
    (1, 'Sour cream',   200,  'ml'),
    (1, 'Tomato',       2,    'pcs');

