from flask import Flask, request
import requests
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Telegram bot token
TOKEN = '5595298904:AAExEMcbyKGA3cBdIECmFB-AD55Zx8L0uOM'
# JioSaavn API base URL
JIOSAAVN_API_BASE_URL = 'https://semantic-genni-sathishskinsta.koyeb.app/'

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return 'Bot is running and healthy!'

def download_media(song_id, quality='128kbps', output_format='mp3'):
    try:
        # Construct the API endpoint URL
        api_url = f"{JIOSAAVN_API_BASE_URL}api.php?id={song_id}&quality={quality}"

        # Send a GET request to download the media file with the specified quality
        with requests.get(api_url, timeout=10) as response:
            response.raise_for_status()
            response_json = response.json()

        # Check if the response has required data
        if 'media_url' in response_json and 'thumbnail' in response_json:
            # Save the content (media file) to a temporary file
            temp_file_path = f'downloaded_media_temp.{output_format}'
            with open(temp_file_path, 'wb') as f:
                f.write(requests.get(response_json['media_url']).content)

            # Save the thumbnail image
            thumbnail_url = response_json['thumbnail']
            thumbnail_file_path = f'song_thumbnail.jpg'
            with open(thumbnail_file_path, 'wb') as f:
                f.write(requests.get(thumbnail_url).content)

            # Convert the media file to the desired output format using FFmpeg
            output_file_path = f'downloaded_media_{quality}.{output_format}'
            subprocess.run(['ffmpeg', '-i', temp_file_path, '-i', thumbnail_file_path, '-c', 'copy', output_file_path])

            # Remove the temporary files
            subprocess.run(['rm', temp_file_path])
            subprocess.run(['rm', thumbnail_file_path])

            return f'Media file downloaded successfully with {quality} quality as {output_format}.'

        else:
            return 'Failed to download media file or response does not contain required data.'

    except requests.RequestException as e:
        return f"Error: {e}"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Media Downloader Bot! Send me the JioSaavn song ID to download.')

def download(update: Update, context: CallbackContext) -> None:
    song_id = update.message.text
    response_message = download_media(song_id)
    update.message.reply_text(response_message)

def quality(update: Update, context: CallbackContext) -> None:
    quality_option = context.args[0].lower()
    if quality_option in ('128kbps', '320kbps'):
        song_id = context.args[1]
        response_message = download_media(song_id, quality=quality_option)
        update.message.reply_text(response_message)
    else:
        update.message.reply_text('Invalid quality option. Please choose either 128kbps or 320kbps.')

def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('download', download))
    updater.dispatcher.add_handler(CommandHandler('quality', quality, pass_args=True))

    updater.start_polling()

    # Run Flask app in the background
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
