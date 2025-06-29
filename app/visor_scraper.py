from visor_scraper import capturar_mapa

# rutas de salida
mapa_vulner = os.path.join(output_folder, "mapa_vulnerabilidad.png")
capturar_mapa(municipio, "Tipología de vulnerabilidad", mapa_vulner)

# luego inserta esa imagen en el documento (con python-docx)
doc.add_picture(mapa_vulner, width=Inches(6))
