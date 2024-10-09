from flask import Flask, render_template, request, jsonify
from downloader import Downloader

app = Flask(__name__)
downloader = Downloader()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    output_path = request.form.get('output_path', '.')
    format = request.form.get('format', 'mp4')
    quality = request.form.get('quality', 'highest')
    downloader.download_video(url, output_path, format, quality)
    return jsonify({'message': 'Download started'})

@app.route('/batch_download', methods=['POST'])
def batch_download():
    urls = request.form.getlist('urls')
    output_path = request.form.get('output_path', '.')
    format = request.form.get('format', 'mp4')
    quality = request.form.get('quality', 'highest')
    downloader.batch_download(urls, output_path, format, quality)
    return jsonify({'message': 'Batch download started'})

@app.route('/schedule_download', methods=['POST'])
def schedule_download():
    url = request.form.get('url')
    output_path = request.form.get('output_path', '.')
    format = request.form.get('format', 'mp4')
    quality = request.form.get('quality', 'highest')
    time_to_download = request.form.get('time_to_download', '00:00')
    downloader.schedule_download(url, output_path, format, quality, time_to_download)
    return jsonify({'message': 'Download scheduled'})

@app.route('/resume_download', methods=['POST'])
def resume_download():
    url = request.form.get('url')
    output_path = request.form.get('output_path', '.')
    format = request.form.get('format', 'mp4')
    quality = request.form.get('quality', 'highest')
    downloader.resume_download(url, output_path, format, quality)
    return jsonify({'message': 'Download resumed'})

@app.route('/download_multiple_files', methods=['POST'])
def download_multiple_files():
    urls = request.form.getlist('urls')
    output_path = request.form.get('output_path', '.')
    format = request.form.get('format', 'mp4')
    quality = request.form.get('quality', 'highest')
    downloader.download_multiple_files(urls, output_path, format, quality)
    return jsonify({'message': 'Multiple file download started'})

if __name__ == '__main__':
    app.run(debug=True)
