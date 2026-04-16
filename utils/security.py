import re
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityScanner:
    """
    Utility for scanning and masking PII (Personally Identifiable Information).
    Uses a combination of Regex and Transformers for NER.
    """
    def __init__(self):
        try:
            # Using a lightweight NER model for PII detection
            self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")
            logger.info("SecurityScanner: NER pipeline initialized.")
        except Exception as e:
            logger.warning(f"SecurityScanner: Failed to load Transformers pipeline ({e}). Falling back to Regex only.")
            self.ner_pipeline = None

    def mask_pii(self, text: str) -> str:
        """
        Masks common PII patterns like account numbers and entities found by NER.
        """
        # 1. Mask Fake Account Numbers (e.g., 10-12 digit sequences)
        # Pattern: matches 10 to 12 digits, potentially separated by dashes or spaces
        account_pattern = r'\b(?:\d[ -]?){10,12}\b'
        masked_text = re.sub(account_pattern, "[MASKED_ACCOUNT]", text)

        # 2. Mask Entities (Names, Locations, Orgs) using NER if available
        if self.ner_pipeline:
            try:
                entities = self.ner_pipeline(masked_text)
                # Sort entities in reverse order of start position to avoid indexing issues while replacing
                for entity in sorted(entities, key=lambda x: x['start'], reverse=True):
                    start = entity['start']
                    end = entity['end']
                    label = entity['entity_group']
                    masked_text = masked_text[:start] + f"[MASKED_{label}]" + masked_text[end:]
            except Exception as e:
                logger.error(f"SecurityScanner NER Error: {e}")

        return masked_text

def audit_data(content: str) -> str:
    """
    Standalone function to audit content for PII.
    """
    scanner = SecurityScanner()
    return scanner.mask_pii(content)
