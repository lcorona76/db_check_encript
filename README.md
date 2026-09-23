# Script para valiar si la DB tiene habilitada encripción

## Requerimientos
#### El script se valido con las siguientes versiones
- Python 3.13.2
- pip 26.1.2
#### Librerías necesarias
- cffi==2.1.1
- cryptography==50.0.1
- mysql-connector==2.2.9
- mysql-connector-python==26.7.0
- oracledb==4.0.2
- psycopg2==2.9.12
- psycopg2-binary==2.9.12
- pycparser==3.0
- pymssql==2.3.13
- typing_extensions==4.16.0

## Preperar instalación

- Crear directorio de trabajo
- Clonar repositorio
- Cambiar a directorio de trabajo

````bash
mkdir folder_trabajo
cd folder_trabajo
git clone https://github.com/lcorona76/db_check_encript.git
cd db_check_encript
````
- Crear entorno virtual de trabajo
- Activar entorno virtual
- Instalar dependencias

````bash
python -m venv .venv
````
- En Windows
````bash
.\.venv\Scripts\Activate.ps1
````
- En Linux
````bash
./.venv/Scripts/Activate
````
````bash
pip install -r requeriments.txt
````

# Configurar conexión DBS
- Editar Archivo y configurar datos de acceso de cada base de datos

````bash
vim motores_bd.json    #archivo de configuraciones
````
- Por ejemplo:
<img width="477" height="862" alt="image" src="https://github.com/user-attachments/assets/ca84d827-2712-4584-bd81-bed4a079054e" />

# Ejecutar auditor_dbs.py

# Salida
````bash
PS C:\Temp> python .\auditar_dbs.py
======================================================================
 INICIANDO AUDITORÍA CORPORATIVA DE CIFRADO
 Total de objetivos cargados desde el inventario: 4
======================================================================

🔍 [SRV-NUCLEO-MS01] Evaluando SQL_SERVER en 192.168.75.132:1433...
     Database: master -> 🚨 NO CIFRADO
     Database: tempdb -> 🚨 NO CIFRADO
     Database: model -> 🚨 NO CIFRADO
     Database: msdb -> 🚨 NO CIFRADO

🔍 [SRV-VENTAS-MY02] Evaluando MYSQL en 192.168.75.132:3308...
     🟢 Tabla Cifrada Detectada: bd_segura.usuarios

🔍 [SRV-PROD-MA01] Evaluando MARIADB en 192.168.75.132:3307...
     🟢 Variable 'innodb_encrypt_tables': ON (CIFRADO EN REPOSO ACTIVO)

🔍 [SRV-APP-PG01] Evaluando POSTGRESQL en 192.168.75.132:5432...
     🔒 Conexiones TLS/SSL activas: 0
     💡 Nota: Validar pgcrypto o cifrado de almacenamiento local en el sistema operativo.

======================================================================
 RESUMEN DE LA AUDITORÍA
 ✅ Conexiones/Auditorías Exitosas: 4
 ❌ Fallas (Red/Credenciales/No Soportados): 0
======================================================================
PS C:\Temp>
````
