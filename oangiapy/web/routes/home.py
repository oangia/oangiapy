from flask import Blueprint, render_template
from ...database.firebase import Firebase
from ...database.mongodb import MongoDB
home_bp = Blueprint("home", __name__)

@home_bp.route("/") 
def index():
    #firebase_db = Firebase("agent52-firebase-adminsdk-fbsvc-913162cdf2.json")
    #firebase_db.create("users", {"name": "Alice"})
    #mongo_db = MongoDB("mongodb+srv://hqnhatdn:XiSgrN0lRLq4A8ch@cluster0.wnkrqan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", "mydb")
    #mongo_db.create("users", {"name": "Bob"})
    return render_template('index.html', card_name="1s")
