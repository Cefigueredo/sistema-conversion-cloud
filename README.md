# sistema-conversion-cloud
## Sistema de conversión de archivos


Para iniciar:

1. Crear ambiente virtual usando:
```
python3 -m venv venv
```
2. Activar ambiente virtual con:
- Si está en windows ejecutar:
```
venv\Scripts\activate
```
- Si está en Unix ejecutar:
```
source venv/Scripts/activate
```
3. Instalar dependencias
```
pip3 install -r requirements.txt
```
4. Copiar el ```env.template``` y renombar a ```.env```
5. Cambiar variables de entorno necesarias
6. Ejecutar base de datos usando: 
```
docker-compose up -d
```
7. Añadir variable de entorno ``FLASK_APP``:
- Si está en windows ejecutar:
```
set "FLASK_APP=entrypoint"
```
- Si está en Unix:
```
export FLASK_APP="entrypoint"
```
8. Ejecutar en modo pruebas usando:
```
flask run
```



