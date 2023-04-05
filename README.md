# django-prueba-rest-api
Este es el repositorio en donde esta el desarrollo de lo pedido en la prueba backend.

* Para poder ejecutar el proyecto, se tiene que clonar el codigo del repositorio en el link
proporcionado: https://github.com/Kotoamatsukam/django-prueba-rest-api

* Una vez realizado esto, se tiene que tener instalado el mysql workbench para administrar
la base de datos MySql. Se puede realizar la instalacion descargando tal instalador de la pagina web:
https://dev.mysql.com/downloads/workbench/

* Una vez realizado tal descarga, se tiene que crear una conexion a base de datos. En mi caso,
realize una conexion en localhost con el punto de enlace 127.0.0.1 y puero 3306. Se tiene que anotar
la contraseña y el usuario root para luego acceder a la base de datos desde el conector de Django.

* Se tiene que tener la version de python instalada y configurada en las variables de entorno.
Se aconseja Python 3.10.8.

Tambien, se tienen que instalar los siguientes comandos para correr la aplicacion:
- pip install django
- pip install mysqlclient

* En el codigo, se tiene que entrar en la carpeta DjangoApiTest, luego en la carpeta de adentro llamada
DjangoApiTest, y en el archivo settings configurar los parametros de la base de datos para realizar
la conexion, segun el usuario y contrasenhia que haya definido. Y guardarlo.

Lo que tiene que cambiar es esto:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apitestdb',
        'USER': <nombre_de_usuario_root_que_usted_creo>,
        'PASSWORD': <contrasenia_de_usuario_root_que_usted_creo>,
        'HOST': <puerto de enlace, aqui ponde localhost si lo desplegara localmente>,
        'PORT': '3306'
    }
}
,
cambie todo lo que esta entre <> por los datos de su conexion a Mysql. No se olvide de guardar el archivo.

* Finalmente para correr la aplicacion, volvemos adentro de la carpeta principal y ejecutamos los siguientes comandos:
-python manage.py makemigrations ApiTestApp
-python manage.py migrate
-python manage.py runserver

Y ya estaria el servidor desplegado, y podrian probar las apis mediante la coleccion de postman.

Para las pruebas unitarias correr el comando:
-python manage.py test ApiTestApp.test


