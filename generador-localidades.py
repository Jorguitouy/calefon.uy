import google.generativeai as genai
import os
import json
import time
import urllib.parse
import unidecode

# --- ⚙️ CONFIGURACIÓN OBLIGATORIA ⚙️ ---
GOOGLE_API_KEY = "AIzaSyD1dGRLMfot_aXriZKx-N8ciETqvNByI18"
NOMBRE_DEL_SERVICIO = "Reparación de Calefones"

# --- LISTA DE UBICACIONES ---
ubicaciones = [
    # Barrios de Montevideo
    {'nombre': 'Aguada', 'departamento': 'Montevideo'}, {'nombre': 'Aires Puros', 'departamento': 'Montevideo'},
    {'nombre': 'Atahualpa', 'departamento': 'Montevideo'}, {'nombre': 'Bañados de Carrasco', 'departamento': 'Montevideo'},
    {'nombre': 'Barrio Sur', 'departamento': 'Montevideo'}, {'nombre': 'Belvedere', 'departamento': 'Montevideo'},
    {'nombre': 'Bolívar', 'departamento': 'Montevideo'}, {'nombre': 'Brazo Oriental', 'departamento': 'Montevideo'},
    {'nombre': 'Buceo', 'departamento': 'Montevideo'}, {'nombre': 'Capurro', 'departamento': 'Montevideo'},
    {'nombre': 'Bella Vista', 'departamento': 'Montevideo'}, {'nombre': 'Arroyo Seco', 'departamento': 'Montevideo'},
    {'nombre': 'Carrasco', 'departamento': 'Montevideo'}, {'nombre': 'Carrasco Norte', 'departamento': 'Montevideo'},
    {'nombre': 'Casabó', 'departamento': 'Montevideo'}, {'nombre': 'Pajas Blancas', 'departamento': 'Montevideo'},
    {'nombre': 'Casavalle', 'departamento': 'Montevideo'}, {'nombre': 'Castro', 'departamento': 'Montevideo'},
    {'nombre': 'Castellana', 'departamento': 'Montevideo'}, {'nombre': 'Centro', 'departamento': 'Montevideo'},
    {'nombre': 'Cerrito de la Victoria', 'departamento': 'Montevideo'}, {'nombre': 'Cerro', 'departamento': 'Montevideo'},
    {'nombre': 'Ciudad Vieja', 'departamento': 'Montevideo'}, {'nombre': 'Colón Centro y Noroeste', 'departamento': 'Montevideo'},
    {'nombre': 'Colón Sudeste', 'departamento': 'Montevideo'}, {'nombre': 'Abayubá', 'departamento': 'Montevideo'},
    {'nombre': 'Conciliación', 'departamento': 'Montevideo'}, {'nombre': 'Cordón', 'departamento': 'Montevideo'},
    {'nombre': 'Flor de Maroñas', 'departamento': 'Montevideo'}, {'nombre': 'Goes', 'departamento': 'Montevideo'},
    {'nombre': 'Ituzaingó', 'departamento': 'Montevideo'}, {'nombre': 'Jacinto Vera', 'departamento': 'Montevideo'},
    {'nombre': 'Jardines del Hipódromo', 'departamento': 'Montevideo'}, {'nombre': 'La Blanqueada', 'departamento': 'Montevideo'},
    {'nombre': 'La Comercial', 'departamento': 'Montevideo'}, {'nombre': 'La Figurita', 'departamento': 'Montevideo'},
    {'nombre': 'La Paloma', 'departamento': 'Montevideo'}, {'nombre': 'Tomkinson', 'departamento': 'Montevideo'},
    {'nombre': 'La Teja', 'departamento': 'Montevideo'}, {'nombre': 'Larrañaga', 'departamento': 'Montevideo'},
    {'nombre': 'Las Acacias', 'departamento': 'Montevideo'}, {'nombre': 'Las Canteras', 'departamento': 'Montevideo'},
    {'nombre': 'Lezica', 'departamento': 'Montevideo'}, {'nombre': 'Melilla', 'departamento': 'Montevideo'},
    {'nombre': 'Malvín', 'departamento': 'Montevideo'}, {'nombre': 'Malvín Norte', 'departamento': 'Montevideo'},
    {'nombre': 'Manga', 'departamento': 'Montevideo'}, {'nombre': 'Manga - Toledo Chico', 'departamento': 'Montevideo'},
    {'nombre': 'Maroñas', 'departamento': 'Montevideo'}, {'nombre': 'Parque Guaraní', 'departamento': 'Montevideo'},
    {'nombre': 'Mercado Modelo', 'departamento': 'Montevideo'}, {'nombre': 'Nuevo París', 'departamento': 'Montevideo'},
    {'nombre': 'Palermo', 'departamento': 'Montevideo'}, {'nombre': 'Parque Batlle', 'departamento': 'Montevideo'},
    {'nombre': 'Villa Dolores', 'departamento': 'Montevideo'}, {'nombre': 'Parque Rodó', 'departamento': 'Montevideo'},
    {'nombre': 'Paso de la Arena', 'departamento': 'Montevideo'}, {'nombre': 'Paso de las Duranas', 'departamento': 'Montevideo'},
    {'nombre': 'Peñarol', 'departamento': 'Montevideo'}, {'nombre': 'Lavalleja', 'departamento': 'Montevideo'},
    {'nombre': 'Piedras Blancas', 'departamento': 'Montevideo'}, {'nombre': 'Pocitos', 'departamento': 'Montevideo'},
    {'nombre': 'Prado', 'departamento': 'Montevideo'}, {'nombre': 'Nueva Savona', 'departamento': 'Montevideo'},
    {'nombre': 'Punta Carretas', 'departamento': 'Montevideo'}, {'nombre': 'Punta de Rieles', 'departamento': 'Montevideo'},
    {'nombre': 'Bella Italia', 'departamento': 'Montevideo'}, {'nombre': 'Punta Gorda', 'departamento': 'Montevideo'},
    {'nombre': 'Reducto', 'departamento': 'Montevideo'}, {'nombre': 'Sayago', 'departamento': 'Montevideo'},
    {'nombre': 'Tres Cruces', 'departamento': 'Montevideo'}, {'nombre': 'Tres Ombúes', 'departamento': 'Montevideo'},
    {'nombre': 'Pueblo Victoria', 'departamento': 'Montevideo'}, {'nombre': 'Unión', 'departamento': 'Montevideo'},
    {'nombre': 'Villa Española', 'departamento': 'Montevideo'}, {'nombre': 'Villa García', 'departamento': 'Montevideo'},
    {'nombre': 'Villa Muñoz', 'departamento': 'Montevideo'}, {'nombre': 'Retiro', 'departamento': 'Montevideo'},
    {'nombre': 'Villa del Cerro', 'departamento': 'Montevideo'},
    # Localidades de Canelones
    {'nombre': 'Ciudad de la Costa', 'departamento': 'Canelones'}, {'nombre': 'Barra de Carrasco', 'departamento': 'Canelones'},
    {'nombre': 'Parque Carrasco', 'departamento': 'Canelones'}, {'nombre': 'Shangrilá', 'departamento': 'Canelones'},
    {'nombre': 'San José de Carrasco', 'departamento': 'Canelones'}, {'nombre': 'Lagomar', 'departamento': 'Canelones'},
    {'nombre': 'Solymar', 'departamento': 'Canelones'}, {'nombre': 'El Pinar', 'departamento': 'Canelones'},
    {'nombre': 'Pando', 'departamento': 'Canelones'}, {'nombre': 'Barros Blancos', 'departamento': 'Canelones'},
    {'nombre': 'Progreso', 'departamento': 'Canelones'}, {'nombre': 'Canelones', 'departamento': 'Canelones'},
    {'nombre': 'Las Piedras', 'departamento': 'Canelones'}
]

