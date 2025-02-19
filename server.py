from flask import Flask, request, jsonify
from chatbot import handle_user_query

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("Received data:", data)  # Ajout pour voir ce que Flask reçoit
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request"}), 400

        user_input = data["message"]
        user_phone = "test_user"
        response = handle_user_query(user_input, user_phone)

        return jsonify({"response": response})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
