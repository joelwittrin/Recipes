from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def make_card(name: str, description: str = "") -> dict:
    """Skapar ett kort från ett namn och valfri beskrivning."""
    return {
        "name": name,
        "description": description,
    }


CARDS = [
    make_card("Tacos",        "Kryddigt nötkött, salsa, guacamole"),
    make_card("Sushi",        "Lax, avokado, japanskt ris"),
    make_card("Pizza",        "Tomatsås, mozzarella, basilika"),
    make_card("Pad Thai",     "Risnudlar, jordnötter, lime"),
    make_card("Lammgryta",    "Långkokt med rotfrukter och timjan"),
    make_card("Caesarsallad", "Romansallad, parmesan, krutonger"),
    make_card("Ramen",        "Rik buljong, ägg, nori"),
    make_card("Köttbullar",   "Med potatismos och lingon"),
]

@app.route("/")
def index():
    return render_template("swiper.html")

@app.route("/swiper", methods=["POST"])
def post_cards():
    return jsonify(CARDS)


if __name__ == "__main__":
    app.run(debug=True)