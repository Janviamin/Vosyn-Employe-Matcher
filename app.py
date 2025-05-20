import streamlit as st
import pandas as pd

# ----------- UI Setup -----------
st.set_page_config(page_title="Project Skill Matcher", layout="wide")
st.title("💼 Project Skill Matcher")
st.markdown("Match employees to projects based on **complete skill alignment**.")

st.markdown("---")

# ----------- Function to check full match -----------
def fully_matches(required_skills, employee_skills):
    return set(required_skills).issubset(set(employee_skills))

# ----------- Upload Project Requirements File -----------
st.header("📁 Upload Project Requirements File")
project_file = st.file_uploader("Choose a CSV file with columns: Project, Required_Skills, Number_of_People_Required", type=["csv"])

# ----------- Load Employee Data -----------
try:
    employee_data = pd.read_csv("employees.csv")
    if "Employee" not in employee_data.columns or "Skills" not in employee_data.columns:
        st.error("❌ 'employees.csv' must contain 'Employee' and 'Skills' columns.")
        st.stop()
    employee_data["Skills"] = employee_data["Skills"].apply(lambda x: [s.strip() for s in x.split(";")])
except Exception as e:
    st.error(f"❌ Failed to load 'employees.csv': {e}")
    st.stop()

# ----------- Main Processing -----------
if project_file:
    try:
        project_data = pd.read_csv(project_file)

        required_columns = {"Project", "Required_Skills", "Number_of_People_Required"}
        if not required_columns.issubset(set(project_data.columns)):
            st.error("❌ Project CSV must contain 'Project', 'Required_Skills', and 'Number_of_People_Required'.")
            st.stop()

        project_data["Required_Skills"] = project_data["Required_Skills"].apply(lambda x: [s.strip() for s in x.split(";")])
        result_rows = []

        st.markdown("### 🧠 Match Results")

        for _, proj_row in project_data.iterrows():
            proj_name = proj_row["Project"]
            required_skills = proj_row["Required_Skills"]
            people_needed = proj_row["Number_of_People_Required"]

            matched_employees = []
            for _, emp_row in employee_data.iterrows():
                emp_name = emp_row["Employee"]
                emp_skills = emp_row["Skills"]

                if fully_matches(required_skills, emp_skills):
                    matched_employees.append(emp_name)

            top_employees = matched_employees[:5]

            result_rows.append({
                "🗂️ Project": proj_name,
                "👥 People Needed": people_needed,
                "✅ Fully Matched Employees": len(matched_employees),
                "🏆 Top 5 Employees": ", ".join(top_employees) if top_employees else "None"
            })

        results_df = pd.DataFrame(result_rows)

        st.success("✅ Matching complete!")
        st.dataframe(results_df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error processing project file: {e}")
