# Guia: site de contratação para DJ (modelo DJ JG)

Este repositório é o site **https://contrateojg.vercel.app/** do DJ JG (João Guilherme),
feito pela Multi Hits Produtora. Ele serve de **modelo** para vender o mesmo serviço
para outros DJs. Este guia registra os padrões do site e o passo a passo para montar
um novo.

---

## 1. O que o site é

Uma página única de venda (landing page), pensada para o **celular primeiro**. O objetivo
é levar o contratante até o **WhatsApp**. Não tem build, framework nem banco de dados:
um `index.html` com CSS e JS dentro, mais uma pasta `img/`. A hospedagem é gratuita na
Vercel, ligada ao GitHub: cada merge na `main` publica sozinho.

### Arquivos
```
index.html            página inteira (HTML + CSS + JS)
img/                  imagens otimizadas (WebP) + prévia de link + ícone 192
favicon.ico           ícone da aba do navegador
apple-touch-icon.png  ícone do atalho na tela inicial do iPhone
tools/preparar-imagens.py  gera todas as imagens a partir das fotos originais
docs/guia-site-dj.md  este guia
CLAUDE.md             resumo lido automaticamente pelo Claude Code ao abrir o repositório
.vercelignore         impede que docs/, tools/ e CLAUDE.md sejam publicados no site
```

---

## 2. Seções da página (na ordem)

| # | Seção | Conteúdo | Por quê |
|---|---|---|---|
| 1 | **Menu fixo** | Abas "DJ" e "Locutor" (âncoras `#dj` e `#locutor`). A aba acompanha a rolagem | Mostra logo as duas frentes do artista |
| 2 | **Abertura (hero)** | Linha pequena com as funções e a cidade, nome grande com destaque amarelo, frase de impacto e botões Instagram, **WhatsApp** e YouTube | Primeira tela = quem é + como contratar |
| 3 | **Faixa animada** | "PISTA PARADA NUNCA MAIS!" rolando em fundo vermelho | Slogan e energia |
| 4 | **Bio do DJ** | 2 parágrafos, destaques em amarelo, etiquetas de estilo (Funk, Eletrônico…) | Prova de estilo musical |
| 5 | **Bastidores** | Carrossel de Shorts do YouTube (vertical, 9:16) | Prova social rápida |
| 6 | **Sets ao vivo** | Carrossel de vídeos 16:9, podendo começar num minuto específico (`start`) | Mostra o DJ tocando |
| 7 | **2ª frente (Locutor)** | Paleta própria (azul-marinho e âmbar), selo "No ar", bio, rádios, foto, carrossel de Shorts e botão de WhatsApp com mensagem própria | Vende o segundo serviço sem misturar com o DJ |
| 8 | **Para contratantes** | Botões para Google Drive: fotos oficiais, logo e rider técnico | Facilita a vida do produtor do evento |
| 9 | **Produto** | Pack de músicas com lista de benefícios e botão de compra (Kiwify) | Renda extra com o mesmo tráfego |
| 10 | **Rodapé** | Nome + "© Multi Hits Produtora Ltda" | Assinatura |
| — | **Botão flutuante** | WhatsApp verde fixo no canto, sempre visível | Contratação a um toque de distância |

A seção 7 (Locutor) e a 9 (Pack) são **opcionais**. Para um DJ sem outra frente, remova a
seção 7 e a aba "Locutor" do menu. A seção 7 também pode virar outra frente, como
Produtor, MC ou Aulas.

---

## 3. Identidade visual (padrões)

### Cores (variáveis em `:root`)
| Variável | Cor | Uso |
|---|---|---|
| `--black` | `#0A0A0A` | Fundo geral |
| `--white` | `#F5F5F5` | Texto |
| `--red` | `#C8000A` | Faixa animada, rótulos de seção, bordas das etiquetas, degradê da abertura no computador |
| `--yellow` | `#FFE500` | Destaques (`.hl`), nome em destaque, botão do pack, aba DJ ativa |
| `--gray` / `--gray2` | `#1A1A1A` / `#2A2A2A` | Fundos de cartões e divisórias |
| `--navy` / `--navy2` | `#060912` / `#0E1526` | Fundo da seção Locutor |
| `--amber` | `#FFB100` | Destaque da seção Locutor |

Para outro DJ, troque principalmente `--red` e `--yellow` pelas cores dele (e o degradê
em `@media (min-width: 768px) .hero-bg`).

