from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def get_video_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # yt-dlp কমান্ড দিয়ে সরাসরি ডিরেক্ট ভিডিও স্ট্রিম লিংক (mp4) বের করা
        # -g ফ্লাগটি শুধু মিডিয়া বা ভিডিওর ডিরেক্ট লিংক প্রিন্ট করে
        command = ['yt-dlp', '-g', video_url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        direct_link = result.stdout.strip().split('\n')[0] # হাই-কোয়ালিটি বা প্রথম লিংকটি নেওয়া
        
        return jsonify({
            "status": "success",
            "download_url": direct_link
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)