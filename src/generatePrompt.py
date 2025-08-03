from aiRequest import send_ai_request
import json
import re
from jinja2 import Environment, FileSystemLoader
import os 
import dotenv
# inputs: 
# string linkedInContent,
# jsonObject resumeData,
# string promptType ("resume", "coverLetter", "linkedin"),
# string promptSubType ("SkillsSection", WorkSection", "ProjectSection")
# output: sting prompt

def generate_prompt(linkedInContent, resumeData, promptType, promptSubType):
    # Load environment variables from .env file
    dotenv.load_dotenv()
    prompt_path = os.getenv('AI_PROMPT_PATH')
    template_dir = os.path.dirname(prompt_path)
    print(linkedInContent)
    print(resumeData)
    env = Environment(loader=FileSystemLoader(template_dir or '.'))
    if(promptType == "resume" and promptSubType == "WorkSection"):
        systemTemplate = env.get_template("systemWorkExperianceSection.jinja2")
        userPrompt = env.get_template("userWorkExperiancePrompt.jinja2")
        SystemPrompt = systemTemplate.render()
        userPrompt = userPrompt.render(
            linkedInContent=linkedInContent,
            resumeData=resumeData
        )
   
    elif(promptType == "resume" and promptSubType == "SkillsSection"):
        systemTemplate = env.get_template("systemSkillsSection.jinja2")
        userPrompt = env.get_template("userSkillsPrompt.jinja2")
        SystemPrompt = systemTemplate.render()
        userPrompt = userPrompt.render(
            linkedInContent=linkedInContent,
            resumeData=resumeData
        )
    
    elif(promptType == "resume" and promptSubType == "ProjectSection"):
        # print("Generating project section prompt")
        systemTemplate = env.get_template("systemProjectSection.jinja2")
        userPrompt = env.get_template("userProjectPrompt.jinja2")
        SystemPrompt = systemTemplate.render()
        userPrompt = userPrompt.render(
            linkedInContent=linkedInContent,
            resumeData=resumeData
        )
    return SystemPrompt, userPrompt


#############################################################
if __name__ == "__main__":
    jsonData = {
        "work_experience": [
            {
                "dates": "Mar 2023 -- Present",
                "title": "Systems Operations Engineer",
                "company": "Wells Fargo",
                "location": "Charlotte, NC",
                "responsibilities": [
                    "Maintained SLOs for front-end and back-end apps",
                    "Built dashboards in Grafana",
                    "Led MIM calls"
                ]
            }
        ]
    }
    system_prompt, user_prompt = generate_prompt(
        "Need local candidates The position requires a developer of components in a distributed, N-tier architecture collection of services and web applications, which work in concert to provide reliable solutions. The ideal candidate will have worked in a Test-Driven Development (TDD) environment utilizing a Scrum (Agile) methodology to provide end-to-end development. Our developers gather and analyze requirements, make architectural and design recommendations, code, document, and test their contributions in a high-energy, team-oriented environment. Software Developers are expected to contribute significantly to the formulation and design of the solution, not just coding the implementation.",
        jsonData,
        "resume",
        "WorkSection"
    )
    print("System Prompt:", system_prompt)
    print("User Prompt:", user_prompt)
    response = send_ai_request(system_prompt, user_prompt)
    print("AI Response:", response)
    raw= json.loads(response)
    # print(raw)
    aiResponse = raw.get("message", {}).get("content", "")
    clean = re.sub(r"([\`]{3}json|[\`]{3})", "", aiResponse)
    print("Cleaned Response:", clean)
# Parse the cleaned string into a dictionary
    data = json.loads(clean)
    print(data)

