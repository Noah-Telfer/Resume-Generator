from jinja2 import Environment, FileSystemLoader
import subprocess
import os
import dotenv
def generate_latex_resumes(context):
    # Load environment variables from .env file
    dotenv.load_dotenv()    
    # Required paths from environment variables
    # resume_data_path = os.getenv('REESUME_LATEX_DETAILS_PATH')
    resume_template_path = os.getenv('RESUME_TEMPLATE_LATEX_PATH')
    output_dir = os.getenv('RESUME_OUTPUT_PATH')

    template_dir = os.path.dirname(resume_template_path)
    template_filename = os.path.basename(resume_template_path)

    env = Environment(loader=FileSystemLoader(template_dir or '.'))
    template = env.get_template(template_filename)

    # with open(resume_data_path, "r") as f:
    #     import json
    #     context = json.load(f)

    for person in context:
        output_tex = template.render(**person)
        filename = f"{person['myname']}_{person['mysurname']}.tex"
        output_file_path = os.path.join(output_dir, f"latex_Resume.tex")
        with open(output_file_path, "w") as f:
            f.write(output_tex)
    # subprocess.run(["pdflatex", output_file_path])
    # print(f"✅ PDF generated: {output_file_path.replace('.tex', '.pdf')}")