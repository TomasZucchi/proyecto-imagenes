from PIL import Image, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import cv2
from IPython.display import display

# Tamaños para redes sociales
TAMANIOS = {
    "Instagram": (1080, 1080),
    "Facebook": (1200, 630),
    "Twitter": (1600, 900),
    "Youtube": (1280, 720)
}

# Cargar imagen
def cargar_imagen(ruta):
    try:
        if ruta.startswith("http"):
            datos = requests.get(ruta).content
            return Image.open(BytesIO(datos)).convert("RGB")
        else:
            return Image.open(ruta).convert("RGB")
    except Exception as e:
        print("Error al cargar la imagen:", e)
        return None

# Mostrar imagen
def mostrar_imagen(ruta):
    try:
        img = Image.open(ruta)
        w, h = img.size
        plt.figure(figsize=(w/100, h/100))
        plt.imshow(img)
        plt.axis("off")
        display(plt.gcf())
        plt.close()
    except Exception as e:
        print("Error al mostrar la imagen:", e)

# Redimensionar según red social
def redimensionar_imagen(ruta, red_social):
    red_social = red_social.capitalize()
    if red_social not in TAMANIOS:
        print("Red social no válida.")
        return None
    img = cargar_imagen(ruta)
    if img is None:
        return None
    ancho_obj, alto_obj = TAMANIOS[red_social]
    img.thumbnail((ancho_obj, alto_obj))
    nombre_salida = f"imagen_{red_social}.jpg"
    img.save(nombre_salida)
    print(f"Imagen redimensionada guardada como {nombre_salida} ({img.size})")
    mostrar_imagen(nombre_salida)
    return nombre_salida

# Ecualizar contraste
def ecualizar_contraste(ruta, nombre_salida="ecualizada"):
    img = cargar_imagen(ruta)
    if img is None:
        return None
    img_gray = img.convert("L")
    img_array = np.array(img_gray)
    hist, bins = np.histogram(img_array.flatten(), 256, (0, 256))
    cdf = hist.cumsum()
    cdf_normalized = 255 * cdf / cdf[-1]
    img_eq = np.interp(img_array.flatten(), bins[:-1], cdf_normalized)
    img_eq = img_eq.reshape(img_array.shape).astype("uint8")
    img_ecualizada_pil = Image.fromarray(img_eq)
    # Mostrar
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.title("Ecualizada")
    plt.imshow(img_eq, cmap="gray")
    plt.axis("off")
    display(plt.gcf())
    plt.close()
    img_orig = f"{nombre_salida}_original.jpg"
    img_mod = f"{nombre_salida}_ecualizada.jpg"
    img.save(img_orig)
    img_ecualizada_pil.save(img_mod)
    print("Guardado:", img_orig)
    print("Guardado:", img_mod)
    return img_mod

# Filtros disponibles
FILTROS = {
    "BLUR": ImageFilter.BLUR,
    "CONTOUR": ImageFilter.CONTOUR,
    "DETAIL": ImageFilter.DETAIL,
    "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
    "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
    "EMBOSS": ImageFilter.EMBOSS,
    "FIND_EDGES": ImageFilter.FIND_EDGES,
    "SHARPEN": ImageFilter.SHARPEN,
    "SMOOTH": ImageFilter.SMOOTH
}

# Aplicar filtro
def aplicar_filtro(ruta, filtro):
    filtro = filtro.upper()
    if filtro not in FILTROS:
        print("Filtro no válido.")
        return None
    img = cargar_imagen(ruta)
    if img is None:
        return None
    img_filtrada = img.filter(FILTROS[filtro])
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.title(f"Filtro: {filtro}", color="red")
    plt.imshow(img_filtrada)
    plt.axis("off")
    display(plt.gcf())
    plt.close()
    nombre_salida = f"filtro_{filtro}.jpg"
    img_filtrada.save(nombre_salida)
    print("Guardado:", nombre_salida)
    return nombre_salida

# Mostrar todos los filtros
def mostrar_todos_los_filtros(ruta):
    img = cargar_imagen(ruta)
    if img is None:
        return None
    nombres = list(FILTROS.keys())
    plt.figure(figsize=(12, 12))
    plt.subplot(4, 3, 1)
    plt.title("ORIGINAL", color="blue")
    plt.imshow(img)
    plt.axis("off")
    for i, nombre in enumerate(nombres):
        img_f = img.filter(FILTROS[nombre])
        plt.subplot(4, 3, i + 2)
        plt.title(nombre)
        plt.imshow(img_f)
        plt.axis("off")
    plt.tight_layout()
    display(plt.gcf())
    plt.close()
    print("Guardado: todos_los_filtros.jpg")
    return "todos_los_filtros.jpg"

# Generar boceto
def generar_boceto(ruta, persona=True, invertir=True):
    if not persona:
        print("La IA detectó que no es una persona.")
        return None
    img = cargar_imagen(ruta)
    if img is None:
        return None
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gris = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    suave = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(suave, 50, 150)
    boceto = cv2.bitwise_not(bordes) if invertir else bordes
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1, 3, 2)
    plt.title("Grises")
    plt.imshow(gris, cmap="gray")
    plt.axis("off")
    plt.subplot(1, 3, 3)
    plt.title("Boceto")
    plt.imshow(boceto, cmap="gray")
    plt.axis("off")
    display(plt.gcf())
    plt.close()
    salida = "boceto_resultado.jpg"
    Image.fromarray(boceto).save(salida)
    print("Guardado:", salida)
    return salida

# Menú
def menu():
    ruta_actual = None
    while True:
        print("\n=== MENÚ ===")
        print("1. Cargar y redimensionar imagen")
        print("2. Ecualizar histograma")
        print("3. Aplicar filtro")
        print("4. Generar boceto")
        print("5. Mostrar todos los filtros")
        print("6. Salir")
        opcion = input("Elegí una opción: ")
        try:
            if opcion == "1":
                ruta = input("Ruta o URL de la imagen: ")
                red = input("Red social (Instagram, Facebook, Twitter, Youtube): ")
                ruta_actual = redimensionar_imagen(ruta, red)
            elif opcion == "2":
                if ruta_actual is None:
                    print("Primero cargá una imagen (opción 1)")
                    continue
                ecualizar_contraste(ruta_actual)
            elif opcion == "3":
                if ruta_actual is None:
                    print("Primero cargá una imagen (opción 1)")
                    continue
                filtro = input(f"Elegí filtro ({', '.join(FILTROS.keys())}): ")
                aplicar_filtro(ruta_actual, filtro)
            elif opcion == "4":
                if ruta_actual is None:
                    print("Primero cargá una imagen (opción 1)")
                    continue
                generar_boceto(ruta_actual)
            elif opcion == "5":
                if ruta_actual is None:
                    print("Primero cargá una imagen (opción 1)")
                    continue
                mostrar_todos_los_filtros(ruta_actual)
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error:", e)

# Ejecutar menú
if __name__ == "__main__":
    menu()