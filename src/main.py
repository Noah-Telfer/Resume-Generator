import os 
import dotenv
from aiRequest import send_ai_request
from generatePrompt import generate_prompt
from generateLatexResume import generate_latex_resumes
import json
import traceback
import re
from cleanAIResponse import process_ai_response

def main():
    # Goal: Pass valid fields to the jinja2 template that have been enhanced to match the prompt

    # Step 1:
    # Step 1: Read in json and text file that contains description 
    dotenv.load_dotenv()
    resume_json_path = os.getenv('RESUME_LATEX_DETAILS_PATH')
    resume_output_path = os.getenv('RESUME_OUTPUT_PATH')
    linkedin_post_description_path = os.getenv('LINKEDIN_POST_DESCRIPTION_PATH')
    print(f"Loaded paths:\n  Resume JSON: {resume_json_path}\n  Output: {resume_output_path}\n  LinkedIn Description: {linkedin_post_description_path}")

    # Step 2: Pull files from directory 
    try:
        with open(resume_json_path, "r") as f:
            resume_data = json.load(f)
        print("Loaded resume data.")
    except Exception as e:
        print("Error loading resume data:", str(e))
        traceback.print_exc()
        return

    try:
        with open(linkedin_post_description_path, "r") as f:
            linkedin_post_json = json.load(f)
        print("Loaded LinkedIn post description.")
    except Exception as e:
        print("Error loading LinkedIn post description:", str(e))
        traceback.print_exc()
        return

    # Step 3: Organize prompts 
    try:
        work_experience = {}
        skills_section = {}
        project_section = {}
        
        work_experience["work_experience"] = resume_data[0].get("work_experience", [])
        # print(f"Work experience count: {len(work_experience)}")
        linkedin_post_description = linkedin_post_json.get("description", "")
        # print(f"LinkedIn post description: {linkedin_post_description[:100]}...")
        project_section["projects"] = resume_data[0].get("projects", [])
        print(f"Project section count: {len(project_section['projects'])}")
    except Exception as e:
        print("Error organizing prompts:", str(e))
        traceback.print_exc()
        return

    # Step 4: Generate prompts for AI
    try:
        # Work experience section
        print("Generating prompts for AI...")
        print(linkedin_post_description)
        print(work_experience)
        system_prompt, user_prompt = generate_prompt(
            linkedin_post_description,
            work_experience,
            "resume",
            "WorkSection"
        )
        print("System Prompt:", system_prompt)
        print("User Prompt:", user_prompt)
        
        # Skills section
        # system_prompt_skills, user_prompt_skills = generate_prompt(
        #     linkedin_post_description,
        #     resume_data,
        #     "resume",
        #     "SkillsSection"
        # )
        # print("System Prompt (Skills):", system_prompt_skills)
        # print("User Prompt (Skills):", user_prompt_skills)

        # Project section
        system_prompt_projects, user_prompt_projects = generate_prompt(
            linkedin_post_description,
            project_section,
            "resume",
            "ProjectSection"
        )
        print("System Prompt (Projects):", system_prompt_projects)
        print("User Prompt (Projects):", user_prompt_projects)

        print("Generated prompts for AI.")

    except Exception as e:
        print("Error generating prompts:", str(e))
        traceback.print_exc()
        return

    # Step 5: Send prompts to the AI and process response

    clean_Work_Response = process_ai_response(system_prompt, user_prompt)
    cleanProjectResponse = json.loads(process_ai_response(system_prompt_projects, user_prompt_projects))


    # Step 6: Combine updated data with original json and submit to jinja2
    try:
        aiResponse_json = json.loads(clean_Work_Response)
        for work in resume_data[0]["work_experience"]:
            for newWork in aiResponse_json:
                print(f"Checking work title: {work.get('title')} against new work title: {newWork.get('title')}")
                if newWork.get("title") == work.get("title"):
                    work["responsibilities"] = newWork.get("responsibilities", [])
                    print(f"Updated responsibilities for {work['title']}: {work['responsibilities']}")
        
        # update project section 
        for project in resume_data[0]["projects"]:
            for newProject in cleanProjectResponse:
                print(f"Checking project title: {project.get('title')} against new project title: {newProject.get('title')}")
                if newProject.get("title") == project.get("title"):
                    project["details"] = newProject.get("details", "")
                    print(f"Updated details for {project['title']}: {project['details']}")
        print("Updated resume data with AI response.")
    except Exception as e:
        print("Error updating resume data:", str(e))
        traceback.print_exc()
        return

    # Step 7: Generate LaTeX resume(s)
    try:
        print(resume_data)
        generate_latex_resumes(resume_data)
        print("Generated LaTeX resume(s).")
    except Exception as e:
        print("Error generating LaTeX resume(s):", str(e))
        traceback.print_exc()
        return
    
if __name__ == "__main__":
    print("hello will start now ")
    main()
