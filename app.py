# Gerador de legendas para videos e filmes
# Arquivo de testes interface
# Criado em: 19/06/2025
# Modificado em: 
# By: Douglas G. Bressar

import customtkinter as ctk
from tkinter import filedialog
import threading
from backend import Backend
import os

class AppGUI:
    def __init__(self):
        self.backend = Backend()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.janela = ctk.CTk()
        self.janela.title("Transcrição de Vídeo com Whisper")
        self.janela.geometry("500x350")

        self.tipo_entrada = ctk.StringVar(value="youtube")
        self.formato_saida = ctk.StringVar(value="srt")
        self.caminho_arquivo = ctk.StringVar()

        self.construir_interface()

    def construir_interface(self):
        ctk.CTkLabel(self.janela, text="Escolha a origem do vídeo:").pack(pady=5)
        ctk.CTkRadioButton(self.janela, text="YouTube", variable=self.tipo_entrada, value="youtube").pack()
        ctk.CTkRadioButton(self.janela, text="Arquivo Local", variable=self.tipo_entrada, value="local").pack()

        ctk.CTkEntry(self.janela, textvariable=self.caminho_arquivo, width=400).pack(pady=5)
        ctk.CTkButton(self.janela, text="Selecionar Arquivo (se for local)", command=self.escolher_arquivo).pack(pady=5)

        ctk.CTkLabel(self.janela, text="Formato de saída:").pack(pady=5)
        ctk.CTkOptionMenu(self.janela, values=["srt", "txt", "docx"], variable=self.formato_saida).pack()

        ctk.CTkButton(self.janela, text="Iniciar Transcrição", command=self.iniciar_thread).pack(pady=20)
        self.status = ctk.CTkLabel(self.janela, text="")
        self.status.pack()

        self.janela.mainloop()

    def escolher_arquivo(self):
        path = filedialog.askopenfilename(filetypes=[("Vídeo", "*.mp4 *.mkv *.avi")])
        if path:
            self.caminho_arquivo.set(path)

    def iniciar_thread(self):
        threading.Thread(target=self.iniciar_processo).start()
        self.status.configure(text="🔁 Processando...")

    def iniciar_processo(self):
        try:
            self.backend.criar_pasta_temp()
            tipo = self.tipo_entrada.get()
            formato = self.formato_saida.get()
            video_input = self.caminho_arquivo.get()

            if not video_input:
                self.status.configure(text="⚠️ Selecione um link ou arquivo.")
                return

            if tipo == "youtube":
                video_path = self.backend.baixar_video(video_input)
            else:
                video_path = os.path.join("Temp", "video_local.mp4")
                shutil.copy(video_input, video_path)

            audio_path = self.backend.extrair_audio(video_path)
            resultado = self.backend.transcrever(audio_path)

            nome_saida = f"legenda.{formato}"
            self.backend.salvar_texto(resultado, nome_saida, formato)
            self.status.configure(text=f"✅ Arquivo salvo: {nome_saida}")
        except Exception as e:
            self.status.configure(text=f"❌ Erro: {e}")
        finally:
            self.backend.limpar_temp()


if __name__ == "__main__":
    AppGUI()
