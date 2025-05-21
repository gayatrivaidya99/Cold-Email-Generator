

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    st.title("📧 Cold Email Generator")
    st.markdown("Automatically generate personalized cold emails from job postings using AI and your portfolio.")
    st.divider()

    # Input layout
    with st.form(key="url_form", clear_on_submit=False):
        url_input = st.text_input("Enter a job listing URL:", placeholder="Paste job URL here...")
        submit_button = st.form_submit_button("Submit")

    # Sidebar
    with st.sidebar:
        st.header("🧠 About this App")
        st.markdown("""
        This app does the following:
                    
🔍 Scrapes job descriptions from public job posting URLs

🤖 Uses a Groq-hosted LLM to extract structured information such as role, skills, experience, and description

🧠 Matches extracted skills with your personal project portfolio using ChromaDB vector search

✉️ Generates a personalized cold email tailored to the job, showcasing your relevant projects
        """)
        st.markdown("---")
        if st.checkbox("🔗 Show My Portfolio Projects"):
            df = portfolio.data[["Techstack", "Links"]]
            st.dataframe(df, use_container_width=True)
        st.caption("© 2025")

    if submit_button:
        try:
            with st.spinner("🔍 Scraping job listing..."):
                loader = WebBaseLoader([url_input])
                docs = loader.load()

            if not docs or not docs[0].page_content.strip():
                st.error("❌ Unable to extract readable content from this URL. Try another job page.")
                return

            page_content = docs[0].page_content
            data = clean_text(page_content)

            with st.spinner("📄 Extracting job information..."):
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

            # 🔒 Flatten and clean job list
            flat_jobs = []

            def flatten_jobs(j):
                if isinstance(j, dict):
                    flat_jobs.append(j)
                elif isinstance(j, list):
                    for item in j:
                        flatten_jobs(item)

            flatten_jobs(jobs)

            # # Optional: show structure
            # st.subheader("🧪 DEBUG: Flattened Jobs Structure")
            # st.write(flat_jobs)

            if not flat_jobs:
                st.warning("⚠️ No valid job entries found.")
                return

            st.success("✅ Job and project match found! Generating emails...")

            st.subheader("✉️ Generated Cold Emails")
            for idx, job in enumerate(flat_jobs):
                if not isinstance(job, dict):
                    st.warning(f"⚠️ Skipping invalid job entry at index {idx}: {job}")
                    continue

                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)

                with st.expander(f"📌 Email for Job #{idx + 1}: {job.get('role', 'Unknown Role')}"):
                    st.code(email, language='markdown')
                    st.markdown("**Matched Skills:** " + ", ".join(skills) if skills else "No skills matched.")
                    # if links:
                    #     # st.markdown("**Portfolio Links:**")
                    #     # Flatten links list (ChromaDB returns List[List[dict]])
                    #     flat_links = []
                    #     for sublist in links:
                    #         if isinstance(sublist, list):
                    #             flat_links.extend(sublist)
                    #         elif isinstance(sublist, dict):
                    #             flat_links.append(sublist)

                    #     if flat_links:
                    #         for item in flat_links:
                    #             st.markdown(f"- [{item.get('links')}]({item.get('links')})")
                    #     else:
                    #         st.markdown("No matching projects found.")

                    

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
