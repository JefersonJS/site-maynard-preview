# -*- coding: utf-8 -*-
"""Gera as páginas internas do protótipo (serviços, posts, sobre, contato, conteúdo)
reaproveitando o conteúdo já aprovado em maynard_seo/content/*.html, dentro do
novo layout (header/footer/CTA/whatsapp compartilhados do prototype/)."""

import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE, "..", "maynard_seo", "content")
OUT_DIR = BASE

WHATSAPP_ICON = (
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2Zm0 18.2a8.1 8.1 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1-.2.2-.7.8-.8 1-.2.2-.3.2-.5.1-.2-.1-1-.4-2-1.2-.7-.7-1.2-1.5-1.4-1.7-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.2-.5.1-.2 0-.4 0-.5-.1-.1-.6-1.5-.9-2-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.2-1 1-1 2.4s1 2.8 1.1 3c.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.3-.5-.3Z"/></svg>'
)
PHONE_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">'
    '<path d="M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.5 21 3 13.5 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1L6.6 10.8z"/></svg>'
)
PIN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-5.7 7-11a7 7 0 1 0-14 0c0 5.3 7 11 7 11Z"/><circle cx="12" cy="11" r="2.6"/></svg>'
CLOCK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>'
INSTAGRAM_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>'

WHATSAPP_URL_GENERIC = "https://api.whatsapp.com/send?phone=5571996266142&text=Olá, vi o site e gostaria de agendar um serviço."


def whatsapp_url(mensagem):
    return f"https://api.whatsapp.com/send?phone=5571996266142&text={mensagem}"


CATEGORIAS = {
    "dicas": "Dicas de Manutenção",
    "cuidados": "Cuidados com o Veículo",
    "salvador": "Oficina em Salvador",
}

IMAGENS = {
    "oil_change": {"alt": "Mecânico trocando o óleo do motor de um carro"},
    "general_mechanic": {"alt": "Mecânico segurando um motor de carro removido para reparo"},
    "wheel_service": {"alt": "Mecânico fazendo manutenção na roda de um carro em elevador"},
    "diagnostic_scanner": {"alt": "Mecânico usando scanner de diagnóstico eletrônico em um carro"},
    "brake_disc": {"alt": "Mecânico ajustando pinça de freio em disco de freio"},
    "engine_parts": {"alt": "Motor de carro aberto mostrando peças internas"},
    "road_trip": {"alt": "Carros em uma rodovia durante viagem"},
    "luxury_import": {"alt": "Carro importado BMW estacionado em garagem"},
    "workshop_generic": {"alt": "Mecânico usando tablet para verificar o motor de um carro na oficina"},
}

SERVICOS = [
    {
        "slug": "troca-de-oleo", "menu": "Troca de Óleo", "titulo": "Troca de Óleo em Salvador | Maynard Auto Center",
        "meta_desc": "Troca de óleo para nacionais e importados em Salvador, Av. ACM. Óleo mineral, semissintético e sintético. Agende pelo WhatsApp.",
        "imagem": "oil_change", "whats_msg": "Quero%20agendar%20troca%20de%20óleo",
    },
    {
        "slug": "mecanica-completa", "menu": "Mecânica Completa", "titulo": "Mecânica Completa em Salvador | Nacionais e Importados",
        "meta_desc": "Mecânica geral para nacionais e importados em Salvador. Suspensão, freios, injeção, câmbio e mais. Av. ACM, 3410.",
        "imagem": "general_mechanic", "whats_msg": "Quero%20agendar%20mecânica%20completa",
    },
    {
        "slug": "alinhamento-balanceamento", "menu": "Alinhamento e Balanceamento", "titulo": "Alinhamento e Balanceamento em Salvador | Maynard Auto Center",
        "meta_desc": "Alinhamento e balanceamento para nacionais e importados em Salvador. Av. ACM, 3410. Agende pelo WhatsApp.",
        "imagem": "wheel_service", "whats_msg": "Quero%20agendar%20alinhamento%20e%20balanceamento",
    },
    {
        "slug": "checkup-eletronico", "menu": "Checkup Eletrônico", "titulo": "Checkup Eletrônico em Salvador | Diagnóstico Automotivo",
        "meta_desc": "Diagnóstico eletrônico completo para nacionais e importados em Salvador. Av. ACM, 3410. Agende agora.",
        "imagem": "diagnostic_scanner", "whats_msg": "Quero%20agendar%20checkup%20eletrônico",
    },
    {
        "slug": "suspensao-freios", "menu": "Suspensão e Freios", "titulo": "Suspensão e Freios em Salvador | Maynard Auto Center",
        "meta_desc": "Revisão de suspensão e freios em Salvador. Diagnóstico, amortecedores, pastilhas, discos e muito mais. Av. ACM, 3410.",
        "imagem": "brake_disc", "whats_msg": "Quero%20agendar%20revisão%20de%20suspensão%20e%20freios",
    },
    {
        "slug": "limpeza-bicos-injetores", "menu": "Limpeza de Bicos Injetores", "titulo": "Limpeza de Bicos Injetores em Salvador | Maynard Auto Center",
        "meta_desc": "Limpeza ultrassônica de bicos injetores em Salvador. Mais potência, menos consumo. Av. ACM, 3410.",
        "imagem": "engine_parts", "whats_msg": "Quero%20agendar%20limpeza%20de%20bicos%20injetores",
    },
    {
        "slug": "revisao-de-viagem", "menu": "Revisão de Viagem", "titulo": "Revisão de Viagem em Salvador | Maynard Auto Center",
        "meta_desc": "Revisão completa antes de viagem longa em Salvador. Freios, pneus, fluidos, elétrica e mais. Av. ACM, 3410.",
        "imagem": "road_trip", "whats_msg": "Quero%20agendar%20revisão%20de%20viagem",
    },
    {
        "slug": "veiculos-importados", "menu": "Veículos Importados", "titulo": "Oficina para Carros Importados em Salvador | Maynard Auto Center",
        "meta_desc": "Mecânica especializada em carros importados em Salvador. BMW, Mercedes, Audi, Volkswagen e mais. Av. ACM, 3410.",
        "imagem": "luxury_import", "whats_msg": "Quero%20agendar%20revisão%20do%20meu%20importado",
    },
]

