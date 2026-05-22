import fitz

MARGIN = 20
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MIN_BOTTOM_GAP = 40

doc = fitz.open()
page = doc.new_page(width=595, height=842)

font_regular = "helv"

PAGE_WIDTH = 595

# =========================
# BACKGROUND (CLEAN DESIGN)
# =========================



PAGE_WIDTH = 595
PAGE_HEIGHT = 842

margin = 20  # cleaner

# Green background (full page)
page.draw_rect(
    fitz.Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT),
    fill=(0.0, 0.5, 0.2)  # dark green
)
# =========================
# ROUNDED WHITE PANEL
# =========================

radius = 12

shape = page.new_shape()

x0 = margin
y0 = margin
x1 = PAGE_WIDTH - margin
y1 = PAGE_HEIGHT - margin

# Draw rounded rectangle manually
shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
shape.finish(
    fill=(1, 1, 1),
    color=(0.7, 0.7, 0.7),
    width=1
)

shape.commit()
# =========================
# 🖼️ HEADER LOGO (REAL IMAGE)
# =========================

page.insert_image(
    fitz.Rect(240, 30, 355, 110),
    filename="header_img.png",
    keep_proportion=True
)

# =========================
# HEADER TEXT
# =========================
page.insert_textbox(
    fitz.Rect(50, 100, 545, 200),
    """MINISTÉRIO DA EDUCAÇÃO
INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO CEARÁ
CAMPUS DE MARACANAÚ
COORDENAÇÃO DE EXTENSÃO
AV. PARQUE CENTRAL S/N (DISTRITO INDUSTRIAL I), MARACANAÚ""",
    fontsize=11,
    fontname="helv",  # 🔥 force built-in font
    align=1
)

# =========================
# TITLE (CORRECT POSITION)
# =========================

page.insert_textbox(
    fitz.Rect(50, 200, 545, 240),  # 👈 sits between header and body
    "CERTIFICADO",
    fontsize=20,
    fontname="helv",
    align=1
)

# =========================
# BODY (FIXED - SIMPLE & CLEAN)
# =========================

body_text = """Certificamos que João Victor Costa Pereira da Silva participou do(a) Semana 0 da Ciência da Computação do Instituto Federal de Educação, Ciência e Tecnologia do Ceará, com carga horária de 10000000000000 horas no(s) dia(s) 01, 02 e 03 de Março de 2026."""

page.insert_textbox(
    fitz.Rect(80, 280, 515, 400),  # controls width & wrapping
    body_text,
    fontsize=12,
    fontname="helv",
    align=1  # centered
)
# =========================
# DATE (FIXED)
# =========================

date_text = "Fortaleza, 10 de Março de 2026"

date_rect = fitz.Rect(80, 420, 515, 450)  # adjust vertical position here

page.insert_textbox(
    date_rect,
    date_text,
    fontsize=10,
    fontname="helv",
    align=2  # right aligned
)

# =========================
# SIGNATURES (FIXED)
# =========================

sig_line_y = 520  # vertical position of signature lines

# LEFT signature line
page.draw_line((120, sig_line_y), (280, sig_line_y), width=1)

page.insert_textbox(
    fitz.Rect(80, sig_line_y + 10, 320, sig_line_y + 40),
    "Presidente do Centro Acadêmico do Curso",
    fontsize=10,
    fontname="helv",
    align=1
)

# RIGHT signature line
page.draw_line((320, sig_line_y), (480, sig_line_y), width=1)

page.insert_textbox(
    fitz.Rect(320, sig_line_y + 10, 480, sig_line_y + 40),
    "Coordenador do Curso",
    fontsize=10,
    fontname="helv",
    align=1
)
# =========================
# FOOTER (FIXED PERFECTLY)
# =========================

footer_margin_bottom = 20

# Sizes
img1_height = 30   # bottom logo
img0_size = 90     # top logo MUST be square

spacing = 15

center_x = PAGE_WIDTH / 2
img1_width = 140  # 🔥 increase this
img1_height = 45  # slightly taller

footer_img_1_rect = fitz.Rect(
    center_x - img1_width / 2,
    PAGE_HEIGHT - margin - footer_margin_bottom - img1_height,
    center_x + img1_width / 2,
    PAGE_HEIGHT - margin - footer_margin_bottom
)
page.insert_image(
    footer_img_1_rect,
    filename="footer_img_1.png",
    keep_proportion=True
)

# --- Top image (footer_img_0) (FIXED: square box) ---
footer_img_0_rect = fitz.Rect(
    center_x - img0_size/2,
    footer_img_1_rect.y0 - spacing - img0_size,
    center_x + img0_size/2,
    footer_img_1_rect.y0 - spacing
)

page.insert_image(
    footer_img_0_rect,
    filename="footer_img_0.png",
    keep_proportion=True
)
# =========================
# SAVE
# =========================

doc.save("certificado_final_com_imagens.pdf")

print("Certificado com imagens pronto!")