import os 
from utils import load_user_history, load_evidence_requirements, parse_image_paths

class ClaimProcessor:
    def __init__(self, dataset_dir: str = "../dataset"):
        self.dataset_dir = dataset_dir

        # Load background lookup tables once at startup 
        user_history_path = os.path.join(dataset_dir, "user_history.csv")
        evidence_path = os.path.join(dataset_dir, "evidence_requirements.csv")

        self.user_history = load_user_history(user_history_path)
        self.evidence_requirements = load_evidence_requirements(evidence_path)

    def aggregate_claim_context(self, row:dict) -> dict:
        """
        Gathers raw claim row information, links it to user history 
        and evidence requirements, and parses image IDs. 
        """
        user_id = row['user_id']
        claim_object = row['claim_object']
        image_paths_str = row['image_paths']
        user_claim =  row['user_claim']

        # Look up user history (fallback to empty default if user is new)
        user_profile = self.user_history.get(user_id, {
            'past_claim_count': 0, 'accept_claim': 0, 'manual_review_claim': 0,
            'rejected_claim': 0, 'last_90_days_claim_count': 0,
            'history_flags': 'none', 'history_summary': 'New user with no history.'
        })
        
        # Look up relevant requirements rules
        specific_reqs = self.evidence_requirements.get(claim_object, [])
        global_reqs = self.evidence_requirements.get('all', [])
        relevant_rules = specific_reqs + global_reqs
        
        # Parse out target image paths and matching structural IDs
        images = parse_image_paths(image_paths_str)
        
        # Combine everything into a unified execution payload
        return {
            'user_id': user_id,
            'claim_object': claim_object,
            'user_claim': user_claim,
            'images': images,  # List of maps containing {'path', 'id'}
            'user_profile': user_profile,
            'rules': relevant_rules
        }

