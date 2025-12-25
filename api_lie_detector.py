#!/usr/bin/env python3
"""
API Docs Lie Detector - Because documentation lies more than a politician during election season.
"""

import requests
import json
import sys
from typing import Dict, Any, Optional

def detect_lies(api_url: str, expected_response: Dict[str, Any], method: str = "GET", **kwargs) -> None:
    """
    Compare reality (actual API) with fiction (documentation).
    
    Args:
        api_url: Where the API claims to live
        expected_response: What the docs PROMISED would happen
        method: HTTP method - because sometimes they forget which one works
        **kwargs: Additional requests parameters (headers, data, etc.)
    
    Returns:
        Disappointment and possibly a working API call
    """
    
    print(f"\n🔍 Investigating: {api_url}")
    print(f"📚 Docs claim: {json.dumps(expected_response, indent=2)}")
    
    try:
        # Reality check - what ACTUALLY happens
        response = requests.request(method, api_url, **kwargs, timeout=10)
        
        print(f"\n📊 Reality says:")
        print(f"Status: {response.status_code} {'✅' if response.ok else '❌'}")
        
        if response.headers.get('Content-Type', '').startswith('application/json'):
            actual_data = response.json()
            print(f"Response: {json.dumps(actual_data, indent=2)}")
            
            # The moment of truth - does reality match the fairy tale?
            if actual_data == expected_response:
                print("\n🎉 Miracles happen! Docs are (mostly) accurate!")
            else:
                print("\n🤥 Surprise! Documentation lied! (Or maybe you misread? Nah, probably lied.)")
                print("Differences found between promise and reality.")
        else:
            print(f"Response: {response.text[:200]}...")
            print("\n⚠️  Non-JSON response - docs might be lying about format too!")
            
    except requests.exceptions.RequestException as e:
        print(f"\n💀 API is dead, missing, or pretending to be offline: {e}")
    except json.JSONDecodeError:
        print("\n🤡 API returned invalid JSON - another lie uncovered!")

def main() -> None:
    """Main function - because every script needs one, apparently."""
    
    if len(sys.argv) < 3:
        print("Usage: python api_lie_detector.py <api_url> '<expected_json>'")
        print("Example: python api_lie_detector.py \"https://api.example.com/users/1\" '{\"id\":1,\"name\":\"John\"}'")
        sys.exit(1)
    
    api_url = sys.argv[1]
    
    try:
        expected_response = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print("Error: Invalid JSON in expected response")
        sys.exit(1)
    
    # Optional: Add headers or data from command line if needed
    headers = {"User-Agent": "API-Lie-Detector/1.0 (TrustNoDocs)"}
    
    detect_lies(api_url, expected_response, headers=headers)

if __name__ == "__main__":
    main()
