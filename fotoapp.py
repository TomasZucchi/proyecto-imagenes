from PIL import Image, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import cv2
import os


TAMANIOS = {
          "Instagram": (1080, 1080),
          "Facebook": (1200, 630),
          "Twitter": (1600, 900),          
          "Youtube": (1280, 720)
          }


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


def redimensionar_imagen(ruta, red_social):
    red_social = red_social.capitalize()


    if red_social not in TAMANIOS:
      print("Red social no válida.")
      return None


    img = cargar_imagen(ruta)
    if img is None:
      return None


    ancho_obj, alto_obj = TAMANIOS[red_social]


    # Mantener proporciones
    img.thumbnail((ancho_obj, alto_obj))


    # Guardar con nombre nuevo
    nombre_salida = f"imagen_{red_social}.jpg"
    img.save(nombre_salida)


    print(f"Imagen redimensionada guardada como {nombre_salida} ({img.size})")
    return nombre_salida


def ecualizar_contraste(ruta, nombre_salida="ecualizada"):
    img = cargar_imagen(ruta)
    if img is None:
      return None


    # Convertir a grises
    img_gray = img.convert("L")
    img_array = np.array(img_gray)


    # Histograma y CDF
    hist, bins = np.histogram(img_array.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = 255 * cdf / cdf[-1]


    # Aplicar ecualización
    img_eq = np.interp(img_array.flatten(), bins[:-1], cdf_normalized)
    img_eq = img_eq.reshape(img_array.shape).astype('uint8')


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


    plt.show()


    # Guardar
    orig_path = f"{nombre_salida}_original.jpg"
    eq_path = f"{nombre_salida}_ecualizada.jpg"


    img.save(orig_path)
    img_ecualizada_pil.save(eq_path)


    print("Guardado:", orig_path)
    print("Guardado:", eq_path)


    return eq_path


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


def aplicar_filtro(ruta, filtro):

    filtro = filtro.upper()

    if filtro not in FILTROS:
      print("Filtro no válido.")
      return None


    img = cargar_imagen(ruta)
    if img is None:
        return None


    img_filtrada = img.filter(FILTROS[filtro])


    # Mostrar
    plt.figure(figsize=(8, 4))


    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")


    plt.subplot(1, 2, 2)
    plt.title(f"Filtro: {filtro}", color="red")
    plt.imshow(img_filtrada)
    plt.axis("off")


    plt.show()


    nombre_salida = f"filtro_{filtro}.jpg"
    img_filtrada.save(nombre_salida)
    print("Guardado:", nombre_salida)


    return nombre_salida


def mostrar_todos_los_filtros(ruta):

    img = cargar_imagen(ruta)
    if img is None:
        return None


    nombres = list(FILTROS.keys())


    plt.figure(figsize=(12, 12))


    # Original
    plt.subplot(4, 3, 1)
    plt.title("ORIGINAL", color="blue")
    plt.imshow(img)
    plt.axis("off")


    # Aplicar filtros
    for i, nombre in enumerate(nombres):
        img_f = img.filter(FILTROS[nombre])
        plt.subplot(4, 3, i + 2)
        plt.title(nombre)
        plt.imshow(img_f)
        plt.axis("off")


    plt.tight_layout()
    plt.savefig("todos_los_filtros.jpg")
    plt.show()


    print("Guardado: todos_los_filtros.jpg")


    return "todos_los_filtros.jpg"


def generar_boceto(ruta, persona=True, invertir=True):

    if not persona:
        print("La IA detectó que no es una persona.")
        return None


    img = cargar_imagen(ruta)
    if img is None:
        return None


    # Convertir a OpenCV
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


    gris = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    suave = cv2.GaussianBlur(gris, (5, 5), 0)


    bordes = cv2.Canny(suave, 50, 150)


    if invertir:
        boceto = cv2.bitwise_not(bordes)
    else:
        boceto = bordes


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


    plt.show()


    salida = "boceto_resultado.jpg"
    Image.fromarray(boceto).save(salida)
    print("Guardado:", salida)


    return salida

def menu():
    ruta_actual = None


    while True:
        print("\n=== MENÚ ===")
        print("1. Cargar y redimensionar imagen")
        print("2. Ecualizar histograma")
        print("3. Aplicar filtro")
        print("4. Generar boceto para pintores")
        print("5. Salir")

        opcion = input("Elegí una opción: ")

        try:
            if opcion == "1":
              ruta = input("Ruta o URL de la imagen: ")
              red = input("Red social (Instagram, Facebook, Twitter, Youtube): ")
              ruta_actual = redimensionar_imagen(ruta, red)

            elif opcion == "2":
              if ruta_actual is None:
                raise Exception("Primero cargá una imagen (opción 1)")
              ecualizar_contraste(ruta_actual)

            elif opcion == "3":
              if ruta_actual is None:
                raise Exception("Primero cargá una imagen (opción 1)")
              filtro = input("Elegí filtro: ")
              aplicar_filtro(ruta_actual, filtro)


            elif opcion == "4":
              if ruta_actual is None:
                raise Exception("Primero cargá una imagen (opción 1)")
              generar_boceto(ruta_actual)


            elif opcion == "5":
              print("Saliendo...")
              break


            else:
              print("Opción inválida.")


        except Exception as e:
          print("Error:", e)


    # FIN DEL MÓDULO

if __name__ == "__main__":
    menu()