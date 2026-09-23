import json
import socket
import psycopg2
import mysql.connector
import pymssql
import os

# ==============================================================================
# ENRUTADOR DINÁMICO DE AUDITORÍA
# ==============================================================================

def verificar_puerto_abierto(ip, puerto, timeout=2):
    """Valida la conectividad a nivel de red antes de disparar el conector."""
    try:
        with socket.create_connection((ip, puerto), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def ejecutar_auditoria_motor(srv):
    motor = srv['motor'].lower()
    ip = srv['ip']
    puerto = srv['puerto']
    user = srv['usuario']
    password = srv['contrasena']
    db = srv['base_datos']
    
    print(f"\n🔍 [{srv['id']}] Evaluando {motor.upper()} en {ip}:{puerto}...")
    
    # 1. Validación de Infraestructura / Red
    if not verificar_puerto_abierto(ip, puerto):
        print(f"  -> ❌ ERROR DE RED: El puerto {puerto} está cerrado o inaccesible.")
        return False

    # 2. Enrutamiento Dinámico según el motor listado
    try:
        if motor == 'sql_server':
            conn = pymssql.connect(server=ip, port=puerto, user=user, password=password, database=db, timeout=5)
            cursor = conn.cursor(as_dict=True)
            cursor.execute("""
                SELECT db.name, COALESCE(dm.encryption_state, 0) as estado
                FROM sys.databases db 
                LEFT JOIN sys.dm_database_encryption_keys dm ON db.database_id = dm.database_id;
            """)
            for row in cursor.fetchall():
                status = "🟢 CIFRADO (TDE)" if row['estado'] == 3 else "🚨 NO CIFRADO"
                print(f"     Database: {row['name']} -> {status}")
            
        elif motor == 'mysql':
            conn = mysql.connector.connect(host=ip, port=puerto, user=user, password=password, database=db, connection_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';")
            rows = cursor.fetchall()
            if not rows:
                print("     🚨 Alerta: No se encontraron tablas cifradas de forma explícita en InnoDB.")
            for row in rows:
                print(f"     🟢 Tabla Cifrada Detectada: {row[0]}.{row[1]}")
                
        elif motor == 'mariadb':
            conn = mysql.connector.connect(host=ip, port=puerto, user=user, password=password, database=db, connection_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SHOW GLOBAL VARIABLES LIKE 'innodb_encrypt_tables';")
            res = cursor.fetchone()
            estado = res[1] if res else "OFF"
            if estado.upper() in ['ON', 'FORCE']:
                print(f"     🟢 Variable 'innodb_encrypt_tables': {estado} (CIFRADO EN REPOSO ACTIVO)")
            else:
                print(f"     🚨 Variable 'innodb_encrypt_tables': {estado} (Cifrado global Desactivado)")
                
        elif motor == 'postgresql':
            conn = psycopg2.connect(host=ip, port=puerto, user=user, password=password, database=db, connect_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM pg_stat_ssl WHERE ssl = true;")
            ssl_conns = cursor.fetchone()[0]
            print(f"     🔒 Conexiones TLS/SSL activas: {ssl_conns}")
            print("     💡 Nota: Validar pgcrypto o cifrado de almacenamiento local en el sistema operativo.")
            
        else:
            print(f"  -> ⚠️ Motor '{motor}' no soportado por este script.")
            return False
            
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"  -> ❌ ERROR DE AUTENTICACIÓN / ACCESO: {e}")
        return False

# ==============================================================================
# FLUJO PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    archivo_inventario = 'motores_bd.json'
    
    if not os.path.exists(archivo_inventario):
        print(f"❌ Error: No se encuentra el archivo de inventario '{archivo_inventario}'")
        exit(1)
        
    with open(archivo_inventario, 'r') as f:
        lista_servidores = json.load(f)
        
    print("======================================================================")
    print(f" INICIANDO AUDITORÍA CORPORATIVA DE CIFRADO")
    print(f" Total de objetivos cargados desde el inventario: {len(lista_servidores)}")
    print("======================================================================")
    
    exitos = 0
    fallas = 0
    
    for servidor in lista_servidores:
        resultado = ejecutar_auditoria_motor(servidor)
        if resultado:
            exitos += 1
        else:
            fallas += 1
            
    print("\n======================================================================")
    print(" RESUMEN DE LA AUDITORÍA")
    print(f" ✅ Conexiones/Auditorías Exitosas: {exitos}")
    print(f" ❌ Fallas (Red/Credenciales/No Soportados): {fallas}")
    print("======================================================================")
