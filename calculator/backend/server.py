from flask import Flask, request, jsonify
from flask_cors import CORS
from calculation import calculate_expression

app = Flask(__name__)
CORS(app)

@app.route("/calculate", methods=["POST"])

def calculate():
    data = request.get_json()
    print(data)
    equation = data.get("equation", "")
    print("data", equation)
    try:
        print("trying")
        print(equation)
        normal_result, nn_result, tree_dump, layers = calculate_expression(equation)

        # layers = list(layers)
        
        return jsonify({
            "normal_result": normal_result,
            "nn_result": nn_result,
            "tree_structure": tree_dump,
            "layers": layers
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 