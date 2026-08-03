from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    output_filename = "downloaded_video.mp4"
    
    try:
        # ইউটিউব এবং ফেসবুক উভয়টির জন্য ব্রাউজার ইউজার-এজেন্ট সহ কমান্ড
        command = [
            'yt-dlp',
            '--no-check-certificates',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '-f', 'best[ext=mp4]/best',
            '-o', output_filename,
            video_url
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        if os.path.exists(output_filename):
            response = send_file(output_filename, as_attachment=True)
            return response
        else:
            return jsonify({"status": "error", "message": "File could not be downloaded"}), 500

    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() if e.stderr else str(e)
        return jsonify({"status": "error", "message": f"yt-dlp error: {error_output}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)