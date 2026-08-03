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
        # সার্ভারে ফাইল সরাসরি ডাউনলোড করার কমান্ড (ইউটিউব এবং ফেসবুক উভয়ের জন্য)
        command = [
            'yt-dlp',
            '--no-check-certificates',
            '-f', 'best[ext=mp4]/best',
            '-o', output_filename,
            video_url
        ]
        
        # প্রসেস রান করা
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        if os.path.exists(output_filename):
            # ফাইল সফলভাবে ডাউনলোড হলে ইউজারের কাছে পাঠিয়ে দেওয়া এবং পাঠানো শেষ হলে মুছে ফেলা
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