import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import yt_dlp

app = Flask(__name__)

# This folder will only exist temporarily inside the server memory
TEMP_DOWNLOAD_DIR = 'temp_downloads'
if not os.path.exists(TEMP_DOWNLOAD_DIR):
    os.makedirs(TEMP_DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format') # 'video' or 'audio'
    
    # Generate a unique filename to prevent users from overwriting each other
    unique_id = str(uuid.uuid4())[:8]
    
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'audio' else 'best',
        'outtmpl': f'{TEMP_DOWNLOAD_DIR}/raven_{unique_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # 🧹 CLEANUP LOGIC: This runs AFTER the user receives the file
        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                app.logger.error(f"Error deleting temp file: {e}")
            return response

        # 🚀 THE MAGIC: This sends the file to the user's browser, not your phone
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # '0.0.0.0' is required for Cloud hosting (Render/Railway)
    app.run(host='0.0.0.0', port=5000)