POSTS = [
    {
        "slug": "quando-trocar-oleo-carro", "titulo": "Quando é a hora certa de trocar o óleo do carro?",
        "categoria": "dicas", "imagem": "oil_change", "relacionado": "troca-de-oleo",
        "meta_desc": "Saiba quando é a hora de trocar o óleo do carro: por quilometragem, por tempo e pelos sinais que o carro dá.",
    },
    {
        "slug": "sinais-suspensao-precisa-revisao", "titulo": "5 sinais de que a suspensão do seu carro precisa de revisão",
        "categoria": "dicas", "imagem": "brake_disc", "relacionado": "suspensao-freios",
        "meta_desc": "Carro balançando muito, barulho em buracos ou volante tremendo? Veja 5 sinais de que a suspensão precisa de revisão.",
    },
    {
        "slug": "o-que-e-checkup-eletronico-carro", "titulo": "O que é checkup eletrônico e por que você precisa fazer",
        "categoria": "dicas", "imagem": "diagnostic_scanner", "relacionado": "checkup-eletronico",
        "meta_desc": "Descubra o que é o checkup eletrônico do carro, como funciona o diagnóstico automotivo e quando fazer.",
    },
    {
        "slug": "quanto-tempo-dura-freio-carro", "titulo": "Quanto tempo dura o freio do carro? Saiba o que afeta a vida útil",
        "categoria": "dicas", "imagem": "brake_disc", "relacionado": "suspensao-freios",
        "meta_desc": "A vida útil do freio varia de 20.000 a 60.000 km. Veja o que afeta a durabilidade das pastilhas, discos e fluido.",
    },
    {
        "slug": "diferenca-alinhamento-balanceamento", "titulo": "Alinhamento e balanceamento: qual a diferença e quando fazer cada um",
        "categoria": "cuidados", "imagem": "wheel_service", "relacionado": "alinhamento-balanceamento",
        "meta_desc": "Entenda de vez a diferença entre alinhamento e balanceamento de rodas, quando fazer cada um e o que acontece se deixar passar.",
    },
    {
        "slug": "como-preparar-carro-viagem-longa", "titulo": "Como preparar o carro para uma viagem longa: o checklist completo",
        "categoria": "cuidados", "imagem": "road_trip", "relacionado": "revisao-de-viagem",
        "meta_desc": "Checklist completo para preparar o carro antes de uma viagem longa: freios, pneus, óleo, fluidos, bateria e mais.",
    },
    {
        "slug": "oficina-carros-importados-salvador", "titulo": "Oficina para carros importados em Salvador: o que saber antes de ir",
        "categoria": "salvador", "imagem": "luxury_import", "relacionado": "veiculos-importados",
        "meta_desc": "Procurando oficina para carro importado em Salvador? Saiba o que diferencia uma oficina preparada de uma que não é.",
    },
    {
        "slug": "como-escolher-oficina-mecanica-salvador", "titulo": "Como escolher uma boa oficina mecânica em Salvador",
        "categoria": "salvador", "imagem": "workshop_generic", "relacionado": None,
        "meta_desc": "Saiba o que avaliar antes de escolher uma oficina mecânica em Salvador: equipamento, orçamento transparente, avaliações.",
    },
]

