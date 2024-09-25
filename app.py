from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle video download
@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('videoLink')

    if not video_url:
        return "Error: No video URL provided", 400

    print(f"Received URL: {video_url}")

    try:
        # Set options for yt-dlp
        ydl_opts = {
            'format': 'bestvideo/best',  # Select the best quality video
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        return send_file(
            filename,
            as_attachment=True,
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    app.run(debug=True, host="0.0.0.0")
