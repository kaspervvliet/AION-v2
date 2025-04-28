
"""
📄 Bestand: supabase_client.py
🔍 Doel: Connectie met Supabase + veilige insert functionaliteit
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 🌟 Forceer laden van .env bestand vanuit project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️  Waarschuwing: SUPABASE_URL of SUPABASE_KEY niet gevonden in .env bestand.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert(table: str, data: dict) -> dict:
    """
    Insert een record in de opgegeven Supabase-tabel.
    
    Args:
        table (str): Naam van de tabel
        data (dict): Data om in te voegen
        
    Returns:
        dict: Response van Supabase
    """
    try:
        response = supabase.table(table).insert(data).execute()
        if response.get("status_code", 200) >= 300:
            print(f"⚠️ Supabase insert fout ({table}): {response}")
        return response
    except Exception as e:
        print(f"❌ Fout bij insert in {table}: {e}")
        return {}