PAGINAS_INSTITUCIONAIS = [
    {"slug": "sobre", "titulo": "Sobre a Maynard Auto Center | Oficina em Salvador", "imagem": "workshop_generic",
     "meta_desc": "Conheça a Maynard Auto Center, oficina mecânica em Salvador especializada em veículos nacionais e importados."},
    {"slug": "contato", "titulo": "Contato | Maynard Auto Center", "imagem": "workshop_generic",
     "meta_desc": "Entre em contato com a Maynard Auto Center em Salvador. WhatsApp: (71) 99626-6142. Seg-Sex 8h-18h | Sáb 8h-12h."},
]


CHEVRON_ICON = '<svg class="has-submenu__chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'


def submenu_servicos_html():
    itens = "\n".join(
        f'        <li><a href="{s["slug"]}.html">{s["menu"]}</a></li>'
        for s in SERVICOS
    )
    return f"""      <div class="has-submenu">
        <a href="servicos.html">Serviços</a>
        <button class="has-submenu__toggle" aria-expanded="false" aria-controls="submenu-servicos" aria-label="Abrir lista de serviços">{CHEVRON_ICON}</button>
        <ul class="submenu" id="submenu-servicos">
          <li><a href="servicos.html">Todos os serviços</a></li>
{itens}
        </ul>
      </div>"""


def nav_html():
    return f"""    <nav class="site-header__nav" aria-label="Navegação principal">
      <a href="sobre.html">Sobre</a>
{submenu_servicos_html()}
      <a href="conteudo.html">Conteúdo</a>
      <a href="index.html#localizacao">Localização</a>
      <a href="contato.html">Contato</a>
      <div class="site-header__nav-extra">
        <a class="site-header__phone" href="tel:+5571996266142">{PHONE_ICON}(71) 99626-6142</a>
        <a class="btn btn--primary" href="{WHATSAPP_URL_GENERIC}">Agendar no WhatsApp</a>
      </div>
    </nav>"""


def header_html():
    return f"""<header class="site-header">
  <div class="container">
    <a href="index.html" class="site-header__logo" aria-label="Maynard Auto Center - início">
      <img src="assets/images/logo_maynard.png" alt="Maynard Auto Center">
    </a>
{nav_html()}
    <div class="site-header__actions">
      <a class="site-header__phone" href="tel:+5571996266142">{PHONE_ICON}(71) 99626-6142</a>
      <a class="btn btn--primary" href="{WHATSAPP_URL_GENERIC}">Agendar no WhatsApp</a>
      <button class="nav-toggle" aria-label="Abrir menu" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</header>"""


def footer_html():
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-logo"><img src="assets/images/logo_maynard.png" alt="Maynard Auto Center"></div>
        <p>Mecânica completa para nacionais e importados na Av. ACM, Salvador, Bahia.</p>
        <div class="social-links">
          <a href="https://www.instagram.com/maynardautocenter/" aria-label="Instagram">{INSTAGRAM_ICON}</a>
        </div>
      </div>
      <div>
        <h4>Serviços</h4>
        <ul>
          <li><a href="troca-de-oleo.html">Troca de Óleo</a></li>
          <li><a href="mecanica-completa.html">Mecânica Completa</a></li>
          <li><a href="alinhamento-balanceamento.html">Alinhamento e Balanceamento</a></li>
          <li><a href="servicos.html">Ver todos</a></li>
        </ul>
      </div>
      <div>
        <h4>Contato</h4>
        <ul>
          <li><a href="tel:+5571996266142">(71) 99626-6142</a></li>
          <li><a href="{WHATSAPP_URL_GENERIC}">WhatsApp</a></li>
          <li><a href="contato.html">Fale conosco</a></li>
        </ul>
      </div>
      <div>
        <h4>Horário</h4>
        <ul>
          <li>Seg a Sex: 8h às 18h</li>
          <li>Sábado: 8h às 12h</li>
          <li>Domingo: fechado</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Maynard Auto Center · Av. Antônio Carlos Magalhães, nº 3410, Iguatemi, Salvador/BA.</span>
      <span>Protótipo de layout · em desenvolvimento</span>
    </div>
  </div>
