import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Define departments and skills
departments = {
    "Data Science": ["Python", "SQL", "Machine Learning", "Power BI", "Statistics"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "Cybersecurity": ["Network Security", "Linux", "Penetration Testing", "Firewall Management"],
    "Cloud Computing": ["AWS", "Azure", "Docker", "Kubernetes"],
    "Software Development": ["Java", "Spring Boot", "C#", ".NET", "Microservices"],
    "Project Management": ["Agile", "Scrum", "Risk Management", "Stakeholder Communication"]
}

# Generate 500 dummy employees
employee_data = []
for _ in range(500):
    name = fake.name()
    email = fake.email()
    department = random.choice(list(departments.keys()))
    skills = ", ".join(random.sample(departments[department], k=random.randint(2, 4)))  # Select 2-4 skills

    employee_data.append([name, email, department, skills])

# Create a DataFrame
df = pd.DataFrame(employee_data, columns=["Name", "Email", "Department", "Technical Skills"])

# Save to Excel
df.to_excel("employee_data.xlsx", index=False)

print("500 dummy employee records have been created successfully in 'employee_data.xlsx'.")
