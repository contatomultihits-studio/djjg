# Site DJ JG (contrateojg.vercel.app)

Landing page de contratação do DJ JG (João Guilherme), DJ e locutor, feita pela Multi Hits
Produtora. Ela é o **modelo** de um serviço que a Multi Hits quer vender para outros DJs.

- **Leia `docs/guia-site-dj.md` antes de mexer.** Ele tem as seções, cores, padrões de
  desempenho, prévia de link e o passo a passo para montar o site de um novo DJ.
- Site estático: `index.html` único (CSS e JS dentro), sem build. Publicado pela Vercel a
  cada merge na `main`. Endereço oficial: `https://contrateojg.vercel.app/`, que deve ser
  usado em `og:url`, `og:image` e `canonical`.
- Nunca subir fotos originais. Gerar as imagens com `tools/preparar-imagens.py` (WebP no
  tamanho da tela, prévia 1200×630 em JPG e ícones).
- Vídeos do YouTube sempre como `.yt-lite` (miniatura + player sob demanda), nunca como
  `<iframe>` direto no HTML.
- Textos em português do Brasil. Revise as mensagens de WhatsApp decodificadas.