</footer>"""


def whatsapp_float_html():
    return f"""<a class="whatsapp-float" href="{WHATSAPP_URL_GENERIC}" aria-label="Falar no WhatsApp">
  {WHATSAPP_ICON}
</a>"""


def cta_band_html():
    return f"""<section class="cta-band section--black">
  <div class="container">
    <span class="eyebrow">Vamos resolver o seu carro?</span>
    <h2>Agende agora pelo WhatsApp</h2>
    <p class="lead">Resposta rápida, diagnóstico honesto e orçamento antes de qualquer serviço.</p>
    <div class="cta-band__actions">
      <a class="btn btn--primary" href="{WHATSAPP_URL_GENERIC}">Chamar no WhatsApp</a>
      <a class="btn btn--outline" style="color:#fff;border-color:rgba(255,255,255,0.6);" href="tel:+5571996266142">Ligar: (71) 99626-6142</a>
    </div>
  </div>
</section>"""


def page_shell(title, description, canonical_slug, image_rel, schemas, body):
    schema_scripts = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://maynardautocenter.com.br/{canonical_slug}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image_rel}">
<meta property="og:locale" content="pt_BR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=6">
{schema_scripts}
</head>
<body>

{header_html()}

{body}

{cta_band_html()}

{footer_html()}

{whatsapp_float_html()}

<script src="assets/js/main.js?v=6"></script>
</body>
</html>
"""


def breadcrumb(trilha):
    """trilha: lista de (label, href_or_None). Último item sem href = atual."""
    partes = []
    for label, href in trilha:
        if href:
            partes.append(f'<a href="{href}">{label}</a>')
        else:
            partes.append(f'<span aria-current="page">{label}</span>')
    return f"""<div class="breadcrumb-strip">
  <div class="container"><p class="breadcrumb">{" / ".join(partes)}</p></div>
</div>"""


def extrair_conteudo_limpo(slug):
    """Lê maynard_seo/content/<slug>.html, remove a <img> de topo (se houver) e os
    blocos de schema do final, retorna (corpo_limpo, lista_de_schemas)."""
    caminho = os.path.join(CONTENT_DIR, f"{slug}.html")
    texto = open(caminho, encoding="utf-8").read()

    schemas = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', texto, re.DOTALL):
        schemas.append(json.loads(m.group(1)))

    idx_script = texto.find("<script")
    corpo = texto if idx_script == -1 else texto[:idx_script]
    corpo = re.sub(r'^<img[^>]*/>\s*\n+', "", corpo, count=1, flags=re.DOTALL)
    return corpo.strip(), schemas


def atualizar_imagem_schemas(schemas, nova_url):
    for s in schemas:
        if "image" in s:
            s["image"] = nova_url
    return schemas


def sidebar_cta(mensagem_whatsapp=None):
    url = whatsapp_url(mensagem_whatsapp) if mensagem_whatsapp else WHATSAPP_URL_GENERIC
    return f"""<div class="cta-card">
        <h3>Agende esse serviço</h3>
        <p>Resposta rápida no WhatsApp, diagnóstico antes do orçamento.</p>
        <a class="btn btn--primary" href="{url}">{WHATSAPP_ICON} Chamar no WhatsApp</a>
        <ul class="info-list">
          <li>{PIN_ICON}<span>Av. ACM, nº 3410, Iguatemi, Salvador</span></li>
          <li>{CLOCK_ICON}<span>Seg-Sex 8h-18h · Sáb 8h-12h</span></li>
        </ul>
      </div>"""


def sidebar_outros_servicos(slug_atual):
    itens = "".join(
        f'<li><a href="{s["slug"]}.html">{s["titulo"].split("|")[0].strip()}</a></li>'
        for s in SERVICOS if s["slug"] != slug_atual
    )
    return f"""<div class="side-card">
        <h4>Outros Serviços</h4>
        <ul>{itens}</ul>
      </div>"""


