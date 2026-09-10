from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

from chatbot_config import APP_NAME, MODEL, SYSTEM_PROMPT


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# GEMINI CLIENT
# =========================================================

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ Gemini API key loaded successfully.")
else:
    client = None
    print("⚠️ GEMINI_API_KEY is missing from .env")


# =========================================================
# FOOD MENU
# =========================================================

FOODS = [

    # ---------------- BURGERS ----------------

    {
        "id": 1,
        "name": "Classic Chicken Burger",
        "category": "Burgers",
        "price": 149,
        "emoji": "🍔",
        "description": "Juicy chicken patty with fresh vegetables and creamy sauce.",
        "rating": 4.8,
        "time": "20-25 min"
    },

    {
        "id": 2,
        "name": "Crispy Chicken Burger",
        "category": "Burgers",
        "price": 179,
        "emoji": "🍔",
        "description": "Crispy fried chicken with lettuce and special Zestora sauce.",
        "rating": 4.7,
        "time": "20-25 min"
    },

    {
        "id": 3,
        "name": "Paneer Crunch Burger",
        "category": "Burgers",
        "price": 139,
        "emoji": "🍔",
        "description": "Crispy paneer patty with fresh vegetables and spicy mayo.",
        "rating": 4.6,
        "time": "20-25 min"
    },


    # ---------------- PIZZA ----------------

    {
        "id": 4,
        "name": "Veg Supreme Pizza",
        "category": "Pizza",
        "price": 249,
        "emoji": "🍕",
        "description": "Loaded pizza with fresh vegetables and melted cheese.",
        "rating": 4.7,
        "time": "25-30 min"
    },

    {
        "id": 5,
        "name": "Chicken Tikka Pizza",
        "category": "Pizza",
        "price": 299,
        "emoji": "🍕",
        "description": "Cheesy pizza topped with spicy chicken tikka.",
        "rating": 4.9,
        "time": "25-30 min"
    },

    {
        "id": 6,
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 199,
        "emoji": "🍕",
        "description": "Classic pizza with tomato sauce, mozzarella and herbs.",
        "rating": 4.6,
        "time": "20-25 min"
    },


    # ---------------- BIRYANI ----------------

    {
        "id": 7,
        "name": "Chicken Biryani",
        "category": "Biryani",
        "price": 199,
        "emoji": "🍛",
        "description": "Aromatic basmati rice cooked with tender chicken and spices.",
        "rating": 4.9,
        "time": "25-30 min"
    },

    {
        "id": 8,
        "name": "Mutton Biryani",
        "category": "Biryani",
        "price": 279,
        "emoji": "🍛",
        "description": "Flavorful basmati rice with tender mutton and traditional spices.",
        "rating": 4.9,
        "time": "30-35 min"
    },

    {
        "id": 9,
        "name": "Veg Biryani",
        "category": "Biryani",
        "price": 159,
        "emoji": "🍛",
        "description": "Fragrant basmati rice cooked with fresh vegetables and spices.",
        "rating": 4.6,
        "time": "20-25 min"
    },


    # ---------------- INDIAN ----------------

    {
        "id": 10,
        "name": "Paneer Butter Masala",
        "category": "Indian",
        "price": 179,
        "emoji": "🥘",
        "description": "Soft paneer cooked in a rich and creamy tomato gravy.",
        "rating": 4.6,
        "time": "20-25 min"
    },

    {
        "id": 11,
        "name": "Butter Chicken",
        "category": "Indian",
        "price": 229,
        "emoji": "🍗",
        "description": "Tender chicken cooked in a creamy buttery tomato sauce.",
        "rating": 4.8,
        "time": "25-30 min"
    },

    {
        "id": 12,
        "name": "Chole Bhature",
        "category": "Indian",
        "price": 139,
        "emoji": "🍽️",
        "description": "Spicy chickpea curry served with fluffy bhature.",
        "rating": 4.7,
        "time": "20-25 min"
    },


    # ---------------- SOUTH INDIAN ----------------

    {
        "id": 13,
        "name": "Masala Dosa",
        "category": "South Indian",
        "price": 99,
        "emoji": "🥞",
        "description": "Crispy dosa served with delicious potato masala.",
        "rating": 4.8,
        "time": "15-20 min"
    },

    {
        "id": 14,
        "name": "Idli Sambar",
        "category": "South Indian",
        "price": 79,
        "emoji": "🥣",
        "description": "Soft steamed idlis served with hot sambar and chutney.",
        "rating": 4.7,
        "time": "15-20 min"
    },

    {
        "id": 15,
        "name": "Paneer Dosa",
        "category": "South Indian",
        "price": 129,
        "emoji": "🥞",
        "description": "Crispy dosa filled with flavorful paneer masala.",
        "rating": 4.6,
        "time": "20-25 min"
    },

    {
        "id": 16,
        "name": "Ghee Roast Dosa",
        "category": "South Indian",
        "price": 119,
        "emoji": "🥞",
        "description": "Golden crispy dosa roasted with aromatic ghee.",
        "rating": 4.9,
        "time": "15-20 min"
    },


    # ---------------- RICE ----------------

    {
        "id": 17,
        "name": "Chicken Fried Rice",
        "category": "Rice",
        "price": 169,
        "emoji": "🍚",
        "description": "Flavorful fried rice with chicken and fresh vegetables.",
        "rating": 4.7,
        "time": "20-25 min"
    },

    {
        "id": 18,
        "name": "Veg Fried Rice",
        "category": "Rice",
        "price": 129,
        "emoji": "🍚",
        "description": "Classic fried rice loaded with fresh vegetables.",
        "rating": 4.5,
        "time": "20-25 min"
    },

    {
        "id": 19,
        "name": "Schezwan Chicken Rice",
        "category": "Rice",
        "price": 189,
        "emoji": "🍚",
        "description": "Spicy Schezwan rice tossed with chicken and vegetables.",
        "rating": 4.7,
        "time": "20-25 min"
    },


    # ---------------- NOODLES ----------------

    {
        "id": 20,
        "name": "Chicken Hakka Noodles",
        "category": "Noodles",
        "price": 179,
        "emoji": "🍜",
        "description": "Stir-fried noodles with chicken and crunchy vegetables.",
        "rating": 4.7,
        "time": "20-25 min"
    },

    {
        "id": 21,
        "name": "Veg Hakka Noodles",
        "category": "Noodles",
        "price": 139,
        "emoji": "🍜",
        "description": "Classic Hakka noodles tossed with fresh vegetables.",
        "rating": 4.5,
        "time": "20-25 min"
    },


    # ---------------- SNACKS ----------------

    {
        "id": 22,
        "name": "French Fries",
        "category": "Snacks",
        "price": 99,
        "emoji": "🍟",
        "description": "Golden crispy fries seasoned with Zestora special seasoning.",
        "rating": 4.6,
        "time": "10-15 min"
    },

    {
        "id": 23,
        "name": "Chicken Nuggets",
        "category": "Snacks",
        "price": 129,
        "emoji": "🍗",
        "description": "Crispy golden chicken nuggets served with dipping sauce.",
        "rating": 4.7,
        "time": "15-20 min"
    },

    {
        "id": 24,
        "name": "Paneer Tikka",
        "category": "Snacks",
        "price": 159,
        "emoji": "🍢",
        "description": "Grilled paneer cubes marinated with aromatic Indian spices.",
        "rating": 4.8,
        "time": "20-25 min"
    },


    # ---------------- HEALTHY ----------------

    {
        "id": 25,
        "name": "Fresh Veg Salad",
        "category": "Healthy",
        "price": 119,
        "emoji": "🥗",
        "description": "Fresh vegetables served with a light and refreshing dressing.",
        "rating": 4.5,
        "time": "10-15 min"
    },

    {
        "id": 26,
        "name": "Grilled Chicken Bowl",
        "category": "Healthy",
        "price": 229,
        "emoji": "🥗",
        "description": "Grilled chicken with vegetables and nutritious rice.",
        "rating": 4.8,
        "time": "20-25 min"
    },


    # ---------------- DESSERTS ----------------

    {
        "id": 27,
        "name": "Chocolate Brownie",
        "category": "Desserts",
        "price": 89,
        "emoji": "🍫",
        "description": "Soft and rich chocolate brownie for a perfect sweet ending.",
        "rating": 4.9,
        "time": "10-15 min"
    },

    {
        "id": 28,
        "name": "Gulab Jamun",
        "category": "Desserts",
        "price": 79,
        "emoji": "🍩",
        "description": "Soft sweet dumplings soaked in delicious sugar syrup.",
        "rating": 4.8,
        "time": "10-15 min"
    },

    {
        "id": 29,
        "name": "Choco Lava Cake",
        "category": "Desserts",
        "price": 129,
        "emoji": "🍰",
        "description": "Warm chocolate cake with a rich molten chocolate center.",
        "rating": 4.9,
        "time": "15-20 min"
    },


    # ---------------- DRINKS ----------------

    {
        "id": 30,
        "name": "Fresh Mango Shake",
        "category": "Drinks",
        "price": 79,
        "emoji": "🥭",
        "description": "Refreshing mango shake made with fresh mangoes.",
        "rating": 4.8,
        "time": "10-15 min"
    },

    {
        "id": 31,
        "name": "Cold Coffee",
        "category": "Drinks",
        "price": 109,
        "emoji": "☕",
        "description": "Chilled creamy coffee topped with a smooth foam layer.",
        "rating": 4.7,
        "time": "10-15 min"
    },

    {
        "id": 32,
        "name": "Fresh Lime Soda",
        "category": "Drinks",
        "price": 69,
        "emoji": "🥤",
        "description": "Refreshing sparkling lime drink with a zesty flavor.",
        "rating": 4.6,
        "time": "5-10 min"
    }
]


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template(
        "index.html",
        foods=FOODS,
        app_name=APP_NAME
    )


