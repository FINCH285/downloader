import os
import threading
import requests
import schedule
import time
from pytube import YouTube
from youtube_dl import YoutubeDL
from flask import Flask, request, jsonify

app = Flask(__name__)

class Downloader:
    def __init__(self):
        self.downloads = []

    def download_video(self, url, output_path, format='mp4', quality='highest'):
        ydl_opts = {
            'format': 'best' if quality == 'highest' else 'worst',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def batch_download(self, urls, output_path, format='mp4', quality='highest'):
        for url in urls:
            self.download_video(url, output_path, format, quality)

    def schedule_download(self, url, output_path, format='mp4', quality='highest', time_to_download='00:00'):
        schedule.every().day.at(time_to_download).do(self.download_video, url, output_path, format, quality)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def resume_download(self, url, output_path, format='mp4', quality='highest'):
        self.download_video(url, output_path, format, quality)

    def download_multiple_files(self, urls, output_path, format='mp4', quality='highest'):
        threads = []
        for url in urls:
            thread = threading.Thread(target=self.download_video, args=(url, output_path, format, quality))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

downloader = Downloader()

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    output_path = data.get('output_path', '.')
    format = data.get('format', 'mp4')
    quality = data.get('quality', 'highest')
    downloader.download_video(url, output_path, format, quality)
    return jsonify({'message': 'Download started'})

@app.route('/batch_download', methods=['POST'])
def batch_download():
    data = request.get_json()
    urls = data.get('urls')
    output_path = data.get('output_path', '.')
    format = data.get('format', 'mp4')
    quality = data.get('quality', 'highest')
    downloader.batch_download(urls, output_path, format, quality)
    return jsonify({'message': 'Batch download started'})

@app.route('/schedule_download', methods=['POST'])
def schedule_download():
    data = request.get_json()
    url = data.get('url')
    output_path = data.get('output_path', '.')
    format = data.get('format', 'mp4')
    quality = data.get('quality', 'highest')
    time_to_download = data.get('time_to_download', '00:00')
    threading.Thread(target=downloader.schedule_download, args=(url, output_path, format, quality, time_to_download)).start()
    return jsonify({'message': 'Download scheduled'})

@app.route('/resume_download', methods=['POST'])
def resume_download():
    data = request.get_json()
    url = data.get('url')
    output_path = data.get('output_path', '.')
    format = data.get('format', 'mp4')
    quality = data.get('quality', 'highest')
    downloader.resume_download(url, output_path, format, quality)
    return jsonify({'message': 'Download resumed'})

@app.route('/download_multiple_files', methods=['POST'])
def download_multiple_files():
    data = request.get_json()
    urls = data.get('urls')
    output_path = data.get('output_path', '.')
    format = data.get('format', 'mp4')
    quality = data.get('quality', 'highest')
    downloader.download_multiple_files(urls, output_path, format, quality)
    return jsonify({'message': 'Multiple file download started'})

if __name__ == '__main__':
    app.run(debug=True)
