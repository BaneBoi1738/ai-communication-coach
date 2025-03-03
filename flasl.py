from flask import Flask, request, jsonify
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handles chat with AI"""
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    response = f"AI Response: {prompt}"  
    return jsonify({'response': response})

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Handles speech-to-text conversion (Dummy response)"""
    return jsonify({'transcription': 'This is a sample transcription'})  

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Handles text-to-speech conversion (Dummy response)"""
    return jsonify({'audio_base64': 'BASE64_AUDIO_DATA'})  

@app.route('/api/train-skill', methods=['POST'])
def train_skill():
    """Handles skill training activities"""
    data = request.json
    activity = data.get('activity', '').strip().lower()  

    if not activity:
        return jsonify({'error': 'No activity provided'}), 400

    # Empty dictionary for prompts to be inserted later
    exercises = {
        "storytelling": "",  
        "conflict resolution": "",  
        "presentation assessment": "",  
        "impromptu speaking": ""  
    }

    if activity in exercises:
        return jsonify({'exercise': exercises[activity]})
    
    return jsonify({'error': 'Activity not recognized. Choose from Storytelling, Conflict Resolution, Presentation Assessment, or Impromptu Speaking.'}), 400

@app.route('/api/assess-presentation', methods=['POST'])
def assess_presentation():
    """Handles AI feedback for presentation assessments"""
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No presentation text provided'}), 400
    feedback = f"AI feedback on your presentation: {text}"
    return jsonify({'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True, port=5050, host='0.0.0.0') 