from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def get_video_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        # সার্ভারে ফাইল ডাউনলোড না করে শুধু ডিরেক্ট স্ট্রিম লিংক বের করার কমান্ড
        command = [
            'yt-dlp', 
            '--no-check-certificates',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '-f', 'best[ext=mp4]/best', 
            '-g', 
            video_url
        ]
        
        # timeout যোগ করা হয়েছে যাতে সার্ভার ফ্রিজ হয়ে ক্র্যাশ না করে
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=15)
        
        links = result.stdout.strip().split('\n')
        if not links or not links[0]:
            return jsonify({"status": "error", "message": "Could not extract video link"}), 500
            
        direct_link = links[0] 
        
        return jsonify({
            "status": "success",
            "download_url": direct_link
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Request timed out"}), 500
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() if e.stderr else str(e)
        return jsonify({"status": "error", "message": f"yt-dlp error: {error_output}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)