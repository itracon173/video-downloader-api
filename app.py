from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def get_video_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # এখানে -f দিয়ে ভিডিও এবং অডিও একসাথে কম্বাইন করার ফরম্যাট বলে দেওয়া হয়েছে
        # এবং -g এর মাধ্যমে ডিরেক্ট স্ট্রিম লিংক ফেচ করা হচ্ছে
        command = [
            'yt-dlp', 
            '-f', 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]', 
            '-g', 
            video_url
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # yt-dlp কখনো কখনো ভিডিও ও অডিওর আলাদা দুটি লিংক দেয় (প্রথমটা ভিডিও, দ্বিতীয়টা অডিও)
        # তবে ক্লাউড সার্ভারে ffmpeg না থাকলে মার্জ করা সম্ভব হয় না। 
        # তাই সরাসরি সেরা সিঙ্গেল ফাইল বা কম্বাইন্ড লিংক নেওয়ার জন্য নিচে হ্যান্ডেল করা হলো:
        links = result.stdout.strip().split('\n')
        direct_link = links[0] # প্রাইমারি লিংক
        
        return jsonify({
            "status": "success",
            "download_url": direct_link
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)