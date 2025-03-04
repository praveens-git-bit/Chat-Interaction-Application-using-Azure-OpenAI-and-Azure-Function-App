import json
import requests
from flask import Flask, request, jsonify, render_template

# Load settings from appsettings.json
try:
    with open("appsettings.json", "r") as config_file:
        config = json.load(config_file)

    FUNCTION_URL = config.get("FUNCTION_URL")


    if not FUNCTION_URL:
        raise ValueError("FUNCTION_URL is missing in appsettings.json")

except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading configuration: {str(e)}")
    exit(1)  # Stop execution if config is invalid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Render UI

@app.route("/chat", methods=["POST"])  # Changed to "/chat"
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        user_input = data.get("message")

        if not user_input.strip():
            return jsonify({"response": "Message cannot be empty."}), 400

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            FUNCTION_URL,
            json={"message": user_input},
            headers=headers,
        )

        # Handle response errors
        if response.status_code != 200:
            print("Function App Error:", response.text)  # Debugging Log
            return jsonify({"error": "API call failed", "details": response.text}), response.status_code

        return jsonify(response.json())

    except requests.RequestException as req_err:
        print("Request Error:", req_err)
        return jsonify({"error": "Failed to reach API", "details": str(req_err)}), 500

    except Exception as e:
        print("Unexpected Error:", e)
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