### Tipografia
- **Barlow Condensed** (400/700/900): títulos, botões, rótulos, sempre em CAIXA ALTA e com
  espaçamento entre letras.
- **Barlow** (400/500/700): textos corridos.
- Tamanhos com `clamp()`, que se ajustam sozinhos do celular ao computador.

### Estilo
- Visual de "flyer de balada": fundo escuro, blocos de cor chapada, cantos retos
  (só os vídeos e o botão flutuante têm cantos arredondados).
- Destaques de texto com `<span class="hl">` (amarelo e negrito).
- Mobile primeiro. Pontos de quebra: **768px** (computador) e **1200px** (tela larga).
- Abertura: no **celular** é a foto de fundo escurecida com degradê; no **computador**
  é um degradê vermelho com a foto recortada à direita.

---

## 4. Padrões de desempenho (não pular)

Foi isso que tirou a página de ~18 MB para ~100 KB no celular.

1. **Imagens em WebP no tamanho da tela.** Nunca subir foto original de câmera ou PNG
   gigante. Use `tools/preparar-imagens.py`.
2. **Uma foto por aparelho.** A foto do computador fica num `<picture>` com
   `<source media="(min-width: 768px)">` e um GIF transparente de 1px como `src`, para o
   celular não baixá-la. A foto do celular é `background-image` do `.hero-bg`, que o CSS do
   computador substitui.
3. **Preload da foto da abertura**, com `media` diferente para celular e computador.
4. **Vídeos sob demanda ("YouTube leve").** Nenhum `<iframe>` no HTML. Cada vídeo é um
   `<button class="yt-lite" data-yt="ID" data-start="SEG" data-title="…">` com a
   miniatura `https://i.ytimg.com/vi/ID/hqdefault.jpg` (`loading="lazy"`) e um botão de
   play. O JS no fim da página troca o botão pelo iframe `youtube-nocookie` com
   `autoplay=1` só quando a pessoa toca.
5. Imagens abaixo da dobra com `loading="lazy"`, `decoding="async"`, `width` e `height`.
6. Fonte do Google com `display=swap` e `preconnect`.

---

## 5. Prévia de link (WhatsApp, Instagram, Facebook)

- Imagem própria de **1200×630 em JPG, menos de 100 KB** (`img/og-….jpg`), com o rosto do
  artista em destaque.
- `og:url`, `og:image`, `twitter:image` e `<link rel="canonical">` devem usar **o endereço
  oficial de verdade** do site (hoje `https://contrateojg.vercel.app/`). Se apontarem para um
  domínio que não serve o site, o Facebook pega outra imagem qualquer da página.
