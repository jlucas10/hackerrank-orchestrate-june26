import os
from core.processor import ClaimProcessor

def test_pipeline():
    print("=== Testing Step 2: Data Aggregation Pipeline ===\n")
    
    # Initialize our processor pointing to the dataset directory
    # Adjust path if your folder structure differs slightly
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset"))
    print(f"Using dataset directory: {dataset_dir}")
    
    try:
        processor = ClaimProcessor(dataset_dir=dataset_dir)
        print("Successfully initialized ClaimProcessor and loaded lookup tables.\n")
    except Exception as e:
        print(f"Error during initialization: {e}")
        return

    # Mock a realistic input row from claims.csv
    mock_row = {
        "user_id": "user_001",
        "image_paths": "images/sample/case_001/img_1.jpg;images/sample/case_001/img_2.jpg",
        "user_claim": "Customer: Hi, I found new damage on my car. The back bumper has a dent.",
        "claim_object": "car"
    }
    
    print("Processing mock claim row for user_001...")
    payload = processor.aggregate_claim_context(mock_row)
    
    # Print out the aggregated payload to inspect correctness
    print("\n--- Aggregated Payload Result ---")
    print(f"User ID: {payload['user_id']}")
    print(f"Claim Object: {payload['claim_object']}")
    
    print("\nParsed Images JSON-style schema:")
    for img in payload['images']:
        print(f"  - Image ID: {img['id']} | Path: {img['path']}")
        
    print("\nLinked User Profile Summary:")
    print(f"  - Summary: {payload['user_profile']['history_summary']}")
    print(f"  - Risk Flags: {payload['user_profile']['history_flags']}")
    
    print(f"\nLinked Rules Count: {len(payload['rules'])} guidelines attached.")
    for rule in payload['rules']:
        print(f"  - [{rule['requirement_id']}] Applies to: {rule['applies_to']}")

if __name__ == "__main__":
    test_pipeline()