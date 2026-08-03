from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def get_video_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    # নিশ্চিত করা যে লিংকটি ইউটিউবের কি না
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        return jsonify({"status": "error", "message": "Only YouTube links are supported!"}), 400

    try:
        # ইউটিউবের বট ব্লক এড়ানোর জন্য পোটেনশিয়াল ফ্ল্যাগ ও মোবাইল ক্লায়েন্ট বাইপাস
        command = [
            'yt-dlp', 
            '--no-check-certificates',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--extractor-args', 'youtube:player_client=android',  # অ্যান্ড্রয়েড ক্লায়েন্ট সিমুলেট করে ব্লক এড়াতে সাহায্য করে
            '-f', '18/best[ext=mp4]/best',                      # গ্যারান্টিড অডিও-ভিডিও যুক্ত ফরম্যাট
            '-g', 
            video_url
        ]
        
        # সার্ভার যাতে ফ্রিজ না হয় সেজন্য timeout সহ রান করা
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=20)
        
        links = result.stdout.strip().split('\n')
        if not links or not links[0]:
            return jsonify({"status": "error", "message": "Could not extract YouTube link"}), 500
            
        direct_link = links[0] 
        
        return jsonify({
            "status": "success",
            "download_url": direct_link
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Request timed out while connecting to YouTube"}), 500
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() if e.stderr else str(e)
        return jsonify({"status": "error", "message": f"yt-dlp error: {error_output}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)