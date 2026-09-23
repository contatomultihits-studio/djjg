#!/usr/bin/env python3
"""Gera todas as imagens e ícones de um site de DJ a partir das fotos originais.

Uso (exemplo):
  pip install pillow
  python3 tools/preparar-imagens.py \
    --hero-mobile fotos/DJ_05.png \
    --hero-desktop fotos/DJ_03.png \
    --segunda-foto fotos/LOCUTOR_03.jpeg \
    --iniciais JG --cor-fundo "#FFE500" --cor-texto "#0A0A0A" \
    --fonte-icone BarlowCondensed-Black.ttf \
    --prefixo dj-jg

Saída:
  img/<prefixo>-hero-mobile.webp   1080x1620  (fundo da abertura no celular)
  img/<prefixo>-hero-desktop.webp  1000x1500  (foto recortada na abertura do computador)
  img/<prefixo>-segunda.webp       1350 de largura (foto da 2ª seção, ex.: locutor)
  img/og-<prefixo>.jpg             1200x630   (prévia no WhatsApp/Instagram/Facebook)
  favicon.ico, apple-touch-icon.png, img/icon-192.png  (ícones com as iniciais)

Dica: confira img/og-<prefixo>.jpg. Se o rosto ficar cortado, ajuste --og-topo
(0.0 = recorta do topo da foto, 0.5 = do meio).
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont


def salvar(im, caminho, **kw):
    im.save(caminho, **kw)
    print(f"{caminho:40s} {im.size[0]}x{im.size[1]:<6} {os.path.getsize(caminho) // 1024} KB")


def cobrir(im, largura, altura):
    """Redimensiona e corta no centro para preencher largura x altura."""
    escala = max(largura / im.width, altura / im.height)
    im = im.resize((round(im.width * escala), round(im.height * escala)), Image.LANCZOS)
    x = (im.width - largura) // 2
    y = (im.height - altura) // 2
    return im.crop((x, y, x + largura, y + altura))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hero-mobile", required=True)
    p.add_argument("--hero-desktop", required=True)
    p.add_argument("--segunda-foto")
    p.add_argument("--og-foto", help="foto da prévia de link (padrão: a do hero mobile)")
    p.add_argument("--og-topo", type=float, default=0.10,
                   help="posição vertical do recorte da prévia, de 0 a 1 (padrão 0.10)")
    p.add_argument("--iniciais", required=True)
    p.add_argument("--cor-fundo", default="#FFE500")
    p.add_argument("--cor-texto", default="#0A0A0A")
    p.add_argument("--fonte-icone", help="arquivo .ttf bem grosso (ex.: Barlow Condensed Black)")
    p.add_argument("--prefixo", required=True)
    a = p.parse_args()

    os.makedirs("img", exist_ok=True)

    hm = Image.open(a.hero_mobile).convert("RGB")
    salvar(cobrir(hm, 1080, 1620), f"img/{a.prefixo}-hero-mobile.webp", quality=76, method=6)

    hd = Image.open(a.hero_desktop).convert("RGB")
    salvar(cobrir(hd, 1000, 1500), f"img/{a.prefixo}-hero-desktop.webp", quality=78, method=6)

    if a.segunda_foto:
        sf = Image.open(a.segunda_foto).convert("RGB")
        sf = sf.resize((1350, round(sf.height * 1350 / sf.width)), Image.LANCZOS)
        salvar(sf, f"img/{a.prefixo}-segunda.webp", quality=78, method=6)

    og = Image.open(a.og_foto).convert("RGB") if a.og_foto else hm
    altura = round(og.width * 630 / 1200)
    topo = min(round(og.height * a.og_topo), og.height - altura)
    og = og.crop((0, topo, og.width, topo + altura)).resize((1200, 630), Image.LANCZOS)
    salvar(og, f"img/og-{a.prefixo}.jpg", quality=82, optimize=True, progressive=True)

    n = 512
    ic = Image.new("RGB", (n, n), a.cor_fundo)
    d = ImageDraw.Draw(ic)
    tam = 400 if len(a.iniciais) <= 2 else 300
    fonte = ImageFont.truetype(a.fonte_icone, tam) if a.fonte_icone else ImageFont.load_default(tam)
    b = d.textbbox((0, 0), a.iniciais, font=fonte)
    d.text(((n - (b[2] - b[0])) / 2 - b[0], (n - (b[3] - b[1])) / 2 - b[1]),
           a.iniciais, font=fonte, fill=a.cor_texto)
    salvar(ic.resize((180, 180), Image.LANCZOS), "apple-touch-icon.png", optimize=True)
    salvar(ic.resize((192, 192), Image.LANCZOS), "img/icon-192.png", optimize=True)
    ic.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicon.ico")


if __name__ == "__main__":
    main()
