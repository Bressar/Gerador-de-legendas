import customtkinter as ctk
from tkinter import filedialog
import threading
from docx import Document

#  . .\.venv\Scripts\Activate.ps1


def processar_video_local(caminho_video_local, nome_srt="legenda.srt"):
    try:
        print("🎵 Extraindo áudio de arquivo local...")
        criar_pasta_temp()
        # Copia o vídeo para a pasta temporária
        video_destino = os.path.join(TEMP_DIR, "video_local.mp4")
        shutil.copy(caminho_video_local, video_destino)
        audio_path = extrair_audio(video_destino)
        print("🧠 Transcrevendo com Whisper...")
        resultado = transcrever(audio_path)
        print("💾 Salvando legenda .srt...")
        salvar_como_srt(resultado, nome_srt)
        print(f"✅ Legenda salva em: {nome_srt}")
    finally:
        print("🧹 Limpando arquivos temporários...")
        limpar_temp()


# Atualizar para usar saída como .txt ou .docx
def salvar_texto(resultado, nome_arquivo, formato):
    if formato == "srt":
        salvar_como_srt(resultado, nome_arquivo)
    elif formato == "txt":
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            for seg in resultado['segments']:
                f.write(f"[{formatar_tempo(seg['start'])}] {seg['text'].strip()}\n")
    elif formato == "docx":
        doc = Document()
        for seg in resultado['segments']:
            doc.add_paragraph(f"[{formatar_tempo(seg['start'])}] {seg['text'].strip()}")
        doc.save(nome_arquivo)

def processar(video_path, tipo, formato_saida):
    try:
        criar_pasta_temp()
        if tipo == "youtube":
            video_path = baixar_video(video_path)
        elif tipo == "local":
            novo_path = os.path.join(TEMP_DIR, "video_local.mp4")
            shutil.copy(video_path, novo_path)
            video_path = novo_path

        audio_path = extrair_audio(video_path)
        resultado = transcrever(audio_path)

        ext = formato_saida
        nome_saida = f"legenda.{ext}"
        salvar_texto(resultado, nome_saida, ext)
        status.configure(text=f"✅ Arquivo salvo: {nome_saida}")
    except Exception as e:
        status.configure(text=f"Erro: {e}")
    finally:
        limpar_temp()

# --- Interface com customtkinter ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Transcrição de Vídeo com Whisper")
janela.geometry("500x350")

tipo_entrada = ctk.StringVar(value="youtube")
formato_saida = ctk.StringVar(value="srt")
caminho_arquivo = ctk.StringVar()

def escolher_arquivo():
    path = filedialog.askopenfilename(filetypes=[("Vídeo", "*.mp4 *.mkv *.avi")])
    if path:
        caminho_arquivo.set(path)

def iniciar():
    video_input = caminho_arquivo.get()
    tipo = tipo_entrada.get()
    formato = formato_saida.get()

    if not video_input:
        status.configure(text="⚠️ Selecione um link ou arquivo.")
        return

    threading.Thread(target=processar, args=(video_input, tipo, formato)).start()
    status.configure(text="🔁 Processando...")

# Widgets
ctk.CTkLabel(janela, text="Escolha a origem do vídeo:").pack(pady=5)
ctk.CTkRadioButton(janela, text="YouTube", variable=tipo_entrada, value="youtube").pack()
ctk.CTkRadioButton(janela, text="Arquivo Local", variable=tipo_entrada, value="local").pack()

ctk.CTkEntry(janela, textvariable=caminho_arquivo, width=400).pack(pady=5)
ctk.CTkButton(janela, text="Selecionar Arquivo (se for local)", command=escolher_arquivo).pack(pady=5)

ctk.CTkLabel(janela, text="Formato de saída:").pack(pady=5)
ctk.CTkOptionMenu(janela, values=["srt", "txt", "docx"], variable=formato_saida).pack()

ctk.CTkButton(janela, text="Iniciar Transcrição", command=iniciar).pack(pady=20)
status = ctk.CTkLabel(janela, text="")
status.pack()

janela.mainloop()
