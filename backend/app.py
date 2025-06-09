from flask import Flask, request, jsonify
from balancer import parse_equation
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/balance', methods=['POST'])
def balance():
    data = request.get_json()
    equation = data.get('equation')
    race = data.get('race', False)
    if not equation:
        return jsonify({'error': 'equation is required'}), 400
    og, matrix, balanced, el_info, runtime, coeffs = parse_equation(equation, race)

    response = {
        'original': og,
        'matrix': matrix,
        'balanced': balanced,
        'element_info': el_info,
        'time': runtime,
        'coefficients': coeffs
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()
