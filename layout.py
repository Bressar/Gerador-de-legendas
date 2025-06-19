# Gerador de legendas para videos e filmes
# Arquivo de testes
# Criado em: 19/06/2025
# Modificado em: 
# By: Douglas G. Bressar

from moviepy.video.io.VideoFileClip import VideoFileClip as mp
from moviepy.audio.io.AudioFileClip import AudioFileClip


def teste_extrair_audio(video_path, audio_saida):
    try:
        clip = mp.VideoFileClip(video_path)
        print(f"Duração do vídeo: {clip.duration:.2f} segundos")
        audio = clip.audio
        if audio is None:
            print("Não foi possível extrair áudio deste vídeo.")
        else:
            audio.write_audiofile(audio_saida)
            print(f"Áudio extraído salvo em: {audio_saida}")
        clip.close()
    except Exception as e:
        print(f"Erro ao processar vídeo: {e}")

if __name__ == "__main__":
    video_teste = input("Caminho do vídeo para teste (ex: video.mp4): ")
    audio_saida = "audio_extraido.wav"
    teste_extrair_audio(video_teste, audio_saida)
