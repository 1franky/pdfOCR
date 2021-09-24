# OCR 

### Script  para añadir capa de ***OCR*** a documentos ***PDF*** y compresión de los mismos.

--- 

## *Requisitos*:

* Python 3.x 
* Librerias de Python necesarias:
    * img2pdf
    * ocrmypdf
    * PyPDF2


## *INSTALACIÓN*

1. Instalar ***[python](https://www.python.org/downloads/ "Click para descargar python desde el sitio oficial")*** asegurate de añadir ***[python](https://www.python.org/downloads/ "Click para descargar python desde el sitio oficial")***  al ***path*** al momento de la instalación e instalar ***pip***.

2. Clonar el repositorio
```  
    git clone https://github.com/1franky/pdfOCR.git
```  
3. Instalar las siguientes librerias, copia y pega los siguientes comandos en una terminal ***CMD***:

```  
    pip install img2pdf 
```  
```  
    pip install ocrmypdf
```  
```  
    pip install PyPDF2
```

4. Cortar y pegar la carpeta ***ocrCompresor*** en  ***C:\\***

## *Uso*
### configuracion del *conf.ini* 
* Abrir con su editor de texto favorito :wink:

    ![paths!](imagesDocumentacion/paths.png)

    Sustituimos por la ruta a nuestros directorios sobre los que queremos trabajar.

    *urgentes* y *entrega* pueden apuntar hacia el mismo directorio, mientras proceso debe apuntar a otro directorio disntinto fuera de la raiz de los directorios de *urgentes* y *entrega* con el fin de evitar errores ya que el proceso es recursico. *root* debe apuntar a el directorio final donde se depositaran los archivos al final del proceso de ***OCR*** y ***compresión***.




