# Gerador de legendas para videos e filmes
# Arquivo de backend
# Criado em: 19/06/2025
# Modificado em: 
# By: Douglas G. Bressar

# pip install -r requirements.txt


import os
import shutil
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

#import moviepy.editor as mp
import whisper
from docx import Document

TEMP_DIR = "Temp"

class Backend:
    def criar_pasta_temp(self):
        os.makedirs(TEMP_DIR, exist_ok=True)

    def limpar_temp(self):
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

    def baixar_video(self, url):
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        caminho = os.path.join(TEMP_DIR, "video.mp4")
        stream.download(output_path=TEMP_DIR, filename="video.mp4")
        return caminho

    def extrair_audio(self, caminho_video):
        video = VideoFileClip(caminho_video)
        audio_path = os.path.join(TEMP_DIR, "audio.wav")
        video.audio.write_audiofile(audio_path)
        return audio_path

    def transcrever(self, caminho_audio):
        modelo = whisper.load_model("base")
        return modelo.transcribe(caminho_audio, verbose=True)

    def formatar_tempo(self, segundos):
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segs = int(segundos % 60)
        return f"{horas:02}:{minutos:02}:{segs:02}"

    def salvar_texto(self, resultado, nome_arquivo, formato):
        if formato == "srt":
            self.salvar_como_srt(resultado, nome_arquivo)
        elif formato == "txt":
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                for seg in resultado['segments']:
                    f.write(f"[{self.formatar_tempo(seg['start'])}] {seg['text'].strip()}\n")
        elif formato == "docx":
            doc = Document()
            for seg in resultado['segments']:
                doc.add_paragraph(f"[{self.formatar_tempo(seg['start'])}] {seg['text'].strip()}")
            doc.save(nome_arquivo)

    def salvar_como_srt(self, resultado, nome_arquivo):
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(resultado['segments'], start=1):
                inicio = self.formatar_tempo(seg['start'])
                fim = self.formatar_tempo(seg['end'])
                texto = seg['text'].strip()
                f.write(f"{i}\n{inicio} --> {fim}\n{texto}\n\n")
