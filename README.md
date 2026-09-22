# Valida si la DB tiene habilitada encripción

## Preperar instalación

- Crear directorio de trabajo

````bash
mkdir empresa
cd empresa
````
- clonar repositorio

git clone 
- auditar_empresa.py
- motores_bd.json
- requeriments.txt

#################################
Levantar ambiente virtual
#################################
python -m venv .empresa
.\.empresa\Scripts\Activate.ps1

#################################
Instalar librerias necesarias
#################################
pip install -r requeriments.txt

#################################
Configurar conexión DBS
#################################

vi motores_bd.json    #archivo de configuraciones


#################################
ejecutar auditor DBs
#################################

auditar_empresa.py

SALIDA#

PS C:\Temp\python\empresa> python .\auditar_empresa.py
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
PS C:\Temp\python\empresa>
