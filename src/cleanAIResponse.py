import json
import re
import traceback
from aiRequest import send_ai_request
    
def process_ai_response(system_prompt, user_prompt):
    try:
        response = send_ai_request(system_prompt, user_prompt)
        raw = json.loads(response)
        aiResponse = raw.get("message", {}).get("content", "")
        print("Raw AI content:", aiResponse)
        aiResponse = re.sub(r"\n[\`]{3}json", ",", aiResponse)
        clean = re.sub(r"([\`]{3}json|[\`]{3})", "", aiResponse)
        print("Cleaned Response:", clean)
        return clean
    except Exception as e:
        print("Error processing AI response:", str(e))
        traceback.print_exc()
        return None