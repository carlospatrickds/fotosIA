import streamlit as st
import replicate
import os
from PIL import Image

# token vem do secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.title("Melhorar Foto com IA")

uploaded = st.file_uploader("Envie uma foto", type=["jpg", "jpeg", "png"])

if uploaded:
    st.image(uploaded, caption="Original", use_column_width=True)

    with st.spinner("Processando com IA..."):
        output = replicate.run(
            "tencentarc/gfpgan:latest",
            input={"img": uploaded.getvalue()}
        )

    st.image(output, caption="Melhorada", use_column_width=True)
