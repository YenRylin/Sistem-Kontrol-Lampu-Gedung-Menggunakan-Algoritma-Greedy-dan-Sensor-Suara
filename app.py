from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

# Lampu dan daya
lamp_states = {
    "gedung5": False,
    "gedung7": False,
    "gedung8": False,
    "gedung9": False,
    "kantin": False,
    "asrama": False
}

lamp_power = {
    "gedung5": 100,
    "gedung7": 200,
    "gedung8": 300,
    "gedung9": 400,
    "kantin": 500,
    "asrama": 600
}

total_power_capacity = 1000
current_power_usage = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice-command', methods=['POST'])
def voice_command():
    global current_power_usage
    data = request.json
    command = data.get('command', '').lower()
    response_message = ""

    for building in lamp_states.keys():
        if building in command:
            if lamp_states[building]:
                lamp_states[building] = False
                current_power_usage -= lamp_power[building]
            else:
                if current_power_usage + lamp_power[building] <= total_power_capacity:
                    lamp_states[building] = True
                    current_power_usage += lamp_power[building]
                else:
                    response_message = f"Daya tidak cukup untuk {building}!"

    if "matikan semua lampu" in command:
        for building in lamp_states.keys():
            if lamp_states[building]:
                current_power_usage -= lamp_power[building]
            lamp_states[building] = False
        response_message = "Semua lampu dimatikan."

    return jsonify({
        "lamp_states": lamp_states,
        "current_power_usage": current_power_usage,
        "message": response_message
    })

if __name__ == '__main__':
    app.run(debug=True)
