from flask import Flask, request, jsonify
from flask_cors import CORS
import calculator

app = Flask(__name__)
CORS(app)

@app.route("/calculate", methods=["POST"])

def calculate():
    data = request.get_json()
    print(data)
    equation = data.get("equation", "")

    try:
        result = calculator.func()

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 