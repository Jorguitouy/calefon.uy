import os
import json
import time
import unidecode

# Import condicional de la API (solo se usará si no estamos en modo mock)
try:
    import google.generativeai as genai  # type: ignore
except Exception:
    genai = None

# --- ⚙️ CONFIGURACIÓN OBLIGATORIA ⚙️ ---
GOOGLE_API_KEY = "AIzaSyD1dGRLMfot_aXriZKx-N8ciETqvNByI18"
NOMBRE_DEL_SERVICIO = "Reparación de Calefones por Marca"

# --- LISTA DE MARCAS ---
marcas = [
    "Ariston", "Atlantic", "Beusa", "Bosch", "Brillant", "Bronx", "Collerati", "Cyprium",
    "Delne", "Dikler", "Eldom", "Enxuta", "Fagor", "Ganim", "Geloso", "Hyundai", "Ideal", "Ima",
    "James", "Joya", "Kroser", "Midea", "Orion", "Pacific", "Panavox", "Peabody", "Punktal",
    "Queen", "Rotel", "Sevan", "Sirium", "Smartlife", "Steigleder", "Telefunken", "Tem", "Thermor",
    "Thompson", "Ufesa", "Warners", "Wnr", "Xion", "Zero Watt"
]

# --- CAMPOS CRÍTICOS PARA LA PLANTILLA DE MARCAS ---
campos_criticos = [
    'meta_title', 'meta_description', 'titulo_h1', 'subtitulo_hero',
    'titulo_seccion_servicios', 'titulo_seccion_problemas', 'titulo_seccion_nosotros',
    'texto_problema_no_calienta', 'texto_problema_no_enciende', 'texto_nosotros_1'
]

# --- CONFIGURACIÓN DE SEGURIDAD ---
safety_settings = {
    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE', 'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE', 'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
}


def crear_slug(texto: str) -> str:
    sin_acentos = unidecode.unidecode(texto)
    slug = (
        sin_acentos
        .strip()
        .lower()
        .replace(' / ', '-')
        .replace('/', '-')
        .replace(' ', '-')
    )
    while '--' in slug:
        slug = slug.replace('--', '-')
    return ''.join(c for c in slug if c.isalnum() or c == '-')

USE_MOCK = os.getenv("USE_MOCK_BRAND_GEN", "0") == "1"

print("Iniciando generador de landing pages por marca...")
if not USE_MOCK:
    if genai is None:
        print("Error: La librería 'google-generativeai' no está disponible. Instálala con 'pip install google-generativeai' o ejecuta en modo mock (USE_MOCK_BRAND_GEN=1).")
        exit()
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        print(f"Error de configuración de la API: {e}\nVerifica que tu clave de API sea correcta o ejecuta en modo mock (USE_MOCK_BRAND_GEN=1).")
        exit()

# Leer plantilla de marcas
try:
    with open('plantilla-marcas.html', 'r', encoding='utf-8') as f:
        contenido_plantilla = f.read()
except FileNotFoundError:
    print("Error: No se encontró 'plantilla-marcas.html'. Asegúrate de que el archivo esté en la misma carpeta.")
    exit()

model = None if USE_MOCK else genai.GenerativeModel('models/gemini-pro-latest')

