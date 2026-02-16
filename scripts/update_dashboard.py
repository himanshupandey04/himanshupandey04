
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

    FALLBACK_PROJECTS = [
        {
            "name": "Real-Time-Doc-Validator-Instant-E-Challan-Relay",
            "html_url": "https://github.com/himanshupandey04/Real-Time-Doc-Validator-Instant-E-Challan-Relay",
            "description": "Auto-Traffic Enforcement System using Computer Vision & Flask.",
            "languages_cache": {"Python": 8000, "HTML": 1500, "CSS": 500}
        },
        {
            "name": "Blood-Donation-Management",
            "html_url": "https://github.com/himanshupandey04/Blood-Donation-Management",
            "description": "Full-stack MongoDB Inventory System for real-time donor tracking.",
            "languages_cache": {"HTML": 8000, "JavaScript": 1500, "CSS": 500}
        },
        {
            "name": "Fashion-Discount-Prediction",
            "html_url": "https://github.com/himanshupandey04/Fashion-Discount-Prediction",
            "description": "AI/ML Regression model for optimizing retail pricing strategies.",
            "languages_cache": {"Jupyter Notebook": 10000}
        },
        {
            "name": "Parking-Ticket-Issuing-System-using-OCR",
            "html_url": "https://github.com/himanshupandey04/Parking-Ticket-Issuing-System-using-OCR",
            "description": "Automated parking ticket solution using OCR-based license plate detection.",
            "languages_cache": {"Python": 9000, "C++": 1000}
        }
    ]

    try:
        response = requests.get(GITHUB_API)
        data = response.json()
        
        if not isinstance(data, list):
            print(f"API Error (Rate Limit/Other): {data}. Using Fallback.")
            return FALLBACK_PROJECTS
            
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
                
        if not selected_projects:
            return FALLBACK_PROJECTS
            
        return selected_projects
    except Exception as e:
        print(f"Error fetching projects: {e}. Using Fallback.")
        return FALLBACK_PROJECTS

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
        # Return a generic badge if no data (e.g. rate limited)
        return '<img src="https://img.shields.io/badge/ANALYZING-CODEBASE-ff69b4?style=flat-square" />'
    
    total_bytes = sum(languages.values())
    if total_bytes == 0:
        return ""
        
    bar_html = ""
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    
    # Limit to top 4
    for lang, bytes_count in sorted_langs[:4]:
        percent = round((bytes_count / total_bytes) * 100, 1)
        if percent > 1.0: # Filter tiny deps
            # Color mapping
            l_lower = lang.lower()
            color = "inactive"
            if l_lower == "python": color = "3776AB"
            elif l_lower == "javascript": color = "F7DF1E"
            elif l_lower == "html": color = "E34F26"
            elif l_lower == "css": color = "1572B6"
            elif l_lower == "jupyter notebook": color = "F37626"
            elif l_lower == "java": color = "007396"
            elif l_lower == "shell": color = "4EAA25"
            elif l_lower == "c++": color = "00599C"
            else: color = "333333"
            
            # Badge
            bar_html += f'<img src="https://img.shields.io/badge/{lang}-{percent}%25-{color}?style=flat-square" /> '
            
    return bar_html

def generate_markdown(projects):
    # Professional HTML Container Table with "Terminal" aesthetic
    base_asset_url = "https://raw.githubusercontent.com/himanshupandey04/himanshupandey04/main/assets/animated_icons"
    
    html_output = '<table width="100%" style="border-collapse: collapse; background-color: #0d1117; border: 1px solid #30363d; color: #e6edf3;">\n'
    
    # Header Row with Animated Icons
    html_output += '<thead style="background-color: #161b22; border-bottom: 1px solid #30363d;"><tr>'
    html_output += f'<th width="20%" align="left" style="padding: 10px;"><img src="{base_asset_url}/coding.gif" height="20" />&nbsp; MODULE</th>'
    html_output += f'<th width="45%" align="left" style="padding: 10px;"><img src="{base_asset_url}/brain.gif" height="20" />&nbsp; INTELLIGENCE / DESC</th>'
    html_output += f'<th width="25%" align="left" style="padding: 10px;"><img src="{base_asset_url}/data.gif" height="20" />&nbsp; TECH_STACK</th>'
    html_output += f'<th width="10%" align="center" style="padding: 10px;"><img src="{base_asset_url}/server.gif" height="20" />&nbsp; ACCESS</th>'
    html_output += '</tr></thead>\n<tbody>\n'
    
    for p in projects:
        name = p['name']
        url = p['html_url']
        desc = p['description'] if p['description'] else "System module active."
        if len(desc) > 90:
            desc = desc[:87] + "..."
            
        langs = get_repo_languages(name)
        if not langs and 'languages_cache' in p:
             langs = p['languages_cache']
             
        lang_bar = generate_language_bar(langs)
        
        html_output += '<tr style="border-bottom: 1px solid #21262d;">\n'
        html_output += f'<td valign="top" style="padding: 10px;"><a href="{url}" style="color: #58a6ff; text-decoration: none;"><b>{name}</b></a></td>\n'
        html_output += f'<td valign="top" style="padding: 10px;">{desc}</td>\n'
        html_output += f'<td valign="top" style="padding: 10px;">{lang_bar}</td>\n'
        html_output += f'<td valign="top" align="center" style="padding: 10px;"><a href="{url}"><img src="https://img.shields.io/badge/INITIALIZE-1f6feb?style=for-the-badge&logo=github&logoColor=white" height="25" /></a></td>\n'
        html_output += '</tr>\n'
        
    html_output += '</tbody></table>'
    return html_output

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
