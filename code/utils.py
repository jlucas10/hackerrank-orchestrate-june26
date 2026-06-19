# file to read CSV datasets and convert them into dicts

import csv 
import os


def load_user_history(csv_path: str) -> dict:
    """
    Load user histroy into a dictionary keyed by user_id
    """

    userHistoryMap = {}
    if not os.path.exists(csv_path):
        return userHistoryMap
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row['user_id']
            userHistoryMap[user_id] = {
                'past_claim_count': int(row['past_claim_count']),
                'accept_claim': int(row['accept_claim']),
                'manual_review_claim': int(row['manual_review_claim']),
                'rejected_claim': int(row['rejected_claim']),
                'last_90_days_claim_count': int(row['last_90_days_claim_count']),
                'history_flags': row['history_flags'],
                'history_summary': row['history_summary']
            }
        return userHistoryMap
    
def load_evidence_requirements(csv_path: str) -> dict:
    """
    Group evidence requirmeents by three types (car, laptop, package, all)
    """

    requirementsMap = {'car': [], 'laptop': [], 'package': [], 'all': []}
    if not os.path.exists(csv_path):
        return requirementsMap
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            obj_type = row['claim_object']
            req_data = {
                'requirement_id': row['requirement_id'],
                'applies_to': row['applies_to'],
                'minimum_image_evidence': row['minimum_image_evidence']
            }
            if obj_type in requirementsMap:
                requirementsMap[obj_type].append(req_data)
            else:
                requirementsMap[obj_type] = [req_data]
    return requirementsMap

def parse_image_paths(image_paths_str: str) -> list:
    """
    Splits semicolon-delimited paths and extracts basic details.
    Example input: "images/test/case_001/img_1.jpg;images/test/case_001/img_2.jpg"
    Returns a list of dicts: [{'path': ..., 'id': 'img_1'}, ...]
    """
    if not image_paths_str or image_paths_str.lower() == 'none':
        return []
        
    parsed_images = []
    paths = image_paths_str.split(';')
    for p in paths:
        p = p.strip()
        if p:
            # Extract filename without extension for the image ID (ex. 'img_1')
            filename = os.path.basename(p)
            img_id, _ = os.path.splitext(filename)
            parsed_images.append({
                'path': p,
                'id': img_id
            })
    return parsed_images