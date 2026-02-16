
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
        "fashion-discount-prediction": "AI/ML Regression model for optimizing retail pricing strategies."
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

def generate_markdown(projects):
    """Generates the Markdown table for the projects."""
    md = "| **PROJECT MODULE** | **DESCRIPTION** | **TECH STACK** | **LAST UPDATE** |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    
    for p in projects:
        name = f"[{p['name']}]({p['html_url']})"
        desc = p['description'] if p['description'] else "No description provided."
        # Truncate desc if too long
        if len(desc) > 60:
            desc = desc[:57] + "..."
            
        lang = p['language'] if p['language'] else "Unknown"
        
        # Mapping language to shield icon
        lang_icon = ""
        if lang:
            l_lower = lang.lower()
            color = "black" # consistent style
            logo = l_lower
            if l_lower == "jupyter notebook": logo = "jupyter"; color="F37626"
            elif l_lower == "html": logo="html5"; color="E34F26"
            elif l_lower == "css": logo="css3"; color="1572B6"
            elif l_lower == "python": logo="python"; color="3776AB"
            elif l_lower == "javascript": logo="javascript"; color="F7DF1E"
            
            lang_icon = f"![{lang}](https://img.shields.io/badge/-{lang}-black?style=flat-square&logo={logo}&logoColor=white)"

        updated = datetime.strptime(p['updated_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
        
        md += f"| {name} | {desc} | {lang_icon} | {updated} |\n"
        
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
