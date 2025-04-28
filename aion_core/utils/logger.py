
# 📄 Bestand: aion_core/utils/logger.py
# 🔍 Doel: Basislogger configureren voor AION project

import logging

# Maak een basis logger aan
logger = logging.getLogger("AION")
logger.setLevel(logging.INFO)

# Zorg dat we geen dubbele handlers toevoegen
if not logger.handlers:
    # Console handler toevoegen
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter instellen
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    # Handler toevoegen aan logger
    logger.addHandler(ch)
