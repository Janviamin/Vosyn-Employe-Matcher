import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Define possible departments and required skills
departments = {
    "Data Science": ["Python", "SQL", "Machine Learning", "Power BI", "Statistics"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "Cybersecurity": ["Network Security", "Linux", "Penetration Testing", "Firewall Management"],
    "Cloud Computing": ["AWS", "Azure", "Docker", "Kubernetes"],
    "Software Development": ["Java", "Spring Boot", "C#", ".NET", "Microservices"],
    "Project Management": ["Agile", "Scrum", "Risk Management", "Stakeholder Communication"]
}

# Generate 10 random projects
project_data = []
for i in range(10):
    project_name = f"Project {i+1}: {fake.bs().title()}"  # Generates a business-sounding project name
    department = random.choice(list(departments.keys()))  # Random department
    required_skills = ", ".join(random.sample(departments[department], k=random.randint(2, 4)))  # Pick 2-4 skills
    number_of_people = random.randint(1, 5)  # Number of people required for the project
    project_data.append([project_name, department, required_skills, number_of_people])

# Create a DataFrame
df = pd.DataFrame(project_data, columns=["Project Name", "Department", "Required Skills", "Number of People Required"])

# Save to Excel
df.to_excel("project_requirements.xlsx", index=False)

print("10 random project requirements have been created successfully in 'project_requirements.xlsx'.")