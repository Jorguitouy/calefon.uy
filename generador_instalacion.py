import google.generativeai as genai
import os
import json
import time
import urllib.parse
import unidecode

# --- ⚙️ CONFIGURACIÓN OBLIGATORIA ⚙️ ---
GOOGLE_API_KEY = "AIzaSyD1dGRLMfot_aXriZKx-N8ciETqvNByI18"
NOMBRE_EMPRESA = "calefon.uy"
URL_BASE = "https://calefon.uy"

# --- LISTA DE MARCAS PARA GENERAR PÁGINAS ---
MARCAS = [
    "Ariston", "Atlantic", "Beusa", "Bosch", "Bronx", "Brilliant", "Collerati", 
    "Cyprium", "Delne", "Dikler", "Eldom", "Enxuta", "Fagor", "Ganim", "Geloso", 
    "Hyundai", "Ideal", "Ima", "James", "Joya", "Kroser", "Midea", "Orion", 
    "Pacific", "Panavox", "Peabody", "Punktal", "Queen", "Rotel", "Sevan", 
    "Sirium", "Smartlife", "Steigleder", "Telefunken", "Tem", "Thermor", 
    "Thompson", "Ufesa", "Warners", "Wnr", "Xion", "Zero Watt"
]

# --- CONFIGURACIÓN DE SEGURIDAD ---
safety_settings = {
    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE', 'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
}

# --- SCRIPT ---

def crear_slug(texto):
    sin_acentos = unidecode.unidecode(texto)
    return ''.join(c for c in sin_acentos.lower().replace(' ', '-') if c.isalnum() or c == '-')

print("🚀 Iniciando generador de páginas de INSTALACIÓN...")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"❌ Error de configuración de la API: {e}\nVerifica que tu clave de API sea correcta.")
    exit()

try:
    with open('plantilla-instalacion.html', 'r', encoding='utf-8') as f:
        contenido_plantilla = f.read()
except FileNotFoundError:
    print("❌ Error: No se encontró 'plantilla-instalacion.html'. Asegúrate de que el archivo de plantilla exista en la misma carpeta.")
    exit()

model = genai.GenerativeModel('models/gemini-pro-latest')

# --- DEFINIR TAREAS DE GENERACIÓN ---
tareas = [{'marca': None, 'filename': 'instalacion-calefones.html'}] # Tarea para la página principal
for marca in MARCAS:
    tareas.append({'marca': marca, 'filename': f"instalacion-{crear_slug(marca)}.html"})

