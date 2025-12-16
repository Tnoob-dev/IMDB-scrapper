# IMDB-Scraper
[Go to English version](./README.md)

### Descripción del proyecto

Este proyecto es un scraper en Python que consulta IMDb, obtiene información detallada sobre títulos (películas, series, episodios) y opcionalmente descarga la imagen del póster asociada a una ruta local.
​​Utiliza la librería Requests con una Session persistente y BeautifulSoup para analizar el HTML de la interfaz en español de IMDb (https://www.imdb.com/es-es).​

### Funcionamiento

    * La clase IMDB expone un método search(query: str) que envía una petición GET al endpoint de búsqueda de IMDb y analiza la lista de resultados.

    * El método get_info(url: URL) recibe la URL de un título concreto y extrae campos como título, título original, duración, sinopsis, géneros, puntuación y ruta de la imagen del póster, devolviendo un objeto FinalResult.

Internamente, métodos auxiliares analizan secciones y etiquetas específicas mediante atributos tipo CSS, y funciones de utilidad se encargan de normalizar URLs y descargar imágenes.

### Características principales

    * Buscar títulos en IMDb mediante una cadena de texto libre y obtener una lista estructurada de candidatos (ResultReturned).

    * Extraer información detallada de un título seleccionado, incluyendo puntuación, géneros y sinopsis desde la sección principal del contenido.

​    * Descargar y guardar el póster en disco usando funciones auxiliares que encapsulan la búsqueda de la imagen y la descarga binaria.

### Tecnologías utilizadas

    * Python 3

    * requests Session para la comunicación HTTP

    * BeautifulSoup (bs4) para el análisis de HTML

    * yarl URL para gestionar URLs

    * Tipos personalizados de excepción (TagNotFound) y estructuras de datos (ResultReturned, FinalResult) para señalar claramente errores de parseo y encapsular resultados.
    ​
### Uso

    * Instanciar el cliente: crear un objeto IMDB() para inicializar la URL base, la sesión y las cabeceras (User-Agent).

    * Llamar a search("tu consulta") y seleccionar una de las URLs devueltas en la lista de ResultReturned.

    * Pasar la URL seleccionada a get_info() para obtener un FinalResult con todos los atributos parseados y la ruta local del póster si la descarga tiene éxito.

### Ejemplo de uso:
```python3
im_db = IMDB()

# esto va a retornar una lista de objetos ResultReturned, el cual contiene nombre y url
result = imdb.search("Avatar La leyenda de Aang")

# ahora iteramos sobre todos los resultados y lo pasamos al .get_info de la clase, el cual va a devolvernos para cada uno un objeto FinalResult con toda la informacion
for res in result:
    tv = im_db.get_info(res.url)
    print(tv)
```

El código está diseñado para lanzar RuntimeError en caso de problemas de conexión y TagNotFound cuando la estructura HTML de IMDb cambia y no se pueden localizar las etiquetas necesarias.

### Preguntas frecuentes

    * ¿Este proyecto está afiliado a IMDb?
        - No. Es un scraper independiente con fines educativos/útiles y no está afiliado ni respaldado por IMDb. Revisa siempre los Términos de Uso de IMDb antes de hacer scraping.

    * ¿El scraper puede dejar de funcionar en el futuro?
        - Sí. Si IMDb cambia su estructura HTML o los nombres de las clases CSS, los métodos que dependen de esos selectores pueden lanzar TagNotFound y será necesario actualizarlos.

    * ¿Qué datos devuelve para un título?
        - Devuelve el título principal, el título original (cuando está disponible), la duración, la sinopsis, los géneros, la puntuación media y la ruta local del póster descargado, todo dentro de un objeto FinalResult.

    * ¿Puedo cambiar el idioma o la URL base?
        - La implementación actual apunta a https://www.imdb.com/es-es. Puedes modificar self.url o extender la clase para soportar otros idiomas o endpoints según tus necesidades. Pero no puedo asegurar de que funcione

    * ¿Es apto para scraping a gran escala?
        - Está pensado principalmente para uso personal o a pequeña escala. Para scraping masivo, conviene añadir mecanismos de cortesía (esperas, rotación, control de errores) y posiblemente infraestructura especializada.
​