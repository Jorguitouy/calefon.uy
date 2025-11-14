"""
Generador de Favicons PNG desde SVG
Convierte el favicon.svg en múltiples tamaños PNG
"""

from PIL import Image, ImageDraw
import os

def create_favicon_png(size, output_path):
    """Crea un favicon PNG del tamaño especificado con diseño de llama blanca sobre fondo rojo"""
    
    # Crear imagen con fondo rojo intenso
    img = Image.new('RGBA', (size, size), (227, 24, 55, 255))  # #E31837
    draw = ImageDraw.Draw(img)
    
    # Colores
    white = (255, 255, 255, 255)
    white_semi = (255, 255, 255, 230)  # Blanco semi-transparente
    red_dark = (227, 24, 55)  # Para detalles de ventilación
    
    # Escalar coordenadas según el tamaño
    scale = size / 32
    center_x = size // 2
    center_y = size // 2
    
    # Dibujar base del calefón (rectángulo blanco)
    base_y = center_y + int(5 * scale)
    base_height = int(5 * scale)
    base_width = int(10 * scale)
    base_x1 = center_x - base_width // 2
    base_x2 = center_x + base_width // 2
    
    draw.rounded_rectangle(
        [(base_x1, base_y), (base_x2, base_y + base_height)],
        radius=int(1 * scale),
        fill=white,
        outline=white,
        width=max(1, int(0.3 * scale))
    )
    
    # Líneas de ventilación en la base (rojo sobre blanco)
    line_y1 = base_y + int(2 * scale)
    line_y2 = base_y + int(3.5 * scale)
    line_x1 = base_x1 + int(2 * scale)
    line_x2 = base_x2 - int(2 * scale)
    
    draw.line([(line_x1, line_y1), (line_x2, line_y1)], fill=red_dark, width=max(1, int(0.6 * scale)))
    draw.line([(line_x1, line_y2), (line_x2, line_y2)], fill=red_dark, width=max(1, int(0.6 * scale)))
    
    # Dibujar llama principal (forma aproximada con polígono) - BLANCO
    flame_points = [
        (center_x, center_y - int(10 * scale)),  # Punta superior
        (center_x - int(4 * scale), center_y - int(4 * scale)),  # Izquierda superior
        (center_x - int(4 * scale), center_y),  # Izquierda centro
        (center_x, center_y + int(3 * scale)),  # Base centro
        (center_x + int(4 * scale), center_y),  # Derecha centro
        (center_x + int(4 * scale), center_y - int(4 * scale)),  # Derecha superior
    ]
    
    draw.polygon(flame_points, fill=white, outline=white_semi)
    
    # Llama interna (más pequeña, blanco semi-transparente)
    inner_flame_points = [
        (center_x, center_y - int(7 * scale)),  # Punta superior
        (center_x - int(2.5 * scale), center_y - int(3 * scale)),  # Izquierda superior
        (center_x - int(2.5 * scale), center_y),  # Izquierda centro
        (center_x, center_y + int(2 * scale)),  # Base centro
        (center_x + int(2.5 * scale), center_y),  # Derecha centro
        (center_x + int(2.5 * scale), center_y - int(3 * scale)),  # Derecha superior
    ]
    
    draw.polygon(inner_flame_points, fill=white_semi)
    
    # Punto brillante blanco (elipse) - más sutil
    highlight_y = center_y - int(2 * scale)
    highlight_rx = int(1.2 * scale)
    highlight_ry = int(1.8 * scale)
    
    draw.ellipse(
        [(center_x - highlight_rx, highlight_y - highlight_ry),
         (center_x + highlight_rx, highlight_y + highlight_ry)],
        fill=(255, 255, 255, 180)
    )
    
    # Guardar imagen
    img.save(output_path, 'PNG')
    print(f"✓ Creado: {output_path} ({size}x{size})")

def main():
    """Genera todos los tamaños de favicon necesarios"""
    
    # Crear directorio v2/assets/favicons si no existe
    os.makedirs('v2/assets/favicons', exist_ok=True)
    
    # Tamaños estándar de favicon
    sizes = [
        (16, 'v2/assets/favicons/favicon-16x16.png'),
        (32, 'v2/assets/favicons/favicon-32x32.png'),
        (48, 'v2/assets/favicons/favicon-48x48.png'),
        (180, 'v2/assets/favicons/apple-touch-icon.png'),
        (192, 'v2/assets/favicons/icon-192.png'),
        (512, 'v2/assets/favicons/icon-512.png'),
    ]
    
    print("Generando favicons PNG con fondo rojo intenso e ícono blanco...")
    print("-" * 50)
    
    for size, path in sizes:
        try:
            create_favicon_png(size, path)
        except Exception as e:
            print(f"✗ Error creando {path}: {e}")
    
    print("-" * 50)
    print("¡Favicons generados exitosamente!")
    print("\nPara crear favicon.ico, puedes usar:")
    print("https://www.icoconverter.com/")
    print("O convertir favicon-32x32.png a .ico")

if __name__ == '__main__':
    main()
