"""
Baixador universal de vídeos (YouTube, Instagram, TikTok, Facebook, Reddit, Vimeo, X/Twitter e outros)

Uso:
    python baixador_universal.py                    -> abre a interface gráfica
    python baixador_universal.py <link> [pasta]     -> baixa pelo terminal

Se o yt-dlp não estiver instalado, o programa instala sozinho.
Use apenas para conteúdo seu ou que você tenha permissão para baixar.
Sites com DRM (Netflix, Disney+, etc.) não são suportados.
"""
import shutil
import subprocess
import sys
import threading
from pathlib import Path

# Instala o yt-dlp no MESMO Python que está rodando o script
try:
    import yt_dlp
except ImportError:
    print("Instalando yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "yt-dlp"])
    import yt_dlp

TEM_FFMPEG = shutil.which("ffmpeg") is not None

QUALIDADES = ["Melhor qualidade", "Até 1080p", "Até 720p", "Até 480p", "Só áudio (MP3)"]


def formato_para(qualidade):
    """Retorna as opções de formato do yt-dlp conforme a qualidade escolhida."""
    if qualidade == "Só áudio (MP3)":
        return {"format": "bestaudio/best"}

    altura = {"Até 1080p": 1080, "Até 720p": 720, "Até 480p": 480}.get(qualidade)
    filtro = f"[height<={altura}]" if altura else ""

    if TEM_FFMPEG:
        # Com ffmpeg: junta o melhor vídeo + melhor áudio e entrega em mp4
        return {
            "format": f"bv*{filtro}+ba/b{filtro}",
            "merge_output_format": "mp4",
        }
    # Sem ffmpeg: usa só formatos que já vêm com áudio e vídeo juntos
    # (se nem isso existir, pega o melhor disponível, mesmo que venha sem áudio)
    return {"format": f"b{filtro}[ext=mp4]/b{filtro}/b/bv*{filtro}/bv*"}


def baixar(url, pasta, qualidade, playlist=False, ao_progredir=None, ao_status=None):
    """Baixa o vídeo e retorna o nome do arquivo (ou da pasta, se for playlist)."""
    url = url.strip()
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("Cole um link completo, começando com http:// ou https://")

    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    def hook(d):
        if d["status"] == "downloading" and ao_progredir:
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            if total:
                ao_progredir(d["downloaded_bytes"] / total * 100)
            if ao_status:
                vel = d.get("_speed_str", "").strip()
                eta = d.get("_eta_str", "").strip()
                ao_status(f"Baixando... {vel}  (faltam {eta})")
        elif d["status"] == "finished":
            if ao_progredir:
                ao_progredir(100)
            if ao_status:
                ao_status("Processando arquivo...")

    modelo = "%(playlist_title)s/%(title).80s [%(id)s].%(ext)s" if playlist else "%(title).80s [%(id)s].%(ext)s"
    opcoes = {
        **formato_para(qualidade),
        "outtmpl": str(pasta / modelo),
        "progress_hooks": [hook],
        "noplaylist": not playlist,
        "windowsfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "color": "never",  # tira os códigos de cor que apareciam na mensagem de erro
    }

    if qualidade == "Só áudio (MP3)" and TEM_FFMPEG:
        opcoes["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)
        if playlist and info.get("entries"):
            return str(pasta)
        arquivo = Path(ydl.prepare_filename(info))
        if qualidade == "Só áudio (MP3)" and TEM_FFMPEG:
            arquivo = arquivo.with_suffix(".mp3")
        return str(arquivo)


# ---------------------------- Interface gráfica ----------------------------
def abrir_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    janela = tk.Tk()
    janela.title("Baixador universal de vídeos")
    janela.geometry("600x330")
    janela.resizable(False, False)

    pasta_var = tk.StringVar(value=str(Path.home() / "Downloads"))
    qualidade_var = tk.StringVar(value=QUALIDADES[0])
    playlist_var = tk.BooleanVar(value=False)

    ttk.Label(janela, text="Link do vídeo:").pack(anchor="w", padx=15, pady=(15, 2))
    linha_url = ttk.Frame(janela)
    linha_url.pack(fill="x", padx=15)
    entrada = ttk.Entry(linha_url, width=72)
    entrada.pack(side="left")

    def colar():
        try:
            entrada.delete(0, "end")
            entrada.insert(0, janela.clipboard_get())
        except tk.TclError:
            pass

    ttk.Button(linha_url, text="Colar", width=7, command=colar).pack(side="left", padx=5)

    ttk.Label(janela, text="Salvar em:").pack(anchor="w", padx=15, pady=(10, 2))
    linha = ttk.Frame(janela)
    linha.pack(fill="x", padx=15)
    ttk.Entry(linha, textvariable=pasta_var, width=72).pack(side="left")
    ttk.Button(
        linha, text="...", width=7,
        command=lambda: pasta_var.set(filedialog.askdirectory() or pasta_var.get()),
    ).pack(side="left", padx=5)

    ttk.Label(janela, text="Qualidade:").pack(anchor="w", padx=15, pady=(10, 2))
    opcoes_frame = ttk.Frame(janela)
    opcoes_frame.pack(fill="x", padx=15)
    ttk.Combobox(
        opcoes_frame, textvariable=qualidade_var, values=QUALIDADES,
        state="readonly", width=24,
    ).pack(side="left")
    ttk.Checkbutton(
        opcoes_frame, text="Baixar playlist inteira", variable=playlist_var
    ).pack(side="left", padx=15)

    if not TEM_FFMPEG:
        ttk.Label(
            janela, foreground="#a60",
            text="ffmpeg não encontrado: limitado a formatos prontos; MP3 e 1080p+ podem não funcionar.",
        ).pack(anchor="w", padx=15, pady=(8, 0))

    barra = ttk.Progressbar(janela, length=570, maximum=100)
    barra.pack(padx=15, pady=(15, 5))
    status = ttk.Label(janela, text="Pronto.")
    status.pack(anchor="w", padx=15)

    botao = ttk.Button(janela, text="Baixar")
    botao.pack(pady=10)

    def set_barra(pct):
        janela.after(0, lambda: barra.config(value=pct))

    def set_status(txt):
        janela.after(0, lambda: status.config(text=txt))

    def trabalho(url):
        try:
            arquivo = baixar(
                url, pasta_var.get(), qualidade_var.get(),
                playlist_var.get(), set_barra, set_status,
            )
            set_status(f"Concluído: {Path(arquivo).name}")
        except Exception as e:
            erro = str(e)
            set_status("Erro.")
            janela.after(0, lambda: messagebox.showerror("Erro", erro))
        finally:
            janela.after(0, lambda: botao.config(state="normal"))

    def iniciar():
        url = entrada.get().strip()
        if not url:
            messagebox.showwarning("Atenção", "Cole o link do vídeo primeiro.")
            return
        botao.config(state="disabled")
        barra.config(value=0)
        status.config(text="Iniciando...")
        threading.Thread(target=trabalho, args=(url,), daemon=True).start()

    botao.config(command=iniciar)
    janela.mainloop()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        destino = sys.argv[2] if len(sys.argv) >= 3 else "downloads"
        try:
            print("Salvo em:", baixar(sys.argv[1], destino, QUALIDADES[0],
                                      ao_progredir=lambda p: print(f"\r{p:5.1f}%", end="")))
        except Exception as e:
            print("Erro:", e)
            sys.exit(1)
    else:
        abrir_gui()