for tarea in tareas:
    marca = tarea['marca']
    nombre_archivo = tarea['filename']
    
    if marca:
        print(f"\n▶️  Generando contenido para la marca: {marca}...")
        contexto = f"de la marca {marca}"
        keywords_primarias = f"- instalacion de calefones {marca}\n- instalar calefon {marca}\n- colocacion de calefones {marca}"
        keywords_secundarias = f"- instalador de calefones {marca}\n- cambiar calefon {marca}\n- precio instalacion calefon {marca}"
        h1_ejemplo = f"Instalación Profesional de Calefones {marca} en Montevideo"
        subtitulo_ejemplo = f"Técnicos matriculados para la instalación segura y garantizada de su nuevo calefón {marca}. Proteja su inversión y la seguridad de su hogar."
    else:
        print(f"\n▶️  Generando contenido para la página principal de Instalación (Montevideo)...")
        contexto = "en Montevideo"
        keywords_primarias = "- instalacion de calefones en Montevideo\n- instalar calefon en Montevideo\n- colocacion de calefones"
        keywords_secundarias = "- instalador de calefones matriculado\n- cambiar calefon\n- precio instalacion calefon Montevideo"
        h1_ejemplo = "Instalación Profesional de Calefones en Montevideo"
        subtitulo_ejemplo = "Técnicos matriculados para una instalación segura y garantizada. Proteja su nuevo calefón y la seguridad de su hogar."

    prompt = f"""
    Actúa como un experto redactor SEO y copywriter especializado en servicios para el hogar en Uruguay.
    Tu objetivo es generar el contenido completo para una página web sobre "Instalación de Calefones {contexto}".
    El contenido debe ser persuasivo, enfocado en la seguridad y profesionalismo, y optimizado para SEO integrando las keywords asignadas.

    **REQUISITOS PARA ESTA PÁGINA:**
    - **Keywords Primarias (para H1/H2/H3):** {keywords_primarias}
    - **Keywords Secundarias (para el cuerpo del texto):** {keywords_secundarias}
    - **Instrucciones:** El contenido debe explicar los riesgos de una mala instalación (fugas, problemas eléctricos, pérdida de garantía) y por qué es crucial contratar a un técnico matriculado. El llamado a la acción principal es cotizar el servicio por WhatsApp.

    Devuelve tu respuesta EXCLUSIVAMENTE en formato JSON con las siguientes claves:

    ### CONTENIDO Y METADATOS ###
    - "meta_title": "Título SEO (50-60 chars) con keywords. Ej: {h1_ejemplo} | Garantía y Seguridad"
    - "meta_description": "Meta descripción (140-155 chars) persuasiva con keywords y CTA."
    - "meta_keywords": "4-5 keywords long-tail relevantes."
    - "titulo_h1": "Encabezado H1 potente y optimizado. Ej: {h1_ejemplo}"
    - "subtitulo_hero": "Subtítulo que destaque la seguridad y profesionalismo. Ej: {subtitulo_ejemplo}"
    - "texto_cta_principal": "Texto para el botón principal de WhatsApp. Ej: Cotizar Instalación Ahora"
    - "titulo_beneficios_h2": "Título H2 para la sección de beneficios. Ej: ¿Por Qué Elegir una Instalación Profesional?"
    - "beneficio_1_titulo": "Título para el Beneficio 1 (Seguridad). Ej: Seguridad Eléctrica y de Plomería"
    - "beneficio_1_texto": "Texto sobre la importancia de una conexión segura para evitar riesgos."
    - "beneficio_2_titulo": "Título para el Beneficio 2 (Garantía). Ej: Validez de la Garantía del Fabricante"
    - "beneficio_2_texto": "Texto explicando que una mala instalación anula la garantía del calefón nuevo."
    - "beneficio_3_titulo": "Título para el Beneficio 3 (Rendimiento). Ej: Rendimiento y Eficiencia Energética"
    - "beneficio_3_texto": "Texto sobre cómo una buena instalación asegura el consumo óptimo de energía."
    - "beneficio_4_titulo": "Título para el Beneficio 4 (Durabilidad). Ej: Mayor Vida Útil del Equipo"
    - "beneficio_4_texto": "Texto explicando que una instalación correcta previene averías prematuras."
    - "titulo_proceso_h2": "Título H2 para la sección del proceso. Ej: Nuestro Proceso de Instalación en 3 Pasos"
    - "proceso_1_titulo": "Título para el Paso 1. Ej: Contacto y Cotización"
    - "proceso_1_texto": "Texto del paso 1, enfocado en la cotización por WhatsApp."
    - "proceso_2_titulo": "Título para el Paso 2. Ej: Coordinación y Visita"
    - "proceso_2_texto": "Texto del paso 2, sobre agendar la visita."
    - "proceso_3_titulo": "Título para el Paso 3. Ej: Instalación y Verificación"
    - "proceso_3_texto": "Texto del paso 3, explicando la instalación y prueba final."
    - "subtitulo_nosotros_h3": "Subtítulo H3 para 'Sobre Nosotros'. Ej: Expertos en Instalaciones Seguras"
    - "parrafo_nosotros_1": "Primer párrafo de 'Sobre Nosotros' enfocado en la experiencia en instalaciones."
    - "parrafo_nosotros_2": "Segundo párrafo enfocado en la tranquilidad del cliente y el profesionalismo."
    - "alt_img_nosotros": "Texto ALT para la imagen de 'Sobre Nosotros', con keywords."
    - "testimonio_1_texto": "Crea un testimonio de un cliente satisfecho con la instalación de su calefón."
    - "testimonio_1_autor": "Nombre y apellido del cliente."
    - "testimonio_2_texto": "Crea otro testimonio sobre la prolijidad y rapidez del servicio de instalación."
    - "testimonio_2_autor": "Nombre y apellido de otro cliente."
    - "parrafo_cta_final": "Párrafo para el CTA final. Ej: ¿Listo para instalar su nuevo calefón con total seguridad y garantía?"
    - "texto_cta_final_boton": "Texto para el botón del CTA final. Ej: Pedir Cotización de Instalación"
    - "footer_about_texto": "Texto para la descripción del footer."
    - "faq_pregunta_1": "Pregunta 1 para la FAQ. Ej: ¿Instalan todas las marcas de calefones?"
    - "faq_respuesta_1": "Respuesta 1."
    - "faq_pregunta_2": "Pregunta 2. Ej: ¿Cuánto demora la instalación?"
    - "faq_respuesta_2": "Respuesta 2."
    - "faq_pregunta_3": "Pregunta 3. Ej: ¿Qué incluye el servicio de instalación?"
    - "faq_respuesta_3": "Respuesta 3."
    - "faq_pregunta_4": "Pregunta 4. Ej: ¿Necesito comprar algún material extra?"
    - "faq_respuesta_4": "Respuesta 4."
    """
    
    intentos = 0
    datos_generados = None
    while intentos < 3 and not datos_generados:
        try:
            print("   - Enviando solicitud a la IA (esto puede tardar)...")
            response = model.generate_content(prompt, safety_settings=safety_settings)
            
            print("   - Respuesta recibida. Procesando contenido...")
            texto_limpio = response.text.strip().replace('```json', '').replace('```', '')
            datos_generados = json.loads(texto_limpio)
        except Exception as e:
            intentos += 1
            print(f"   - ⚠️ Advertencia: Intento {intentos} fallido. Reintentando... ({e})")
            time.sleep(5)

    if datos_generados:
        try:
            contenido_final = contenido_plantilla
            
            # Reemplazar todos los datos generados por la IA
            for clave, valor in datos_generados.items():
                contenido_final = contenido_final.replace(f'{{{{{clave}}}}}', str(valor))
            
            # --- CONSTRUCCIÓN DEL SCHEMA ---
            canonical_url = f"{URL_BASE}/{nombre_archivo.replace('.html', '')}/"
            texto_whatsapp = urllib.parse.quote(f"Hola, quisiera cotizar una instalación de calefón {contexto}.")
            
            contenido_final = contenido_final.replace('{{canonical_url}}', canonical_url)
            contenido_final = contenido_final.replace('{{texto_whatsapp}}', texto_whatsapp)
            
            schema_completo = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "HomeAndConstructionBusiness",
                        "name": f"{NOMBRE_EMPRESA} - Instalación de Calefones {contexto}",
                        "image": f"{URL_BASE}/assets/images/banner-instalacion.webp",
                        "url": canonical_url,
                        "telephone": "+59896758200",
                        "priceRange": "$$",
                        "address": {"@type": "PostalAddress", "addressLocality": "Montevideo", "addressCountry": "UY"},
                        "areaServed": {"@type": "City", "name": "Montevideo"}
                    },
                    {
                        "@type": "Service",
                        "serviceType": f"Instalación de Calefones {contexto}",
                        "provider": {"@type": "HomeAndConstructionBusiness", "name": NOMBRE_EMPRESA},
                        "areaServed": {"@type": "City", "name": "Montevideo"},
                        "description": datos_generados.get('meta_description', ''),
                        "offers": {"@type": "Offer", "name": f"Cotización para Instalación de Calefón {contexto}", "price": "0", "priceCurrency": "UYU"}
                    },
                    {
                        "@type": "FAQPage",
                        "mainEntity": [
                            {"@type": "Question", "name": datos_generados.get('faq_pregunta_1'), "acceptedAnswer": {"@type": "Answer", "text": datos_generados.get('faq_respuesta_1')}},
                            {"@type": "Question", "name": datos_generados.get('faq_pregunta_2'), "acceptedAnswer": {"@type": "Answer", "text": datos_generados.get('faq_respuesta_2')}},
                            {"@type": "Question", "name": datos_generados.get('faq_pregunta_3'), "acceptedAnswer": {"@type": "Answer", "text": datos_generados.get('faq_respuesta_3')}},
                            {"@type": "Question", "name": datos_generados.get('faq_pregunta_4'), "acceptedAnswer": {"@type": "Answer", "text": datos_generados.get('faq_respuesta_4')}}
                        ]
                    }
                ]
            }
            if marca:
                schema_completo['@graph'][1]['brand'] = {"@type": "Brand", "name": marca}

            contenido_final = contenido_final.replace('{{json_ld_schema}}', json.dumps(schema_completo, ensure_ascii=False, indent=2))

            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(contenido_final)
            
            print(f"✅ Landing Page creada: {nombre_archivo}")
            time.sleep(20) # Pausa para no exceder los límites de la API
            
        except Exception as e:
            print(f"   - ❌ Error al procesar o guardar los datos: {e}")
    else:
        print(f"❌ Falló la generación de contenido después de 3 intentos.")

print("\n🎉 ¡Proceso de generación completado!")