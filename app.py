# app.py (updated with error handling)
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from src.main import crew
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="GenAI Use Case Generator", layout="wide")

st.title("🚀 AI/GenAI Use Case Generator")

with st.sidebar:
    st.header("Configuration")
    company_name = st.text_input("Company Name", placeholder="Enter company name...")
    industry = st.text_input("Industry", placeholder="Enter industry...")
    generate_button = st.button("Generate Report")

def display_section(title, content):
    with st.expander(title):
        if isinstance(content, str):
            st.markdown(content)
        else:
            st.write(content)

if generate_button:
    if company_name and industry:
        with st.spinner("Generating AI use cases. This may take a few minutes..."):
            try:
                result = crew(company_name, industry)
                
                if result and "tasks_output" in result:
                    st.success("Report Generated Successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        display_section("📊 Industry Analysis", result["tasks_output"][0])
                        
                    with col2:
                        display_section("💡 AI Use Cases", result["tasks_output"][1])
                        
                    with col3:
                        display_section("🛠️ Implementation Resources", result["tasks_output"][2])
                    
                    # Optional: Add download button
                    report_content = f"# AI Use Case Report for {company_name}\n\n"
                    report_content += "## Industry Analysis\n" + result["tasks_output"][0] + "\n\n"
                    report_content += "## AI Use Cases\n" + result["tasks_output"][1] + "\n\n"
                    report_content += "## Implementation Resources\n" + result["tasks_output"][2]
                    
                    st.download_button(
                        label="Download Full Report",
                        data=report_content,
                        file_name=f"{company_name}_AI_Report.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("No results were generated. Please check your inputs and try again.")
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
    else:
        st.warning("Please fill in both company name and industry fields.")