from aiRequest import send_ai_request
import json
import re
# inputs: 
# string linkedInContent,
# jsonObject resumeData,
# string promptType ("resume", "coverLetter", "linkedin"),
# string promptSubType ("SkillsSection", WorkSection", "ProjectSection")
# output: sting prompt
def generate_prompt(linkedInContent, resumeData, promptType, promptSubType):
    SystemPrompt= """You are an assistant that extracts structured data from text. 

    Respond ONLY in this format:
    ```json
    {
    "name": "",
    "location": "",
    "job": ""
    }
    ```"""
    
    userPrompt = "My name is noah I'm from charlotte and I'm a dev"
    return SystemPrompt, userPrompt
if __name__ == "__main__":

    system_prompt, user_prompt = generate_prompt(
        "Sample LinkedIn content",
        {},
        "resume",
        "SkillsSection"
    )
    response = send_ai_request(system_prompt, user_prompt)
    raw= json.loads(response)
    # print(raw)
    aiResponse = raw.get("message", {}).get("content", "")
    clean = re.sub(r"^```(?:json)?\n|\n```$", "", aiResponse.strip())

# Parse the cleaned string into a dictionary
    data = json.loads(clean)
    print(data)

