import streamlit as st
import os
import replicate
from PIL import Image
import io

# ====================
# CONFIGURAÇÃO
# ====================
st.set_page_config(page_title="Melhorar Foto com IA", layout="centered")

st.title("✨ Melhorar Foto com IA")
st.write("Envie uma foto borrada e a IA irá melhorar automaticamente.")

# ====================
# TOKEN
# ====================
if "REPLICATE_API_TOKEN" not in st.secrets:
    st.error("Token do Replicate não configurado.")
    st.stop()

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# ====================
# UPLOAD
# ====================
uploaded_file = st.file_uploader(
    "Envie uma imagem (JPG ou PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem original", use_column_width=True)

    if st.button("✨ Melhorar com IA"):
        with st.spinner("Processando com IA..."):
            output = replicate.run(
                "tencentarc/gfpgan",
                input={
                    "img": uploaded_file.getvalue()
                }
            )

        st.success("Imagem melhorada!")
        st.image(output, caption="Imagem melhorada", use_column_width=True)
