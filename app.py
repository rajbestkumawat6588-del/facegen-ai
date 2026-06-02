import os
import time
import base64
import requests
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max upload

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64_url(file_bytes, content_type="image/jpeg"):
    b64 = base64.b64encode(file_bytes).decode('utf-8')
    return f"data:{content_type};base64,{b64}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not REPLICATE_API_TOKEN:
        return jsonify({"error": "REPLICATE_API_TOKEN set nahi hai. .env file mein add karein."}), 400

    if 'photo' not in request.files:
        return jsonify({"error": "Photo upload karein"}), 400

    file = request.files['photo']
    prompt = request.form.get('prompt', '').strip()

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Valid image file upload karein (JPG, PNG, WEBP)"}), 400

    if not prompt:
        return jsonify({"error": "Prompt likhein"}), 400

    try:
        file_bytes = file.read()
        content_type = file.content_type or "image/jpeg"
        face_image_b64 = image_to_base64_url(file_bytes, content_type)

        # InstantID model on Replicate - preserves face perfectly
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "version": "7efc04c9c4e5df9c6d48e3e9b95ee6c5ca13a756",  # InstantID
            "input": {
                "image": face_image_b64,
                "prompt": prompt,
                "negative_prompt": "deformed face, bad face, ugly, distorted, extra face, disfigured",
                "num_inference_steps": 30,
                "guidance_scale": 5.0,
                "ip_adapter_scale": 0.8,
                "controlnet_conditioning_scale": 0.8,
                "width": 640,
                "height": 640
            }
        }

        # Create prediction
        resp = requests.post(
            "https://api.replicate.com/v1/predictions",
            json=payload,
            headers=headers,
            timeout=30
        )

        if resp.status_code != 201:
            return jsonify({"error": f"Replicate API error: {resp.text}"}), 500

        prediction = resp.json()
        prediction_id = prediction.get("id")

        # Poll for result (max 3 minutes)
        for _ in range(36):
            time.sleep(5)
            poll = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=headers,
                timeout=15
            )
            result = poll.json()
            status = result.get("status")

            if status == "succeeded":
                output = result.get("output")
                image_url = output[0] if isinstance(output, list) else output
                return jsonify({"success": True, "image_url": image_url})

            elif status == "failed":
                error_msg = result.get("error", "Generation fail ho gayi")
                return jsonify({"error": error_msg}), 500

        return jsonify({"error": "Timeout — Replicate ne 3 minute mein response nahi diya"}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
