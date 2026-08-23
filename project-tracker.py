import os
from datetime import datetime

def read_project_details():
    projects_dir = "projects"
    all_projects = []
    
    for project in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project)
        details_file = os.path.join(project_path, "details.txt")
        
        if os.path.isfile(details_file):
            with open(details_file, 'r') as f:
                content = f.read()
                all_projects.append({'name': project, 'details': content})
    
    return all_projects

def generate_report(projects):
    report = "=" * 60 + "\n"
    report += "CYBERSECURITY PROJECTS TRACKER REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 60 + "\n\n"
    report += f"Total Projects: {len(projects)}\n\n"
    
    for i, project in enumerate(projects, 1):
        report += f"--- Project {i} ---\n"
        report += f"Folder: {project['name']}\n"
        report += f"Details:\n{project['details']}\n\n"
    
    return report

if __name__ == "__main__":
    projects = read_project_details()
    report = generate_report(projects)
    
    print(report)
    
    with open("reports/project-report.txt", "w") as f:
        f.write(report)
    
    print("Report saved to: reports/project-report.txt")
