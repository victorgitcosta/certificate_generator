import fitz
import re
import os

# =========================
# SETTINGS
# =========================
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN = 20
CSV_FILE = "certificates/attendes.txt"
OUTPUT_DIR = "certificates"

# Ensure the output directory exists, creating it if necessary
os.makedirs(OUTPUT_DIR, exist_ok=True)

lista_participantes = []
# Open the CSV file and read the names
try:
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        # Skip the first line (header: name,hrs,email)
        next(file, None)
        
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Split by comma and check if we have at least name and hours
            parts = line.split(",")
            if len(parts) >= 2:
                nome = parts[0].strip()
                horas = parts[1].strip()
                # We ignore parts[2] (the email) entirely
                
                lista_participantes.append({
                    "nome": nome,
                    "horas": horas
                })
            else:
                print(f"Aviso: linha pulada por formato incorreto: '{line}'")
except FileNotFoundError:
    print(f"Erro: O arquivo '{CSV_FILE}' não foi encontrado.")
    exit()

# =========================
# LOOP THROUGH NAMES
# =========================
for participante in lista_participantes:
    nome = participante["nome"]
    horas = participante["horas"]
    
    # Create a new blank PDF document for EACH person
    doc = fitz.open()
    
    # Create a new page
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

    # 🖼️ BACKGROUND (ABSTRACT BORDER IMAGE)
    page.insert_image(
        fitz.Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT),
        filename="border.png",
        keep_proportion=False  
    )

    # ROUNDED WHITE PANEL
    radius = 12
    shape = page.new_shape()
    x0 = MARGIN
    y0 = MARGIN
    x1 = PAGE_WIDTH - MARGIN
    y1 = PAGE_HEIGHT - MARGIN

    # Draw standard rectangle
    shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
    shape.finish(
        fill=(1, 1, 1),        
        color=(0.7, 0.7, 0.7), 
        width=1
    )
    shape.commit()

    # 🖼️ HEADER LOGO
    page.insert_image(
        fitz.Rect(240, 30, 355, 110),
        filename="header_img.png",
        keep_proportion=True
    )

    # HEADER TEXT
    page.insert_textbox(
        fitz.Rect(50, 100, 545, 200),
        """MINISTÉRIO DA EDUCAÇÃO
INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO CEARÁ
CAMPUS DE MARACANAÚ
COORDENAÇÃO DE EXTENSÃO
AV. PARQUE CENTRAL S/N (DISTRITO INDUSTRIAL I), MARACANAÚ""",
        fontsize=9,
        fontname="hebo",  
        align=1
    )

    # TITLE
    page.insert_textbox(
        fitz.Rect(50, 206, 545, 240),  
        "CERTIFICADO",
        fontsize=20,
        fontname="helv",
        align=1
    )

    # =========================
    # BODY (USING HTML FOR BOLD TEXT)
    # =========================
    html_body = f"""
    <div style="font-family: Helvetica; font-size: 14pt; text-align: center; line-height: 1.6;">
        Certificamos que <b>{nome}</b> participou do(a) 
        <b>Semana 0 da Ciência da Computação</b> do Instituto Federal de Educação, 
        Ciência e Tecnologia do Ceará Campus Maracanaú, com carga horária de <b>{horas} horas</b> 
        no(s) dia(s) <b>03, 04 e 05 de Março de 2026</b>.
    </div>
    """

    page.insert_htmlbox(
        fitz.Rect(80, 280, 515, 400),  
        html_body
    )

    # DATE
    date_text = "Maracanaú, 24 de Março de 2026"
    date_rect = fitz.Rect(80, 420, 515, 450)  

    page.insert_textbox(
        date_rect,
        date_text,
        fontsize=9,
        fontname="helv",
        align=2  
    )

    # =========================
    # SIGNATURES
    # =========================
    sig_line_y = 520  

    # --- LEFT signature line ---
    page.insert_image(
        fitz.Rect(117, 450, 280, 565), 
        filename="ass_ca.png",
        keep_proportion=True
    )

    page.draw_line((120, sig_line_y), (280, sig_line_y), width=1)
    
    page.insert_textbox(
        fitz.Rect(80, sig_line_y + 10, 320, sig_line_y + 40),
        "Presidente do Centro Acadêmico do Curso",
        fontsize=10,
        fontname="helv",
        align=1
    )

    # --- RIGHT signature line ---
    page.insert_image(
        fitz.Rect(317, 450, 480, 565), 
        filename="ass_coord.png",
        keep_proportion=True
    )

    page.draw_line((320, sig_line_y), (480, sig_line_y), width=1)
    page.insert_textbox(
        fitz.Rect(320, sig_line_y + 10, 480, sig_line_y + 40),
        "Coordenador do Curso",
        fontsize=10,
        fontname="helv",
        align=1
    )

    # FOOTER
    footer_margin_bottom = 20
    img0_size = 90    
    spacing = 15
    center_x = PAGE_WIDTH / 2
    img1_width = 140  
    img1_height = 45  

    footer_img_1_rect = fitz.Rect(
        center_x - img1_width / 2,
        PAGE_HEIGHT - MARGIN - footer_margin_bottom - img1_height,
        center_x + img1_width / 2,
        PAGE_HEIGHT - MARGIN - footer_margin_bottom
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
    # SAVE INDIVIDUAL FILE
    # =========================
    # Clean the name to make it a safe filename (removes invalid characters)
    safe_filename = re.sub(r'[\\/*?:"<>|]', "", nome)
    
    # Save the file inside the OUTPUT_DIR folder
    output_pdf = os.path.join(OUTPUT_DIR, f"{safe_filename}.pdf")
    
    doc.save(output_pdf)
    doc.close() # Free up memory
    print(f"Certificado gerado: {output_pdf}")

print(f"\nSucesso! Gerados {len(lista_participantes)} certificados na pasta '{OUTPUT_DIR}'.")