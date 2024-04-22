import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import LoginError

import yaml
from yaml.loader import SafeLoader
from pororo_khc.pororo import Pororo

with open("./config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)


def replace_person_name(ner: Pororo, sentence: str, replace_str: str) -> str:
    entities = ner(sentence)
    for entity in entities:
        if entity[1] == "PERSON":
            sentence = sentence.replace(entity[0], replace_str)
    return sentence


# Creating the authenticator object
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)

# Creating a login widget
try:
    authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout()

    ner = Pororo(task="ner", lang="ko")

    st.title("Named Entity Recognition(NER)")
    st.markdown("***Model : proro NER, 0.4.1***")

    st.write("")
    st.write("")

    with st.form("my_form"):

        input_txt = st.text_area(
            "Input your text here",
            "오늘 자전거를 타다가 정명관이 다리를 다쳐 병원에 왔고, 홍길동 전문의가 담당해서 진료를 진행했다.",
        )

        submitted = st.form_submit_button(
            label="deidentificate",
            help=None,
            on_click=None,
            args=None,
            kwargs=None,
            type="secondary",
            disabled=False,
            use_container_width=False,
        )

        if submitted:

            st.text_area("Output", replace_person_name(ner, input_txt, "***"))

elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
