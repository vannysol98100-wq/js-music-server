from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOADS_FOLDER = "downloads"
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"


def gerar_nome():
    return str(uuid.uuid4())


@app.route("/api/mp3")
def baixar_mp3():
    url = request.args.get("url")
    if not url:
        return "URL não encontrada", 400

    nome = gerar_nome()
    caminho_saida = f"{DOWNLOADS_FOLDER}/{nome}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{DOWNLOADS_FOLDER}/{nome}.%(ext)s",
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
        'ffmpeg_location': FFMPEG_PATH,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(caminho_saida, as_attachment=True)


@app.route("/api/mp4")
def baixar_mp4():
    url = request.args.get("url")
    if not url:
        return "URL não encontrada", 400

    nome = gerar_nome()
    caminho_saida = f"{DOWNLOADS_FOLDER}/{nome}.mp4"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f"{DOWNLOADS_FOLDER}/{nome}.%(ext)s",
        'merge_output_format': 'mp4',
        'ffmpeg_location': FFMPEG_PATH,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    arquivos = os.listdir(DOWNLOADS_FOLDER)
    for arquivo in arquivos:
        if arquivo.startswith(nome) and arquivo.endswith(".mp4"):
            return send_file(f"{DOWNLOADS_FOLDER}/{arquivo}", as_attachment=True)

    return "Erro ao processar vídeo", 500


@app.route("/")
def home():
    return "Servidor JS-MUSIC Online ✅"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
