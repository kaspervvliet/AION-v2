"""
📄 Bestand: analyse_bos_choc.py
🔍 Doel: Detecteert BOS of CHoCH structuurwijziging
🧩 Gebruikt door: strategiepool, reflectie of bias-modules
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: StrategyInterface, concepts
"""

from aion_core.abstract import StrategyInterface
from aion_core.knowledge.concepts import detect_choc, detect_bos
from aion_core.utils.logger import logger


class AnalyseBOSCHoCHStrategy(StrategyInterface):
    def generate_signal(self, context):
        structure = context.get("structure")
        if not structure:
            return self.log("⚠️ Geen structuurdata in context", context)

        if detect_choc(structure):
            return {
                "type": "structure",
                "detail": "CHoCH gedetecteerd",
                "strategy": self.__class__.__name__
            }

        if detect_bos(structure):
            return {
                "type": "structure",
                "detail": "BOS gedetecteerd",
                "strategy": self.__class__.__name__
            }

        return self.log("❌ Geen BOS of CHoCH in structuur", context)
