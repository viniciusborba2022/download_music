import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from youtubesearchpython import VideosSearch
import yt_dlp
import os
import re

# Configurar o diretório para salvar os arquivos MP3
output_dir = 'musicas_baixadas'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Função para limpar o título da música
def limpar_titulo(titulo):
    titulo = re.sub(r'[<>:"/\\|?*]', '', titulo)  # Remove caracteres inválidos
    titulo = re.sub(r'\s+', ' ', titulo)  # Substituir múltiplos espaços por um único
    return titulo.strip()  # Remove espaços em branco no início e no final

# Função para buscar o vídeo no YouTube
def buscar_video(query):
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()
    if result['result']:
        return result['result'][0]['link'], result['result'][0]['title']
    return None, None

# Função para baixar o áudio como MP3
def baixar_audio(video_url, nome_musica):
    nome_musica = limpar_titulo(nome_musica)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/{nome_musica}.mp3',  
        'ffmpeg_location': 'C:/ffmpeg/bin',  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Função chamada quando o usuário clica no botão de download pelo nome
def baixar_musica():
    musica = entry_musica.get()
    if not musica:
        messagebox.showwarning("Entrada Inválida", "Por favor, digite o nome da música.")
        return

    video_url, titulo_video = buscar_video(musica)

    if video_url:
        try:
            label_carregando.pack()
            janela_principal.update()

            baixar_audio(video_url, titulo_video)
            messagebox.showinfo("Download Completo", f"Download de '{titulo_video}' concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")
        finally:
            label_carregando.pack_forget()
    else:
        messagebox.showerror("Erro", f"Não foi possível encontrar um vídeo para: {musica}")

# Função chamada quando o usuário clica no botão de download pelo link
def baixar_por_link():
    link = entry_link.get()
    if not link:
        messagebox.showwarning("Entrada Inválida", "Por favor, cole o link do vídeo do YouTube.")
        return

    try:
        label_carregando.pack()
        janela_principal.update()

        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(link, download=False)
            titulo_video = info.get('title', 'Música do YouTube')

        baixar_audio(link, titulo_video)
        messagebox.showinfo("Download Completo", "Download concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")
    finally:
        label_carregando.pack_forget()

# Funções para abrir janelas de download
def janela_nome_musica():
    nova_janela = tk.Toplevel()
    nova_janela.title("Baixar Música pelo Nome")
    nova_janela.geometry("400x150+90+200")
    nova_janela.configure(bg="#f7f7f7")

    label_musica = tk.Label(nova_janela, text="Digite o nome da música que deseja baixar:", bg="#f7f7f7")
    label_musica.pack(pady=10)

    global entry_musica
    entry_musica = tk.Entry(nova_janela, width=40)
    entry_musica.pack(pady=5)

    botao_baixar_nome = tk.Button(nova_janela, text="Baixar", command=baixar_musica, bg="#28a745", fg="white", relief="flat", padx=10, pady=5)
    botao_baixar_nome.pack(pady=10)

def janela_link_musica():
    nova_janela = tk.Toplevel()
    nova_janela.title("Baixar Música pelo Link")
    nova_janela.geometry("400x150+90+390")
    nova_janela.configure(bg="#f7f7f7")

    label_link = tk.Label(nova_janela, text="Cole o link do vídeo do YouTube:", bg="#f7f7f7")
    label_link.pack(pady=10)

    global entry_link
    entry_link = tk.Entry(nova_janela, width=40)
    entry_link.pack(pady=5)

    botao_baixar_link = tk.Button(nova_janela, text="Baixar", command=baixar_por_link, bg="#28a745", fg="white", relief="flat", padx=10, pady=5)
    botao_baixar_link.pack(pady=10)

# Função para abrir uma janela com instruções
def janela_instrucoes():
    nova_janela = tk.Toplevel()
    nova_janela.title("Instruções")
    nova_janela.geometry("500x300+400+250")
    nova_janela.configure(bg="#f7f7f7")

    texto_instrucoes = """
    Baixar músicas do Youtube.
    
    - Clique em "Baixar pelo Nome" para buscar e baixar uma música digitando o nome. A busca é feita diretamente pelo youtube.
    - Se você tem o link de um vídeo do Youtube, clique em "Baixar pelo Link", em seguida cole no campo em branco e clique em baixar.
    - As músicas serão salvas na pasta 'musicas_baixadas' no formato MP3.
    
    As músicas serão salvas na pasta "musicas_baixadas"
    
    Esse programa foi feito com fins de adquirir conhecimento a respeito das bibliotecas e recursos do Python.
    """
    label_instrucoes = tk.Label(
        nova_janela, 
        text=texto_instrucoes, 
        bg="#f7f7f7", 
        wraplength=450, 
        justify="left"
    )
    label_instrucoes.pack(pady=10, padx=10)

    botao_fechar = tk.Button(
        nova_janela, 
        text="Fechar", 
        command=nova_janela.destroy, 
        bg="#d9534f", 
        fg="white", 
        relief="flat", 
        padx=10, 
        pady=5
    )
    botao_fechar.pack(pady=2)    

# Criar a janela principal
janela_principal = tk.Tk()
janela_principal.title("Baixar Músicas em mp3")
janela_principal.geometry("300x350+500+200")
janela_principal.configure(bg="#f7f7f7")

# Carregar a imagem e colocá-la no topo
imagem_caminho = "lutube.png"
imagem = PhotoImage(file=imagem_caminho)
label_imagem = tk.Label(janela_principal, image=imagem, bg="#f7f7f7")
label_imagem.pack(pady=10)

# Texto informativo abaixo da imagem
label_opcoes = tk.Label(janela_principal, text="Escolha uma opção abaixo, fonte: Youtube.", bg="#f7f7f7")
label_opcoes.pack(pady=10)

# Botões abaixo do texto informativo
botao_nome = tk.Button(janela_principal, text="Baixar pelo Nome", command=janela_nome_musica, bg="#007bff", fg="white", relief="flat", padx=10, pady=5)
botao_nome.pack(pady=5)

botao_link = tk.Button(janela_principal, text="Baixar pelo Link do Youtube", command=janela_link_musica, bg="#007bff", fg="white", relief="flat", padx=10, pady=5)
botao_link.pack(pady=5)

# Botão para exibir as instruções
botao_instrucoes = tk.Button(
    janela_principal, 
    text="Instruções", 
    command=janela_instrucoes, 
    bg="#6c757d", 
    fg="white", 
    relief="flat", 
    padx=10, 
    pady=5
)
botao_instrucoes.pack(pady=10)


# Adicionar texto de carregando
label_carregando = tk.Label(janela_principal, text="Aguarde, baixando...", font=("tahoma", 12), fg="red", bg="#f7f7f7")

# Executar a janela principal
janela_principal.mainloop()
