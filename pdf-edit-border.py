import fitz

MARGIN = 20
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MIN_BOTTOM_GAP = 40

doc = fitz.open()
page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

font_regular = "helv"

margin = 20  # Size of the border frame

# =========================
# 🖼️ BACKGROUND (ABSTRACT BORDER IMAGE)
# =========================

# Insert the image to cover the full page. 
# Make sure "abstract_border.png" is in the same directory as this script.
page.insert_image(
    fitz.Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT),
    filename="border.png",
    keep_proportion=False  # Stretches the image to fill the page perfectly
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

# Draw rounded rectangle manually (this sits on top of the background image)
shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
shape.finish(
    fill=(1, 1, 1),        # White interior
    color=(0.7, 0.7, 0.7), # Light gray border line
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
    fontname="helv",  
    align=1
)

# =========================
# TITLE (CORRECT POSITION)
# =========================

page.insert_textbox(
    fitz.Rect(50, 200, 545, 240),  
    "CERTIFICADO",
    fontsize=20,
    fontname="helv",
    align=1
)

# =========================
# BODY (FIXED - SIMPLE & CLEAN)
# =========================

body_text = """Certificamos que ______________________________ participou do(a) Semana 0 da Ciência da Computação do Instituto Federal de Educação, Ciência e Tecnologia do Ceará, com carga horária de ___ horas no(s) dia(s) 03, 04 e 05 de Março de 2026."""

page.insert_textbox(
    fitz.Rect(80, 280, 515, 400),  
    body_text,
    fontsize=12,
    fontname="helv",
    align=1  
)

# =========================
# DATE (FIXED)
# =========================

date_text = "Maracanaú, 24 de Março de 2026"

date_rect = fitz.Rect(80, 420, 515, 450)  

page.insert_textbox(
    date_rect,
    date_text,
    fontsize=10,
    fontname="helv",
    align=2  
)

# =========================
# SIGNATURES (FIXED)
# =========================

sig_line_y = 520  

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
img0_size = 90     
spacing = 15
center_x = PAGE_WIDTH / 2
img1_width = 140  
img1_height = 45  

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

doc.save("certificado_final_com_borda.pdf")

print("Certificado com borda abstrata pronto!")