for marca in marcas:
    print(f"\nGenerando contenido para la marca: {marca}...")

    prompt = f"""
    Actúa como un estratega de marketing digital y copywriter experto en SEO para servicios técnicos en Uruguay.
    Tu misión es generar el contenido completo para una landing page de "{NOMBRE_DEL_SERVICIO}" para la marca "{marca}".
    El objetivo es persuadir al usuario para que contacte por WhatsApp o teléfono y obtener un presupuesto estimado gratis y sin compromiso.

    DIRECTIVAS CLAVE Y OBLIGATORIAS:
    1.  H1 ESTRICTO: Para "titulo_h1", ELIGE ALEATORIAMENTE UNA de estas 4 plantillas e inclúyela con la marca:
        - "Service de Calefones {marca}. ¡Lo reparamos Hoy Mismo!"
        - "Técnico de Calefones {marca}. Reparación en el Día"
        - "Reparación de Calefones {marca}. Solución Inmediata"
        - "Arreglo de Calefones {marca}. Servicio Urgente"
    2.  H2 OPTIMIZADOS: Los títulos de sección deben incluir variaciones de las keywords con la marca.
    3.  Keywords: Integra naturalmente "reparación de calefones", "service técnico", "arreglo de calefón" y "técnico de calefones".
    4.  Garantía: Menciona que los trabajos tienen "garantía por escrito" o son "trabajos garantizados", pero NUNCA un período de tiempo.
    5.  Urgencia: Transmite urgencia e inmediatez.
    6.  Tono: Profesional y cercano, que genere confianza.

    Devuelve EXCLUSIVAMENTE JSON con estas claves:

    ### SEO & METADATOS ###
    - "meta_title": "Título SEO (50-60). Ej: Service de Calefones {marca} | Reparación Urgente"
    - "meta_description": "Meta descripción (140-155) con keywords y CTA. Ej: Service técnico para calefones {marca}. Reparación en el día. Presupuesto gratis por WhatsApp. ¡Llámenos al 096 758 200!"
    - "og_title": "Título para redes sociales"
    - "og_description": "Descripción para redes sociales"

    ### CONTENIDO PRINCIPAL ###
    - "titulo_h1": "Uno de los 4 modelos especificados, con {marca}"
    - "subtitulo_hero": "Subtítulo persuasivo (2-3 oraciones). Ej: Atendemos todas las capacidades de la marca {marca}. Pida presupuesto GRATIS por WhatsApp."
    - "texto_hero_adicional": "Texto adicional (1-2 oraciones). Ej: Equipo de técnicos especializados en {marca} para solución rápida y garantizada."

    ### SECCIONES ###
    - "titulo_seccion_servicios": "H2 para servicios (con {marca}). Ej: Servicio técnico de calefones {marca}"
    - "titulo_seccion_problemas": "H2 para problemas comunes (con {marca}). Ej: Arreglo de calefones {marca}"
    - "titulo_seccion_nosotros": "H2 para 'Sobre nosotros' (con {marca}). Ej: Expertos en reparación de calefones {marca}"

    ### TEXTOS DE PROBLEMAS (2-3 oraciones cada uno) ###
    - "texto_problema_no_calienta": "Descripción persuasiva del problema 'Luz prende, no calienta' enfocada en equipos {marca}. Terminar con CTA para contactar."
    - "texto_problema_no_enciende": "Descripción para 'No prende, ni calienta' en {marca}. Mencionar seguridad y CTA."
    - "texto_problema_salta_llave": "Descripción para 'Hace saltar la llave' en {marca}. Alerta de seguridad y CTA urgente."
    - "texto_problema_pierde_agua": "Descripción para 'El calefón pierde agua' en {marca}. Aclarar que no siempre es tanque roto y CTA."
    - "texto_problema_agua_tibia": "Descripción para 'Agua siempre sale tibia' en {marca}. Mencionar consumo y CTA."
    - "texto_problema_no_corta": "Descripción para 'Calienta continuamente' en {marca}. Seguridad grave y CTA urgente."

    ### SECCIÓN NOSOTROS (4 párrafos de 3-4 oraciones) ###
    - "texto_nosotros_1": "Frustración del cliente y cómo nacimos para solucionar eso. Enfatizar misión clara: servicio rápido y profesional."
    - "texto_nosotros_2": "Eficacia: reparación el mismo día a domicilio, margen horario y especialización 100% en calefones eléctricos."
    - "texto_nosotros_3": "Transparencia: empresa registrada en BPS y DGI, repuestos originales y garantía real."
    - "texto_nosotros_4": "CTA: contactar al 096 758 200 por llamada o WhatsApp para presupuesto sin compromiso."

    ### FAQS (2-3 oraciones, naturales y persuasivas) ###
    - "faq_respuesta_no_calienta"
    - "faq_respuesta_salta_llave"
    - "faq_respuesta_no_enciende"
    - "faq_respuesta_gotea"
    - "faq_respuesta_poca_presion"
    - "faq_respuesta_agua_tibia"

    ### FAQS ADICIONALES (SECCIÓN 2) ###
    - "faq2_respuesta_instalacion": "4-5 oraciones. Confirmar instalaciones de todas las marcas, normas técnicas, verificación completa y opción de retirar el antiguo. CTA para agendar al 096 758 200."
    - "faq2_respuesta_marcas": "3 oraciones. Confirmar experiencia en marcas comercializadas en Uruguay (incluir {marca} como ejemplo). CTA 096 758 200."
    - "faq2_respuesta_garantia": "4-5 oraciones. Diagnóstico profesional y trabajo garantizado. Garantía específica según reparación (sin período). Cubre mano de obra y repuestos. Empresa registrada en BPS y DGI."

    ### SERVICIOS (¿QUÉ HACEMOS?) - 2 oraciones cada uno ###
    - "texto_servicio_instalacion"
    - "texto_servicio_mantenimiento"
    - "texto_servicio_reparacion"
    - "texto_servicio_asesoramiento"

    ### TESTIMONIOS (3-4 oraciones, naturales) ###
    - "testimonio_1_texto"
    - "testimonio_1_autor"
    - "testimonio_2_texto"
    - "testimonio_2_autor"
    - "testimonio_3_texto"
    - "testimonio_3_autor"

    ### FOOTER ###
    - "footer_descripcion": "Texto (2-3 oraciones) que mencione riesgos eléctricos y de presión, necesidad de personal especializado, y que Calefon.UY se dedica exclusivamente a calefones con trabajos garantizados. Enfocado a marca {marca}."
    """

    # Intentos con reintentos ante bloqueos o respuestas incompletas
    datos_generados = None
    if USE_MOCK:
        # Contenido mínimo pero coherente para validar reemplazos y estructura
        datos_generados = {
            "meta_title": f"Service de Calefones {marca} | Reparación Urgente",
            "meta_description": f"Técnicos especialistas en calefones {marca}. Reparación en el día. Presupuesto por WhatsApp al 096 758 200.",
            "og_title": f"Reparación de Calefones {marca}",
            "og_description": f"Servicio técnico para calefones {marca} con trabajos garantizados.",
            "titulo_h1": f"Service de Calefones {marca}. ¡Lo reparamos Hoy Mismo!",
            "subtitulo_hero": f"Atendemos todas las capacidades de {marca}. Pida su presupuesto GRATIS.",
            "texto_hero_adicional": f"Equipo especializado en {marca} para solución rápida y segura.",
            "titulo_seccion_servicios": f"Servicio técnico de calefones {marca}",
            "titulo_seccion_problemas": f"Problemas comunes en calefones {marca}",
            "titulo_seccion_nosotros": f"Expertos en reparación de calefones {marca}",
            "texto_problema_no_calienta": f"Si la luz enciende pero no calienta en su {marca}, podemos resolverlo en el acto. Contáctenos para diagnóstico y presupuesto.",
            "texto_problema_no_enciende": f"Si su calefón {marca} no prende ni calienta, es importante revisarlo cuanto antes. Llámenos para asistencia urgente.",
            "texto_problema_salta_llave": f"Cuando un {marca} hace saltar la llave, podría ser una falla eléctrica. Nuestros técnicos lo solucionan con seguridad.",
            "texto_problema_pierde_agua": f"Una pérdida de agua en su {marca} no siempre implica tanque roto. Evaluamos y reparamos al mejor costo.",
            "texto_problema_agua_tibia": f"Si el agua siempre sale tibia en su {marca}, optimizamos el rendimiento y consumo para recuperar el confort.",
            "texto_problema_no_corta": f"Si su {marca} calienta continuamente y no corta, es una falla crítica. Atendemos con urgencia.",
            "texto_nosotros_1": f"Sabemos lo molesto que es quedarse sin agua caliente. Nacimos para dar respuestas rápidas y profesionales a usuarios de {marca}.",
            "texto_nosotros_2": f"Ofrecemos reparación el mismo día, en domicilio, con franjas horarias claras y especialización en calefones eléctricos.",
            "texto_nosotros_3": f"Somos empresa registrada (BPS y DGI), trabajamos con repuestos originales y brindamos trabajos garantizados.",
            "texto_nosotros_4": f"Escríbanos por WhatsApp o llámenos al 096 758 200 para un presupuesto orientativo sin compromiso.",
            "faq_respuesta_no_calienta": f"Generalmente es resistencia o termostato. Diagnosticamos su {marca} y resolvemos rápido.",
            "faq_respuesta_salta_llave": f"Puede haber fuga a tierra en la resistencia. Recomendamos detener el uso y solicitar revisión profesional.",
            "faq_respuesta_no_enciende": f"Chequeamos conexiones, termostato y resistencia de su {marca} para restaurar el funcionamiento.",
            "faq_respuesta_gotea": f"Una pérdida puede ser junta o válvula. Evaluamos su {marca} y proponemos la solución más conveniente.",
            "faq_respuesta_poca_presion": f"El sarro reduce caudal. Una limpieza profesional devuelve la presión adecuada.",
            "faq_respuesta_agua_tibia": f"Ajustamos o reemplazamos componentes para que su {marca} caliente correctamente.",
            "faq2_respuesta_instalacion": f"Sí, instalamos calefones de todas las marcas. Cumplimos normas técnicas, verificamos conexiones y dejamos funcionando. Podemos retirar el antiguo. Agende al 096 758 200.",
            "faq2_respuesta_marcas": f"Trabajamos con todas las marcas en Uruguay, incluyendo {marca}. Conocimiento técnico y reparación de calidad. Llame al 096 758 200.",
            "faq2_respuesta_garantia": f"Cada reparación comienza con diagnóstico y finaliza con trabajo garantizado. La cobertura depende del tipo de reparación y se informa antes de iniciar. Cubre mano de obra y repuestos. Empresa registrada en BPS y DGI.",
            "texto_servicio_instalacion": f"Instalamos o reemplazamos su calefón {marca} con precisión y seguridad según normativa.",
            "texto_servicio_mantenimiento": f"El mantenimiento anual de su {marca} previene fallas y optimiza el consumo energético.",
            "texto_servicio_reparacion": f"Somos especialistas en reparación de {marca}. Diagnóstico certero y solución en el acto.",
            "texto_servicio_asesoramiento": f"Le ayudamos a elegir el {marca} adecuado según su hogar y consumo para evitar problemas y gastos.",
            "testimonio_1_texto": f"Mi {marca} hacía saltar la llave y me quedé sin agua caliente. Vinieron el mismo día, explicaron todo y quedó perfecto.",
            "testimonio_1_autor": "Mariana Pérez",
            "testimonio_2_texto": f"El técnico conocía muy bien los {marca}. En media hora ya estaba solucionado y funcionando mejor que antes.",
            "testimonio_2_autor": "Gustavo Rodríguez",
            "testimonio_3_texto": f"Antes probé con otro servicio y no quedó bien. Con Calefon.UY fue rápido, claro y sin sorpresas en el precio.",
            "testimonio_3_autor": "Laura Martínez",
            "footer_descripcion": f"El calefón implica riesgos eléctricos y de presión. Confíe su {marca} a técnicos especializados. En Calefon.UY nos dedicamos exclusivamente a calefones con trabajos garantizados."
        }
    else:
        intentos = 0
        while intentos < 3 and not datos_generados:
            try:
                print("   - Enviando solicitud a la IA (esto puede tardar hasta 90 segundos)...")
                response = model.generate_content(prompt, safety_settings=safety_settings)

                print("   - Respuesta recibida. Verificando integridad...")
                if response.parts:
                    texto_limpio = response.text.strip().replace('```json', '').replace('```', '')
                    temp_datos = json.loads(texto_limpio)

                    campos_faltantes = [c for c in campos_criticos if c not in temp_datos or not temp_datos[c]]
                    if campos_faltantes:
                        print(f"   - Verificación fallida. Faltan campos: {', '.join(campos_faltantes)}. Reintentando...")
                        raise ValueError("Respuesta incompleta de la IA")

                    print("   - Verificación exitosa. Contenido completo.")
                    datos_generados = temp_datos
                else:
                    print("   - Advertencia: La respuesta fue bloqueada por el filtro de seguridad de la IA. Reintentando...")
                    raise ValueError("Respuesta bloqueada")

            except Exception as e:
                intentos += 1
                print(f"   - Advertencia: Intento {intentos} fallido para {marca}. Reintentando... ({e})")
                time.sleep(5)

        if not datos_generados:
            print(f"Error: Falló la generación de contenido para {marca} después de 3 intentos.")
            continue

    try:
        # Fallbacks mínimos
        datos_generados.setdefault('og_title', datos_generados.get('meta_title', f"Service de Calefones {marca}"))
        datos_generados.setdefault('og_description', datos_generados.get('meta_description', ''))

        contenido_final = contenido_plantilla

        marca_slug = crear_slug(marca)

        # Primero reemplazar los datos generados por la IA
        for clave, valor in datos_generados.items():
            contenido_final = contenido_final.replace(f'{{{{{clave}}}}}', str(valor))

        # Luego reemplazar placeholders de marca
        contenido_final = contenido_final.replace('{{marca_slug}}', marca_slug)
        contenido_final = contenido_final.replace('{{marca}}', marca)

        # Guardar directamente en la carpeta raíz con el nombre de la marca.
        # Usamos el slug (minúsculas, sin acentos, espacios como guiones) para asegurar compatibilidad con el sistema de archivos.
        # Ejemplos: "Bronx" -> bronx.html, "James" -> james.html, "Zero Watt" -> zero-watt.html
        ruta_archivo = f"{marca_slug}.html"
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_final)

        print(f"Landing Page creada: {ruta_archivo}")
    except Exception as e:
        print(f"   - Error al procesar o guardar los datos para {marca}: {e}")

print("\nProceso completado. Landing pages por marca generadas.")