# =========================================================
# FOOD API
# =========================================================

@app.route("/api/foods")
def get_foods():
    return jsonify(FOODS)


# =========================================================
# AI API
# =========================================================

@app.route("/api/ai", methods=["POST"])
def ai_chat():

    try:

        if client is None:
            return jsonify({
                "response": (
                    "⚠️ Gemini API is not configured. "
                    "Please check your .env file."
                )
            }), 500

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "response": "Invalid request."
            }), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "response": "Please enter a question."
            }), 400

        menu_text = "\n".join(
            [
                f"{food['name']} | "
                f"Category: {food['category']} | "
                f"Price: ₹{food['price']} | "
                f"Rating: {food['rating']} | "
                f"Delivery: {food['time']}"
                for food in FOODS
            ]
        )

        prompt = f"""
ZESTORA MENU:

{menu_text}

CUSTOMER QUESTION:

{user_message}

Answer the customer using the Zestora menu.
Do not recommend items that are not in the menu.
"""

        print("🤖 Sending request to Gemini...")

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=500
            )
        )

        answer = response.text

        if not answer:
            return jsonify({
                "response": "Sorry, I couldn't generate a response."
            }), 500

        print("✅ Gemini response received.")

        return jsonify({
            "response": answer
        })

    except Exception as error:

        print("\n" + "=" * 60)
        print("❌ GEMINI ERROR")
        print("=" * 60)
        print(type(error).__name__)
        print(str(error))
        print("=" * 60 + "\n")

        return jsonify({
            "response": (
                "⚠️ Zestora AI is temporarily unavailable. "
                "Please try again."
            )
        }), 500


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Page not found"
    }), 404


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )