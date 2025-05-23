import streamlit as st
import pandas as pd

# Assuming EMPLOYEE_DB is the path to your employee data Excel file
EMPLOYEE_DB = "employee_data.xlsx"

def load_employee_data():
    """Loads the employee database from an Excel file."""
    return pd.read_excel(EMPLOYEE_DB)

def calculate_match_percentage(required_skills, emp_skills):
    """Calculates the match percentage based on skill overlap."""
    required_set = set(required_skills.split(", "))
    emp_set = set(emp_skills.split(", "))
    matched_skills = required_set.intersection(emp_set)
    return round((len(matched_skills) / len(required_set)) * 100, 2)

def match_employees(project_file):
    """Finds the best employees for each project based on exact and partial skill matching."""
    employees = load_employee_data()
    total_employees = len(employees)
    project_requirements = pd.read_excel(project_file)
    print(project_requirements)
    matched_projects = {}
    assigned_employees = set()  # Store emails of already assigned employees

    for _, project in project_requirements.iterrows():
        project_name = project["Project Name"]
        required_skills = project["Required Skills"]
        required_count = project["Number of People Required"]

        matched_candidates = []
        buffer_candidates = []

        for _, employee in employees.iterrows():
            emp_email = employee["Email"]
            if emp_email in assigned_employees:
                continue

            emp_skills = employee["Technical Skills"]
            match_percentage = calculate_match_percentage(required_skills, emp_skills)

            if match_percentage == 100:
                matched_candidates.append({
                    "Name": employee["Name"],
                    "Email": emp_email,
                    "Match Percentage": match_percentage
                })
                assigned_employees.add(emp_email)
                if len(matched_candidates) == required_count:
                    break
            elif match_percentage > 0:
                buffer_candidates.append({
                    "Name": employee["Name"],
                    "Email": emp_email,
                    "Match Percentage": match_percentage
                })

        # If not enough exact matches, fill remaining slots with best buffer candidates
        if len(matched_candidates) < required_count:
            buffer_candidates.sort(key=lambda x: x["Match Percentage"], reverse=True)
            for candidate in buffer_candidates:
                if len(matched_candidates) == required_count:
                    break
                matched_candidates.append(candidate)
                assigned_employees.add(candidate["Email"])

        # Store results
        if matched_candidates:
            formatted_matches = [
                f"{candidate['Name']} ({candidate['Email']}) - {candidate['Match Percentage']}% match"
                for candidate in matched_candidates
            ]
            matched_projects[project_name] = formatted_matches
    
    return matched_projects

@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")

# Streamlit UI
st.title("Employee Matching System")
st.write("Upload a Project Requirement file (Excel format) to get suitable employees.")

uploaded_file = st.file_uploader("Upload Project Requirements Excel", type=["xlsx"])

if uploaded_file:
    matched_results = match_employees(uploaded_file)
    print(matched_results)
    if not matched_results:
        st.write("No projects found with matching employees.")
    else:
        st.write("### Suggested Employees per Project:")
        results_df = pd.DataFrame(list(matched_results.items()), columns=["Project", "Matched Employees"])
        st.table(results_df)
        

    csv = convert_for_download(results_df)
    
    st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
    icon=":material/download:",
    )
