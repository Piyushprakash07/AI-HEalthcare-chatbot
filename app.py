from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyC_rgNU2NeN-aRBVZhc-3sxtP-2wFGAyXo"  
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_gemini_response(user_input):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }
    
    response = requests.post(f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}", json=data, headers=headers)
    print("Response Status Code:", response.status_code)  # Debugging
    print("Response JSON:", response.json())  # Debugging
    
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    
    return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't understand that.")
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    bot_response = get_gemini_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)