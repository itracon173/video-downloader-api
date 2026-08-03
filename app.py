from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def get_video_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        # ইউটিউব এবং ফেসবুক উভয়ের জন্য ডিরেক্ট লিংকের বদলে সবচেয়ে সহজ ফরম্যাট
        command = [
            'yt-dlp', 
            '--no-check-certificates',
            '-f', '18/best[ext=mp4]/best',  # Format 18 হলো ইউটিউবের জন্য গ্যারান্টিড অডিও-ভিডিও যুক্ত 360p এমপিফোর ফাইল
            '-g', 
            video_url
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        links = result.stdout.strip().split('\n')
        if not links or not links[0]:
            return jsonify({"status": "error", "message": "Could not extract video link"}), 500
            
        direct_link = links[0] 
        
        return jsonify({
            "status": "success",
            "download_url": direct_link
        })
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() if e.stderr else str(e)
        return jsonify({"status": "error", "message": f"yt-dlp error: {error_output}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)