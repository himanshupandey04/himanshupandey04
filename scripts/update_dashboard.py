
import requests
import os
from datetime import datetime

# USERNAME = "himanshupandey04"
# Using GitHub API for automatic updates
GITHUB_API = "https://api.github.com/users/himanshupandey04/repos"

def get_projects():
    # Manual overrides for specific projects to ensure professional descriptions
    project_metadata = {
        "real-time-doc-validator-instant-e-challan-relay": "Auto-Traffic Enforcement System using Computer Vision & Flask.",
        "blood-donation-management": "Full-stack MongoDB Inventory System for real-time donor tracking.",
        "fashion-discount-prediction": "AI/ML Regression model for optimizing retail pricing strategies.",
        "parking-ticket-issuing-system-using-ocr": "Automated parking ticket solution using OCR-based license plate detection."
    }

    try:
        response = requests.get(GITHUB_API)
        data = response.json()
        
        # Sort by updated_at (newest first)
        projects = sorted(data, key=lambda x: x['updated_at'], reverse=True)
        
        # Select Top 5 Public Projects (excluding the profile repo)
        selected_projects = []
        for p in projects:
            if p['name'].lower() == "himanshupandey04":
                continue
            if not p['fork']: # Original work only
                # Apply manual metadata if available
                p_name_lower = p['name'].lower()
                if p_name_lower in project_metadata:
                    p['description'] = project_metadata[p_name_lower]
                elif not p['description']:
                    p['description'] = "—"
                
                selected_projects.append(p)
            if len(selected_projects) >= 5:
                break
                
        return selected_projects
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []

def get_repo_languages(repo_name):
    try:
        url = f"https://api.github.com/repos/himanshupandey04/{repo_name}/languages"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def generate_language_bar(languages):
    if not languages:
        return ""
    
    total_bytes = sum(languages.values())
    if total_bytes == 0:
        return ""
        
    bar_md = ""
    # Sort by size
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    
    # Limit to top 3 to avoid clutter
    for lang, bytes_count in sorted_langs[:3]:
        percent = round((bytes_count / total_bytes) * 100, 1)
        if percent > 5: # Only show significant languages
            # Clean color name for shield
            color = "blue"
            l_lower = lang.lower()
            if l_lower == "python": color = "3776AB"
            elif l_lower == "javascript": color = "F7DF1E"
            elif l_lower == "html": color = "E34F26"
            elif l_lower == "css": color = "1572B6"
            elif l_lower == "jupyter notebook": color = "F37626"
            elif l_lower == "java": color = "007396"
            
            # Create a simple text-based representation or shield
            # bar_md += f"![{lang}](https://img.shields.io/badge/{lang}-{percent}%25-{color}) "
            bar_md += f"**{lang}** {percent}% "
            
    return bar_md

def generate_markdown(projects):
    """Generates the Markdown table for the projects."""
    md = "| **PROJECT** | **DESCRIPTION** | **LANGUAGES / TOOLS** | **ACTION** |\n"
    md += "| :--- | :--- | :--- | :---: |\n"
    
    for p in projects:
        name = f"[{p['name']}]({p['html_url']})"
        desc = p['description'] if p['description'] else "No description provided."
        if len(desc) > 80:
            desc = desc[:77] + "..."
            
        # Fetch detailed languages
        langs = get_repo_languages(p['name'])
        lang_bar = generate_language_bar(langs)
        
        # Contribution Badge
        contrib_link = f"[![Contribute](https://img.shields.io/badge/DO_CONTRIBUTION-000000?style=flat&logo=github&logoColor=white)]({p['html_url']})"
        
        md += f"| {name} | {desc} | {lang_bar} | {contrib_link} |\n"
        
    return md

def update_readme():
    projects = get_projects()
    new_content = generate_markdown(projects)
    
    readme_path = "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        start_marker = "<!-- START_PROJECTS -->"
        end_marker = "<!-- END_PROJECTS -->"
        
        if start_marker in content and end_marker in content:
            start_index = content.find(start_marker) + len(start_marker)
            end_index = content.find(end_marker)
            
            updated_content = content[:start_index] + "\n\n" + new_content + "\n" + content[end_index:]
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("README.md updated successfully with latest projects.")
        else:
            print("Markers not found in README.md")
            
    except Exception as e:
        print(f"Error updating README: {e}")

if __name__ == "__main__":
    update_readme()
