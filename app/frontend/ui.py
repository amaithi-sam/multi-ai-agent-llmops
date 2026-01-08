import streamlit as st
import requests 


from app.config.settings import settings 
from app.common.logger import get_logger 
from app.common.custom_exception import CustomException 

logger = get_logger(__name__)

st.set_page_config(page_title="Multi ai agent", layout="centered")
st.title("Multi ai agent using groq and tavily")

system_prompt = st.text_area("Defing your ai agent behavior : ", height=70)
selected_model = st.selectbox("Select your model: ", settings.ALLOWED_MODEL_NAMES)

allow_web_search = st.checkbox("Allow web search ")

user_query = st.text_area("Enter your question : ", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "model_name" : selected_model, 
        "system_prompt" : system_prompt,
        "messages" : [user_query],
        "allow_search" : allow_web_search
    }

    try:
        logger.info("Sending REquest to backend ")

        response = requests.post(API_URL, json=payload)

        logger.info(response)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received backed response")

            st.subheader("Agent Response ")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        else:
            logger.error("Backend Error")
            st.error("Errorr occured backend")


    except Exception as e:
        logger.error("Error occured while sending request to backend")
        st.error(str(CustomException("failed to communicate to backend")))




