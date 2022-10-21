# sistema-conversion-cloud
## Sistema de conversión de archivos


Para iniciar:

1. Crear ambiente virtual usando:
```
python3 -m venv venv
```
2. Instalar dependencias
```
pip3 install -r requirements.txt
```
3. Copiar el ```env.template``` y renombar a ```.env```
4. Cambiar variables de entorno necesarias
5. Ejecutar base de datos usando: 
```
docker-compose up -d
```

6. Ejecutar en modo pruebas usando:
```
flask run
```



