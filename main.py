import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px

# File paths
credentials_file = "credentials.json"

# Initialize the credentials file if it doesn't exist
if not os.path.exists(credentials_file):
    with open(credentials_file, "w") as f:
        json.dump({}, f)

# Helper function to read credentials
def load_credentials():
    with open(credentials_file, "r") as f:
        return json.load(f)

# Helper function to write credentials
def save_credentials(credentials):
    with open(credentials_file, "w") as f:
        json.dump(credentials, f)

# Main logic for navigation between pages
def main():
    # Set default page if not already set
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"  # Default page is the login page

    # Load credentials from file
    credentials = load_credentials()

    # Display the appropriate page based on the current_page state
    if st.session_state.current_page == "login":
        login(credentials)
    elif st.session_state.current_page == "signup":
        signup(credentials)
    elif st.session_state.current_page == "subject_marks":
        subject_marks_page()
    elif st.session_state.current_page == "marks_chart":
        display_marks_chart()
    
    # Sidebar navigation (Login/Signup)
    if not st.session_state.get('logged_in', False):
        st.sidebar.radio("Choose an option", ["Login", "Signup"], 
                         key="page_selector", on_change=change_page)


# Function to change pages based on user input in sidebar
def change_page():
    st.session_state.current_page = st.session_state.page_selector.lower()


# Signup function
def signup(credentials):
    st.title("Signup Page")

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if email not in credentials:
            credentials[email] = {
                "name": name,
                "phone": phone,
                "dob": str(dob),
                "password": password
            }
            save_credentials(credentials)
            user_folder = os.path.join(os.getcwd(), name)
            os.makedirs(user_folder, exist_ok=True)
            st.success(f"User {name} registered successfully!")
        else:
            st.error("Email already exists!")

# Login function
def login(credentials):
    st.title("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Using a submit button with an on_change function
    if st.button("Submit", on_click=attempt_login, args=(credentials, email, password)):
        pass  # Button will call the function

def attempt_login(credentials, email, password):
    if email in credentials and credentials[email]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = credentials[email]["name"]
        st.session_state.user_folder = os.path.join(os.getcwd(), st.session_state.username)
        st.session_state.current_page = "subject_marks" 
    else:
        st.error("Invalid credentials!")

# Signout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_folder = ""
    st.session_state.current_page = "login"  # Go back to login page

# Subject marks input page
def subject_marks_page():
    st.sidebar.title(f"Welcome {st.session_state.username}")
    
    # Sign out button with on_click function
    if st.sidebar.button("Sign Out", on_click=logout):
        pass  # Button will call the function
    
    # Button will call the function

    st.title(f"Hello {st.session_state.username}, Enter Your Marks")
    
    marks = []
    subjects = ["Math", "Science", "English", "History", "Geography", "Art", "PE"]

    for subject in subjects:
        marks.append(st.slider(f"{subject} Marks", 0, 100, 50))

    if st.button("Submit", on_click=attempt_chart, args=(subjects, marks)):
        pass  # Button will call the function  # Go to chart page

# Marks chart display page
def attempt_chart(subjects,marks):
    marks_df = pd.DataFrame({
            "Subjects": subjects,
            "Marks": marks
        })

    marks_file = os.path.join(st.session_state.user_folder, "marks.csv")
    marks_df.to_csv(marks_file, index=False)

        # Set the current page to marks chart page
    st.session_state.current_page = "marks_chart"

def display_marks_chart():
    st.sidebar.title(f"Welcome {st.session_state.username}")
    
    # Sign out button with on_click function
    if st.sidebar.button("Sign Out", on_click=logout):
        pass  # Button will call the function

    # Load the marks from the CSV file
    marks_file = os.path.join(st.session_state.user_folder, "marks.csv")
    marks_df = pd.read_csv(marks_file)

    st.title(f"{st.session_state.username}'s Marks Distribution")

    # Display the marks distribution chart using Plotly
    fig = px.bar(marks_df, x="Subjects", y="Marks", title=f"{st.session_state.username}'s Marks Distribution")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