def gerar_pagina_servico(servico):
    slug = servico["slug"]
    corpo, schemas = extrair_conteudo_limpo(slug)
    img_key = servico["imagem"]
    img_rel = f"assets/images/{img_key}.jpg"
    alt = IMAGENS[img_key]["alt"]
    schemas = atualizar_imagem_schemas(schemas, img_rel)

    body = f"""{breadcrumb([("Início", "index.html"), ("Serviços", "servicos.html"), (servico["titulo"].split("|")[0].strip(), None)])}
<section class="title-band">
  <div class="container">
    <span class="eyebrow">Serviço</span>
    <h1>{servico["titulo"]}</h1>
  </div>
</section>
<section>
  <div class="container content-layout">
    <div class="content-main">
      <img class="featured" src="{img_rel}" alt="{alt}" loading="eager">
      {corpo}
    </div>
    <aside class="content-sidebar">
      {sidebar_cta(servico["whats_msg"])}
      {sidebar_outros_servicos(slug)}
    </aside>
  </div>
</section>"""

    html = page_shell(
        title=f"{servico['titulo']} - MAYNARD AUTO CENTER",
        description=servico["meta_desc"],
        canonical_slug=f"servicos/{slug}",
        image_rel=img_rel,
        schemas=schemas,
        body=body,
    )
    with open(os.path.join(OUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Gerado: {slug}.html")


def sidebar_post(post):
    blocos = [sidebar_cta()]
    if post["relacionado"]:
        rel = next(s for s in SERVICOS if s["slug"] == post["relacionado"])
        blocos.append(f"""<div class="side-card">
        <h4>Serviço Relacionado</h4>
        <ul><li><a href="{rel['slug']}.html">{rel['titulo'].split('|')[0].strip()}</a></li></ul>
      </div>""")
    blocos.append(f"""<div class="side-card">
        <h4>Leia Também</h4>
        <ul><li><a href="conteudo.html">Ver todas as publicações</a></li></ul>
      </div>""")
    return "\n      ".join(blocos)


def gerar_pagina_post(post):
    slug = post["slug"]
    corpo, schemas = extrair_conteudo_limpo(slug)
    img_key = post["imagem"]
    img_rel = f"assets/images/{img_key}.jpg"
    alt = IMAGENS[img_key]["alt"]
    schemas = atualizar_imagem_schemas(schemas, img_rel)
    categoria_label = CATEGORIAS[post["categoria"]]

    body = f"""{breadcrumb([("Início", "index.html"), ("Conteúdo", "conteudo.html"), (post["titulo"], None)])}
<section class="title-band">
  <div class="container">
    <div class="eyebrow-row">
      <span class="category-badge">{categoria_label}</span>
    </div>
    <h1>{post["titulo"]}</h1>
  </div>
</section>
<section>
  <div class="container content-layout">
    <div class="content-main">
      <img class="featured" src="{img_rel}" alt="{alt}" loading="eager">
      {corpo}
    </div>
    <aside class="content-sidebar">
      {sidebar_post(post)}
    </aside>
  </div>
</section>"""

    html = page_shell(
        title=f"{post['titulo']} - MAYNARD AUTO CENTER",
        description=post["meta_desc"],
        canonical_slug=f"blog/{slug}",
        image_rel=img_rel,
        schemas=schemas,
        body=body,
    )
    with open(os.path.join(OUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Gerado: {slug}.html")


def gerar_pagina_sobre():
    slug = "sobre"
    corpo, schemas = extrair_conteudo_limpo(slug)
    img_rel = "assets/images/workshop_generic.jpg"
    schemas = atualizar_imagem_schemas(schemas, img_rel)

    body = f"""{breadcrumb([("Início", "index.html"), ("Sobre", None)])}
<section class="title-band">
  <div class="container">
    <span class="eyebrow">Sobre</span>
    <h1>Sobre a Maynard Auto Center</h1>
  </div>
</section>
<section>
  <div class="container content-layout">
    <div class="content-main">
      <img class="featured" src="{img_rel}" alt="{IMAGENS['workshop_generic']['alt']}" loading="eager">
      {corpo}
    </div>
    <aside class="content-sidebar">
      {sidebar_cta()}
    </aside>
  </div>
</section>"""

    html = page_shell(
        title="Sobre a Maynard Auto Center | Oficina em Salvador - MAYNARD AUTO CENTER",
        description="Conheça a Maynard Auto Center, oficina mecânica em Salvador especializada em veículos nacionais e importados.",
        canonical_slug="sobre",
        image_rel=img_rel,
        schemas=schemas,
        body=body,
    )
    with open(os.path.join(OUT_DIR, "sobre.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Gerado: sobre.html")


def gerar_pagina_contato():
    img_rel = "assets/images/workshop_generic.jpg"
    schemas = [{
        "@context": "https://schema.org", "@type": "AutoRepair", "name": "Maynard Auto Center",
        "url": "https://maynardautocenter.com.br", "telephone": "+55-71-99626-6142", "image": img_rel,
        "address": {"@type": "PostalAddress", "streetAddress": "Av. Antônio Carlos Magalhães, nº 3410",
                    "addressLocality": "Salvador", "addressRegion": "BA", "postalCode": "41820-000", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": -12.9868909, "longitude": -38.4659888},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "12:00"},
        ],
    }]

    body = f"""{breadcrumb([("Início", "index.html"), ("Contato", None)])}
<section class="title-band">
  <div class="container">
    <span class="eyebrow">Contato</span>
    <h1>Fale com a Maynard Auto Center</h1>
    <p class="lead">Quer agendar um serviço, tirar uma dúvida ou pedir um orçamento? Fale pelo canal mais fácil pra você.</p>
  </div>
</section>
<section>
  <div class="container location-grid" style="margin-top:24px;margin-bottom:72px;">
    <div>
      <ul class="info-list">
        <li>{PIN_ICON}<span>Av. Antônio Carlos Magalhães, nº 3410 · no estacionamento do Sam's Club, ao lado do Hiper BomPreço, Iguatemi, Salvador, BA. CEP 41820-000.</span></li>
        <li>{CLOCK_ICON}<span>Segunda a sexta: 8h às 18h · Sábado: 8h às 12h · Domingo: fechado.</span></li>
        <li>{PHONE_ICON}<span>(71) 99626-6142 · WhatsApp e telefone.</span></li>
      </ul>
      <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:8px;">
        <a class="btn btn--primary" href="{WHATSAPP_URL_GENERIC}">{WHATSAPP_ICON} Chamar no WhatsApp</a>
        <a class="btn btn--outline" href="tel:+5571996266142">Ligar agora</a>
      </div>
    </div>
    <div class="map-frame">
      <iframe title="Mapa - Maynard Auto Center" src="https://www.google.com/maps?q=-12.9868909,-38.4659888&z=16&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>"""

    html = page_shell(
        title="Contato | Maynard Auto Center · Oficina em Salvador - MAYNARD AUTO CENTER",
        description="Entre em contato com a Maynard Auto Center em Salvador. WhatsApp: (71) 99626-6142. Seg-Sex 8h-18h | Sáb 8h-12h.",
        canonical_slug="contato",
        image_rel=img_rel,
        schemas=schemas,
        body=body,
    )
    with open(os.path.join(OUT_DIR, "contato.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Gerado: contato.html")


def gerar_conteudo_index():
    cards = []
    for p in POSTS:
        img_key = p["imagem"]
        cards.append(f"""      <div class="card">
        <div class="card__img"><img src="assets/images/{img_key}.jpg" alt="{IMAGENS[img_key]['alt']}" loading="lazy"></div>
        <div class="card__body">
          <span class="category-badge" style="align-self:flex-start;">{CATEGORIAS[p['categoria']]}</span>
          <h3>{p['titulo']}</h3>
          <p>{p['meta_desc']}</p>
          <div class="card__footer">
            <a href="{p['slug']}.html">Ler publicação</a>
          </div>
        </div>
      </div>""")

    body = f"""{breadcrumb([("Início", "index.html"), ("Conteúdo", None)])}
<section class="section" style="padding-top:32px;">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Conteúdo</span>
      <h1>Dicas de manutenção e cuidados com o carro</h1>
      <p>Conteúdo prático sobre manutenção automotiva, direto da equipe da Maynard Auto Center em Salvador.</p>
    </div>
    <div class="grid grid--3">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""

    schemas = [{
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"https://maynardautocenter.com.br/blog/{p['slug']}/"}
            for i, p in enumerate(POSTS)
        ],
    }]

    html = page_shell(
        title="Conteúdo | Dicas de Manutenção Automotiva - MAYNARD AUTO CENTER",
        description="Dicas de manutenção, cuidados com o veículo e conteúdo sobre oficinas em Salvador, direto da Maynard Auto Center.",
        canonical_slug="conteudo",
        image_rel="assets/images/workshop_generic.jpg",
        schemas=schemas,
        body=body,
    )
    with open(os.path.join(OUT_DIR, "conteudo.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Gerado: conteudo.html")


if __name__ == "__main__":
    for s in SERVICOS:
        gerar_pagina_servico(s)
    for p in POSTS:
        gerar_pagina_post(p)
    gerar_pagina_sobre()
    gerar_pagina_contato()
    gerar_conteudo_index()
    print("\nTudo gerado com sucesso.")
