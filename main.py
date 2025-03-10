import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # เปิดใช้งาน CORS ให้ API ใช้งานข้ามโดเมนได้

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({"error": "No video ID provided"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t["text"] for t in transcript])
        return jsonify({"transcript": transcript_text})

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ใช้ PORT ที่ Railway กำหนด
    app.run(host='0.0.0.0', port=port)