- Depois de publicar: [Depurador de Compartilhamento](https://developers.facebook.com/tools/debug/)
  → colar o link → **Extrair novamente**.
- O aviso "fb:app_id ausente" pode ser ignorado: ele só serve para estatísticas do Facebook.

---

## 6. Comportamentos em JavaScript (no fim do `index.html`)

1. **Setas dos carrosséis** (só no computador): `.car-btn` com `data-target="id-do-trilho"`
   rola um cartão por clique. No celular a pessoa arrasta, e aparece o aviso "Arraste para
   o lado".
2. **YouTube leve**: troca a miniatura pelo player ao tocar.
3. **Menu ativo**: a aba "Locutor" acende (âmbar) enquanto a seção `#locutor` passa pela
   tela; no resto da página acende a aba "DJ" (amarelo).

---

## 7. Links de conversão

- **WhatsApp com mensagem pronta**:
  `https://wa.me/55DDDNUMERO?text=` + mensagem codificada (use `encodeURIComponent`).
  Cada botão pode ter a sua mensagem ("quero contratar o DJ…", "quero falar sobre locução…").
  **Revise o texto decodificado**: o site do JG saiu com "locação" no lugar de "locução".
- Instagram, YouTube, Google Drive (material para contratantes) e Kiwify (produto).

---

## 8. Passo a passo para montar o site de um novo DJ

### 8.1 Coletar do cliente (checklist)
- [ ] Nome artístico, nome real, cidade, funções (DJ, Locutor, Produtor…)
- [ ] Frase de impacto e slogan para a faixa animada (ex.: "PISTA PARADA NUNCA MAIS!")
- [ ] Bio curta (2 parágrafos) e estilos musicais (4 a 6 etiquetas)
- [ ] 3 fotos: **vertical, corpo inteiro, fundo liso** (abertura no celular); **vertical,
      fundo liso** para recortar (abertura no computador); **uma para a 2ª frente**, se houver
- [ ] Cores da marca (principal e destaque) e logo
- [ ] WhatsApp de contratação e mensagem padrão
- [ ] Instagram, YouTube e outras redes
- [ ] Links dos vídeos: 4 a 8 Shorts de bastidores e 2 a 4 sets (com o minuto de início)
- [ ] Links do Google Drive: fotos em alta, logo e rider técnico
- [ ] Opcional: 2ª frente (Locutor, Produtor…) com bio, emissoras e vídeos
- [ ] Opcional: produto para vender (pack, curso) e link de pagamento
- [ ] Endereço desejado (ex.: `contrateofulano.vercel.app` ou domínio próprio)

### 8.2 Criar o repositório
1. No GitHub, crie um repositório novo (ex.: `djfulano`) e copie `index.html`, `tools/`,
   `docs/`, `.vercelignore` e `CLAUDE.md` deste repositório (não copie a pasta `img/` nem os
   ícones do JG). Atualize o `CLAUDE.md` com o nome e o endereço do novo DJ.
2. Coloque as fotos originais do cliente numa pasta **fora** do repositório (ou apague-as
   depois). Elas não devem ser publicadas.

### 8.3 Gerar as imagens
```bash
pip install pillow
python3 tools/preparar-imagens.py \
  --hero-mobile ~/fotos/foto-corpo-inteiro.jpg \
  --hero-desktop ~/fotos/foto-recorte.jpg \
  --segunda-foto ~/fotos/foto-locutor.jpg \
  --iniciais DF --cor-fundo "#FFE500" --cor-texto "#0A0A0A" \
  --fonte-icone BarlowCondensed-Black.ttf \
  --prefixo dj-fulano
```
Confira `img/og-dj-fulano.jpg`. Se o rosto ficar cortado, rode de novo com
`--og-topo 0.05` (mais para cima) ou `0.2` (mais para baixo).

### 8.4 Editar o `index.html` (buscar e trocar)
1. `<title>`, `description`, todas as tags `og:*` e `twitter:*`, e `canonical` → nome e
   endereço oficial do novo DJ.
2. Caminhos das imagens: `img/dj-jg-…` → `img/dj-fulano-…` (preload, `.hero-bg`,
   `<picture>`, foto da 2ª seção e `og:image`).
3. Cores em `:root` e o degradê da abertura no computador.
4. Abertura: linha pequena, nome, frase e links de Instagram, WhatsApp e YouTube.
5. Faixa animada: o slogan (repetido 6 vezes para a animação não ter buraco).
6. Bio e etiquetas.
7. Vídeos: em cada `.yt-lite`, trocar `data-yt`, `data-title`, `aria-label`, a URL da
   miniatura e, nos sets, `data-start` (em segundos). O ID é o trecho depois de `v=` ou de
   `/shorts/` no link do YouTube.
8. Seção Locutor: adaptar ou remover (e remover a aba do menu).
9. Links do Drive, bloco do produto e rodapé.
10. **Todos os links de WhatsApp** (abertura, locutor e botão flutuante): número e mensagem.

### 8.5 Testar antes de publicar
- Abrir localmente: `python3 -m http.server 8000` → `http://localhost:8000`.
- No celular (ou no modo celular do navegador, F12): abertura, carrosséis, tocar num
  vídeo, menu trocando de aba, todos os botões de WhatsApp com a mensagem certa.
- Pesquisar no HTML por `jg`, `JG` e `João` para garantir que não sobrou nada do modelo.

### 8.6 Publicar na Vercel
1. Em vercel.com, **Add New → Project**, importar o repositório do GitHub (sem framework,
   sem comando de build).
2. Em **Settings → Domains**, definir o endereço (ex.: `contrateofulano.vercel.app`) ou
   ligar um domínio próprio.
3. Conferir se `og:url`, `og:image` e `canonical` usam exatamente esse endereço.
4. Rodar o link no Depurador de Compartilhamento do Facebook e clicar em **Extrair
   novamente**.
5. Mandar o link para o cliente pelo WhatsApp e ver a prévia aparecer.

### 8.7 Entrega
- Checklist de pontos em aberto para o cliente (vídeos novos, fotos, preços).
- Manutenção: cada alteração vira um pull request no GitHub; o merge publica sozinho.

---

## 9. Pendências conhecidas neste site (DJ JG)
- No celular, o botão flutuante "Contratar" cobre parte do botão do YouTube na abertura.
  O cliente preferiu deixar como está por enquanto.