# --- LISTA DE CAMPOS CRÍTICOS PARA LA NUEVA PLANTILLA ---
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

# --- SCRIPT ---

def crear_slug(texto):
    sin_acentos = unidecode.unidecode(texto)
    slug = sin_acentos.lower().replace(' / ', '-').replace(' ', '-').replace('--', '-')
    return ''.join(c for c in slug if c.isalnum() or c == '-')

print("🚀 Iniciando generador de landing pages...")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"❌ Error de configuración de la API: {e}\nVerifica que tu clave de API sea correcta.")
    exit()

try:
    with open('plantilla-nueva.html', 'r', encoding='utf-8') as f:
        contenido_plantilla = f.read()
except FileNotFoundError:
    print("❌ Error: No se encontró 'plantilla-nueva.html'. Asegúrate de que el archivo esté en la misma carpeta.")
    exit()

model = genai.GenerativeModel('models/gemini-pro-latest')

for lugar in ubicaciones:
    ubicacion = lugar['nombre']
    departamento = lugar['departamento']
    
    print(f"\n▶️  Generando contenido para: {ubicacion}, {departamento}...")
    
    prompt = f"""
    Actúa como un estratega de marketing digital y copywriter experto en SEO hiperlocal, especializado en servicios de urgencia en Uruguay.
    Tu misión es generar el contenido completo para una landing page sobre "{NOMBRE_DEL_SERVICIO}" en "{ubicacion}, {departamento}".
    El objetivo es persuadir al usuario para que contacte por WhatsApp o teléfono para obtener un presupuesto estimado gratis y sin compromiso.

    DIRECTIVAS CLAVE Y OBLIGATORIAS:
    1.  **H1 ESTRICTO:** Para la clave "titulo_h1", DEBES ELEGIR ALEATORIAMENTE UNA de las siguientes 4 plantillas y completarla:
        - "Service de Calefones en {ubicacion}. ¡Lo reparamos Hoy Mismo!"
        - "Técnico de Calefones en {ubicacion}. Reparación en el Día"
        - "Reparación de Calefones en {ubicacion}. Solución Inmediata"
        - "Arreglo de Calefones en {ubicacion}. Servicio Urgente"
    2.  **H2 OPTIMIZADOS:** Los títulos de sección DEBEN incluir variaciones de las keywords con la ubicación.
    3.  **Ecosistema de Keywords:** Integra de forma natural las keywords "reparación de calefones", "service técnico", "arreglo de calefón" y "técnico de calefones" en los textos.
    4.  **Garantía:** Menciona que los trabajos tienen "garantía por escrito" o son "trabajos garantizados", pero NUNCA un período de tiempo.
    5.  **URGENCIA:** Crea sensación de urgencia e inmediatez en todo el contenido.
    6.  **Tono profesional:** Mantén un tono profesional, persuasivo y cercano, enfocado en generar confianza.

    Devuelve tu respuesta EXCLUSIVAMENTE en formato JSON con las siguientes claves:

    --- ESTRUCTURA JSON ---

    ### SEO & METADATOS ###
    - "meta_title": "Título SEO (50-60 chars). Ej: Service de Calefones en {ubicacion} | Reparación Urgente"
    - "meta_description": "Meta descripción SEO (140-155 chars) con keywords y CTA. Ej: Service técnico especializado en calefones en {ubicacion}. Reparación en el día. Presupuesto gratis por WhatsApp. ¡Llámenos al 096 758 200!"
    - "og_title": "Título para redes sociales. Ej: Service de Calefones a Domicilio en {ubicacion}"
    - "og_description": "Descripción para redes sociales. Ej: Reparación de calefones en {ubicacion}. Expertos en todas las marcas. Solución garantizada el mismo día."

    ### CONTENIDO PRINCIPAL ###
    - "titulo_h1": "Título H1 usando una de las 4 plantillas obligatorias."
    - "subtitulo_hero": "Subtítulo persuasivo debajo del H1 (2-3 oraciones). Ej: Atendemos todas las marcas en {ubicacion}. Pida su presupuesto GRATIS por WhatsApp y reciba un diagnóstico al instante."
    - "texto_hero_adicional": "Texto adicional en el hero (1-2 oraciones). Ej: Nuestro equipo de técnicos está en {ubicacion} para darle una solución rápida y garantizada en el día."

    ### SECCIONES ###
    - "titulo_seccion_servicios": "Título H2 para servicios (con ubicación). Ej: Servicio técnico de calefones en {ubicacion}"
    - "titulo_seccion_problemas": "Título H2 para problemas comunes (con ubicación). Ej: Arreglo de calefones en {ubicacion}"
    - "titulo_seccion_nosotros": "Título H2 para 'Sobre nosotros' (con ubicación). Ej: Expertos en reparación de calefones en {ubicacion}"
    
    ### TEXTOS DE PROBLEMAS (2-3 oraciones cada uno, persuasivas con CTA) ###
    - "texto_problema_no_calienta": "Descripción persuasiva del problema 'Luz prende, no calienta' enfocada en {ubicacion}. Debe mencionar que es una falla común con solución rápida y terminar con CTA para contactar."
    - "texto_problema_no_enciende": "Descripción persuasiva del problema 'No prende, ni calienta' enfocada en {ubicacion}. Debe mencionar que es un problema de seguridad y terminar con CTA para contactar."
    - "texto_problema_salta_llave": "Descripción persuasiva del problema 'Hace saltar la llave' enfocada en {ubicacion}. Debe mencionar que es una alerta de seguridad crítica y terminar con CTA urgente."
    - "texto_problema_pierde_agua": "Descripción persuasiva del problema 'El calefón pierde agua' enfocada en {ubicacion}. Debe aclarar que no siempre significa tanque roto y terminar con CTA para presupuesto."
    - "texto_problema_agua_tibia": "Descripción persuasiva del problema 'Agua siempre sale tibia' enfocada en {ubicacion}. Debe mencionar el desperdicio de energía y terminar con CTA para restaurar confort."
    - "texto_problema_no_corta": "Descripción persuasiva del problema 'Calienta continuamente' enfocada en {ubicacion}. Debe mencionar que es un problema de seguridad grave y terminar con CTA de urgencia."

    ### SECCIÓN NOSOTROS (4 párrafos de 3-4 oraciones cada uno) ###
    - "texto_nosotros_1": "Primer párrafo sobre la frustración del cliente y cómo la empresa nació para solucionar eso en {ubicacion}. Enfatizar misión clara: servicio rápido, profesional y que respeta el tiempo del cliente."
    - "texto_nosotros_2": "Segundo párrafo sobre la eficacia del servicio: reparación el mismo día en domicilio, respeto del tiempo con margen de 2 horas, y que son la única empresa 100% especializada en calefones eléctricos en Uruguay."
    - "texto_nosotros_3": "Tercer párrafo sobre transparencia y confianza: empresa registrada en BPS y DGI, uso de repuestos originales, y garantía real. Mencionar que la seguridad y satisfacción son prioridad máxima."
    - "texto_nosotros_4": "Cuarto párrafo con llamado a la acción: contactar al 096 758 200 por llamada o WhatsApp para presupuesto estimado al instante, sin compromiso de contratación."

    ### FAQS (Respuestas mejoradas de 2-3 oraciones, naturales y persuasivas) ###
    - "faq_respuesta_no_calienta": "Respuesta mejorada para '¿Porque mi calefón enciende pero no calienta?' Mencionar resistencia quemada o termostato defectuoso, y que los técnicos pueden diagnosticar y reparar rápidamente."
    - "faq_respuesta_salta_llave": "Respuesta mejorada para '¿Porque mi calefón hace saltar la llave?' Mencionar cortocircuito en resistencia eléctrica, que es falla de seguridad importante que debe ser atendida por profesional."
    - "faq_respuesta_no_enciende": "Respuesta mejorada para '¿Porque mi calefón no enciende y no calienta?' Mencionar que puede ser problema eléctrico, termostato o resistencia. Realizar chequeo completo para solucionar."
    - "faq_respuesta_gotea": "Respuesta mejorada para '¿Por qué mi calefón gotea desde abajo?' Mencionar que no siempre significa tanque roto, puede ser falla menor de menor costo, pero es señal de riesgo. Ofrecer presupuesto estimativo sin costo."
    - "faq_respuesta_poca_presion": "Respuesta para '¿Por qué sale poca agua o sin presión de mi calefón?' Mencionar acumulación de sarro en tuberías o calefón. Limpieza profesional puede restaurar presión y flujo de agua adecuados."
    - "faq_respuesta_agua_tibia": "Respuesta para '¿Por qué el agua de mi calefón siempre sale tibia?' Mencionar termostato mal calibrado o resistencia que no funciona a máxima capacidad. Ajustar o reemplazar piezas suele solucionar el problema."

    ### FAQS ADICIONALES (SECCIÓN 2) ###
    - "faq2_respuesta_instalacion": "Respuesta completa (4-5 oraciones) para '¿Hacen instalación de calefones?' Confirmar que sí realizan instalaciones de todas las marcas, mencionar que incluye instalación segura cumpliendo normas técnicas, conexiones profesionales, verificación completa y opción de llevarse calefón antiguo. Garantizar instalación prolija y segura. Terminar con CTA para agendar llamando al 096 758 200."
    - "faq2_respuesta_marcas": "Respuesta (3 oraciones) para '¿Trabajan con todas las marcas de calefones eléctricos?' Confirmar experiencia en todas las marcas comercializadas en Uruguay (James, Bronx, Sirium, Orion, Delne, Thermor, etc.). Mencionar conocimiento técnico y garantía de reparación de calidad. Terminar con CTA para contactar al 096 758 200."
    - "faq2_respuesta_garantia": "Respuesta completa (4-5 oraciones) para '¿Las reparaciones tienen garantía?' Explicar que cada reparación comienza con diagnóstico profesional y termina con trabajo garantizado. Mencionar que ofrecen garantía específica según tipo de reparación, que el técnico detalla período de cobertura antes de iniciar. Aclarar que la garantía cubre integralmente mano de obra y repuestos. Mencionar que son empresa registrada en BPS y DGI como respaldo."

    ### SERVICIOS (¿QUÉ HACEMOS?) - 2 oraciones cada uno ###
    - "texto_servicio_instalacion": "Texto para servicio de Instalación. Mencionar que instalan calefón nuevo o reemplazo con precisión y seguridad según normativa. Garantizar conexión perfecta para rendimiento óptimo desde primer día."
    - "texto_servicio_mantenimiento": "Texto para servicio de Mantenimientos. Mencionar que anticiparse a averías alarga vida útil del calefón. Mantenimiento anual previene problemas costosos, optimiza consumo energía y asegura funcionamiento eficiente."
    - "texto_servicio_reparacion": "Texto para servicio de Reparación. Mencionar que son especialistas dedicados exclusivamente a reparación de calefones. Diagnostican falla real y solucionan en el acto, devolviendo agua caliente sin demoras."
    - "texto_servicio_asesoramiento": "Texto para servicio de Asesoramiento. Mencionar que brindan asesoramiento experto y honesto para elegir calefón ideal según hogar y consumo. Buena elección ahorra problemas y dinero."

    ### TESTIMONIOS (Testimonios realistas de 3-4 oraciones, naturales, específicos) ###
    - "testimonio_1_texto": "Testimonio realista de un cliente en {ubicacion} que tuvo un problema con su calefón. Debe sonar natural, mencionar el problema específico, la experiencia con el servicio (rapidez, profesionalismo) y el resultado satisfactorio."
    - "testimonio_1_autor": "Nombre completo del primer cliente (nombre y apellido uruguayo realista)."
    - "testimonio_2_texto": "Testimonio realista de un cliente en {ubicacion} que destaca la especialización y profesionalismo. Debe sonar natural y mencionar un problema específico diferente al primero."
    - "testimonio_2_autor": "Nombre completo del segundo cliente (nombre y apellido uruguayo realista, diferente al primero)."
    - "testimonio_3_texto": "Testimonio realista de un cliente en {ubicacion} que menciona experiencia previa negativa con otro servicio y lo buena que fue la experiencia con Calefon.UY. Debe sonar natural."
    - "testimonio_3_autor": "Nombre completo del tercer cliente (nombre y apellido uruguayo realista, diferente a los anteriores)."

    ### FOOTER ###
    - "footer_descripcion": "Texto descriptivo de 2-3 oraciones para el footer enfocado en {ubicacion}. Debe mencionar que el calefón involucra riesgos eléctricos y de presión, que la reparación debe ser por personal especializado, y que Calefon.UY se dedica exclusivamente a reparación de calefones garantizando servicio profesional, seguro y confiable."
    """

    intentos = 0
    datos_generados = None
    while intentos < 3 and not datos_generados:
        try:
            print("   - Enviando solicitud a la IA (esto puede tardar hasta 90 segundos)...")
            response = model.generate_content(prompt, safety_settings=safety_settings)
            
            print("   - Respuesta recibida. Verificando integridad...")
            if response.parts:
                texto_limpio = response.text.strip().replace('```json', '').replace('```', '')
                temp_datos = json.loads(texto_limpio)
                
                campos_faltantes = [campo for campo in campos_criticos if campo not in temp_datos or not temp_datos[campo]]
                if campos_faltantes:
                    print(f"   - ❌ Verificación fallida. Faltan campos: {', '.join(campos_faltantes)}. Reintentando...")
                    raise ValueError("Respuesta incompleta de la IA")
                
                print("   - ✅ Verificación exitosa. Contenido completo.")
                datos_generados = temp_datos
            else:
                print("   - ⚠️ Advertencia: La respuesta fue bloqueada por el filtro de seguridad de la IA. Reintentando...")
                raise ValueError("Respuesta bloqueada")

        except Exception as e:
            intentos += 1
            print(f"   - ⚠️ Advertencia: Intento {intentos} fallido para {ubicacion}. Reintentando... ({e})")
            time.sleep(5)

    if datos_generados:
        try:
            # --- REFUERZO DE DATOS (FALLBACK) ---
            datos_generados.setdefault('og_title', datos_generados.get('meta_title', f"Service de Calefones en {ubicacion}"))
            datos_generados.setdefault('og_description', datos_generados.get('meta_description', ''))
            
            contenido_final = contenido_plantilla
            
            ubicacion_slug = crear_slug(ubicacion)
            
            # Primero reemplazar todos los datos generados por la IA
            for clave, valor in datos_generados.items():
                contenido_final = contenido_final.replace(f'{{{{{clave}}}}}', str(valor))
            
            # Después reemplazar los placeholders de ubicación
            contenido_final = contenido_final.replace('{{ubicacion_slug}}', ubicacion_slug)
            contenido_final = contenido_final.replace('{{ubicacion}}', ubicacion)
            
            nombre_archivo_salida = f"{ubicacion_slug}.html"
            
            with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
                f.write(contenido_final)
            
            print(f"✅ Landing Page creada: {nombre_archivo_salida}")
        except Exception as e:
            print(f"   - ❌ Error al procesar o guardar los datos para {ubicacion}: {e}")
    else:
        print(f"❌ Falló la generación de contenido para {ubicacion} después de 3 intentos.")

print("\n🎉 ¡Proceso completado! Todas las landing pages han sido generadas.")