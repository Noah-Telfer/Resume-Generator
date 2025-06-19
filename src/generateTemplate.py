import os
import json
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Required paths from environment variables
resume_data_path = os.getenv('RESUME_JSON_PATH')
template_config_path = os.getenv('RESUME_TEMPLATE_DETAILS_PATH')  # now a JSON with template info
template_path= os.getenv('RESUME_TEMPLATE_PATH')
output_dir = os.getenv('RESUME_OUTPUT_PATH')

if not all([resume_data_path, template_config_path, output_dir, template_path]):
    raise ValueError("One or more required environment variables are missing.")

# Load resume content
with open(resume_data_path) as f:
    resume_data = json.load(f)

# Load template config JSON (containing template names and files)
with open(template_config_path) as f:
    template_config = json.load(f)

# Access the template dictionary
templates = template_config.get("TemplateName", {})

# Loop through each template entry
for template_name, info in templates.items():
    template_file = info["fileName"]
    template_dir = os.path.dirname(template_path)
    template_filename = os.path.basename(template_file)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir or '.'))
    template = env.get_template(template_filename)

    # Render output
    rendered_resume = template.render(**resume_data)

    # Define output file path
    safe_name = template_name.lower().replace(" ", "_")
    output_file_path = os.path.join(output_dir, f"resume_{safe_name}.html")

    # Write rendered HTML
    with open(output_file_path, 'w') as f:
        f.write(rendered_resume)

    print(f"✅ Resume generated: {output_file_path}")
