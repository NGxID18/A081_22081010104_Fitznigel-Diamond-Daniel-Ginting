from flask import Flask, request, jsonify

app = Flask(__name__)

# Variabel untuk menyimpan suhu
current_temperature = None


@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    global current_temperature
    print(f"Received request: Method={request.method}, Args={request.args}")  # Debugging

    if request.method == 'GET':
        temp = request.args.get('temperature')
        if temp is not None:
            # ESP32 mengirim data suhu
            try:
                current_temperature = float(temp)
                return jsonify({"success": True, "temperature": current_temperature}), 200
            except ValueError:
                return jsonify({"error": "Invalid temperature value"}), 400
        else:
            # Bot Telegram meminta data suhu
            if current_temperature is not None:
                return jsonify({"temperature": current_temperature}), 200
            else:
                return jsonify({"error": "No temperature data available"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
