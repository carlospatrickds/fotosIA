import streamlit as st
import replicate
import os
from PIL import Image

# token vindo do Secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.set_page_config(page_title="Melhorar Foto com IA")
st.title("✨ Melhorar Foto com IA")
st.write("Envie uma foto borrada e a IA irá melhorar automaticamente.")

uploaded = st.file_uploader(
    "Envie uma imagem (JPG ou PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Imagem original", use_column_width=True)

    if st.button("🚀 Melhorar com IA"):
        with st.spinner("Processando com IA..."):
            output = replicate.run(
                "tencentarc/gfpgan",
                input={
                    "img": replicate.File(uploaded)
                }
            )

        st.image(output, caption="Imagem melhorada", use_column_width=True)
