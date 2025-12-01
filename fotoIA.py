import streamlit as st
import os
import replicate
from PIL import Image
import io
import requests

# =============================
# CONFIGURAÇÃO BÁSICA
# =============================
st.set_page_config(page_title="Melhorar Foto com IA", layout="centered")
st.title("🧠 Melhorar Foto com IA")
st.caption("Reconstrução de detalhes usando inteligência artificial")

# =============================
# TOKEN DO REPLICATE
# =============================
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# =============================
# UPLOAD DA IMAGEM
# =============================
uploaded_file = st.file_uploader(
    "📷 Envie uma foto",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.subheader("Original")
    st.image(image, use_column_width=True)

    if st.button("🚀 Melhorar com IA"):
        with st.spinner("IA processando..."):

            # chamada ao modelo de super-resolução
            output = replicate.run(
                "nightmareai/real-esrgan",
                input={
                    "image": uploaded_file.getvalue(),
                    "scale": 2
                }
            )

            # retorno é uma URL
            response = requests.get(output)
            img_final = Image.open(io.BytesIO(response.content))

        st.subheader("Melhorada com IA")
        st.image(img_final, use_column_width=True)

        # download
        buffer = io.BytesIO()
        img_final.save(buffer, format="PNG")
        buffer.seek(0)

        st.download_button(
            "⬇️ Baixar imagem melhorada",
            data=buffer,
            file_name="imagem_melhorada_ia.png",
            mime="image/png"
        )
else:
    st.info("Envie uma imagem para começar.")
