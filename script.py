 
import psycopg2
from psycopg2.extras import RealDictCursor
 
#credenciales para la conneccion a la base de datos
DB_CONFIG = {
    'dbname': 'services-optimization',
    'user': 'postgres',
    'password': 'teamsalchipapa2025',
    'host': 'localhost',
    'port': 5432
}
 
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(" Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(" Error al conectar a la base de datos:", e)
        return None
 
def fetch_campaigns():
    conn = get_connection()
    if not conn:
        return []
   
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Campaigns;")
            campaigns = cursor.fetchall()
            return campaigns
    except Exception as e:
        print(" Error al obtener campañas:", e)
        return []
    finally:
        conn.close()
 
def insert_domain(name):
    conn = get_connection()
    if not conn:
        return
   
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Domains (name) VALUES (%s) RETURNING id;", (name,))
            domain_id = cursor.fetchone()[0]
            conn.commit()
            print(f" Dominio insertado con ID: {domain_id}")
            return domain_id
    except Exception as e:
        print(" Error al insertar dominio:", e)
    finally:
        conn.close()
 
# Ejemplo de uso
if __name__ == "__main__":
    # Insertar un dominio
    insert_domain("")
   
    # Obtener campañas
    campaigns = fetch_campaigns()
    for campaign in campaigns:
        print(campaign)