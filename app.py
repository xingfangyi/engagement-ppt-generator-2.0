import streamlit as st
from modules.ppt_parser import parse_survey_ppt
from modules.ppt_builder import build_output_ppt

TEMPLATE_PATH = "templates/base_template.pptx"

st.set_page_config(
    page_title="Engagement Survey PPT Generator",
    page_icon="📊",
    layout="wide"
)

st.title("Engagement Survey to Development Actions PPT")
st.write("Upload a survey result PPT and generate a new PPT based on the base template.")

uploaded_file = st.file_uploader("Upload survey result PPT", type=["pptx"])

if uploaded_file is not None:
    try:
        data = parse_survey_ppt(uploaded_file)

        st.subheader("Parsed Data")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Department", data["department"])
        col2.metric("Engagement", data["overall_score"])
        col3.metric("Company", data["company_score"])
        col4.metric("Responded", data["responded_count"])

        st.write("### Top Strengths")
        if data["strengths"]:
            for item in data["strengths"]:
                st.write(f"- **{item['title']}**: {item['statement']}")
        else:
            st.write("No strengths detected.")

        st.write("### Top Opportunities")
        if data["opportunities"]:
            for item in data["opportunities"]:
                st.write(f"- **{item['title']}**: {item['statement']}")
        else:
            st.write("No opportunities detected.")

        st.write("### Bottom 10")
        if data["bottom_10"]:
            for idx, item in enumerate(data["bottom_10"], start=1):
                st.write(f"{idx}. {item['driver']} ({item['score']})")
        else:
            st.write("No bottom 10 detected.")

        if st.button("Generate PPT"):
            output_path = build_output_ppt(data, TEMPLATE_PATH)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download generated PPT",
                    data=f.read(),
                    file_name=f"{data['department']}_Development_Actions_2026.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

            st.success("PPT generated successfully.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("Please upload a PPT file.")
