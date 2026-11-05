# Baixador Universal de Vídeos

Interface gráfica simples (e também linha de comando) para baixar vídeos de diversas plataformas, construída em Python sobre o [yt-dlp](https://github.com/yt-dlp/yt-dlp).

> 🤖 **Este projeto foi feito por IA.** O código foi gerado com o auxílio do Claude e revisado/testado por mim. Pode conter erros ou comportamentos inesperados. Use com atenção.

## Aviso legal

Esta ferramenta deve ser usada **apenas para baixar conteúdo seu, de domínio público ou que você tenha permissão para baixar**. O uso é de inteira responsabilidade do usuário. Respeite os termos de uso das plataformas e as leis de direitos autorais do seu país. Este projeto não contorna DRM e não é afiliado a nenhuma plataforma de vídeo.

## Funcionalidades

- Interface gráfica (Tkinter) com botão de colar link e escolha de pasta
- Escolha de qualidade: melhor, até 1080p, 720p ou 480p
- Extração de áudio em MP3
- Download de playlists inteiras (salvas em subpasta)
- Barra de progresso com velocidade e tempo restante
- Modo terminal para uso rápido
- Instala o `yt-dlp` automaticamente se ele não estiver presente

## Requisitos

- Python 3.9 ou superior (com Tkinter, que já vem no instalador oficial do Windows)
- [ffmpeg](https://ffmpeg.org/) (recomendado, necessário para MP3 e qualidades altas)
- [Deno](https://deno.com/) (pode ser necessário para o YouTube, que exige um interpretador de JavaScript)

## Instalação

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
python -m pip install -U "yt-dlp[default]"
```

Instalando as dependências opcionais no Windows:

```powershell
winget install ffmpeg
winget install DenoLand.Deno
```

Feche e abra o terminal depois de instalar para o Windows reconhecer os programas.

## Como usar

**Interface gráfica:**

```bash
python baixador_universal.py
```

Cole o link, escolha a pasta e a qualidade, e clique em **Baixar**.

**Linha de comando:**

```bash
python baixador_universal.py "https://link-do-video" pasta_de_destino
```

## Solução de problemas

| Problema | O que fazer |
|---|---|
| `No module named 'yt_dlp'` | Rode `python -m pip install yt-dlp` (usar `python -m pip` garante o mesmo Python que executa o script) |
| `Requested format is not available` | Instale o ffmpeg e atualize o yt-dlp: `python -m pip install -U "yt-dlp[default]"` |
| `HTTP Error 403: Forbidden` | Instale o Deno, atualize o yt-dlp e reabra o terminal. Em redes de faculdade/empresa, teste em outra rede |
| Parou de funcionar de repente | As plataformas mudam com frequência. Atualize: `python -m pip install -U yt-dlp` |
| MP3 não funciona | O ffmpeg não foi encontrado no PATH |

## Limitações

- Sites com DRM (Netflix, Disney+, Prime Video, Spotify etc.) não são suportados.
- Conteúdo privado ou que exige login não é suportado nesta versão.
- O funcionamento depende do `yt-dlp`, que pode quebrar quando uma plataforma muda.

## Créditos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - o motor de download, que faz todo o trabalho pesado
- [ffmpeg](https://ffmpeg.org/) - processamento de áudio e vídeo
- Código gerado com auxílio de IA (Claude)
