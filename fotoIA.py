import streamlit as st
import replicate
import os
from PIL import Image
from io import BytesIO # Importe BytesIO se precisar embrulhar os bytes

# ... (código anterior)

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Imagem original", use_column_width=True)

    if st.button("🚀 Melhorar com IA"):
        with st.spinner("Processando com IA..."):
            # AQUI ESTÁ A MUDANÇA
            # Use uploaded.getvalue() para obter o conteúdo binário do arquivo.
            output = replicate.run(
                "tencentarc/gfpgan",
                input={
                    # O Replicate é frequentemente capaz de lidar com bytes diretamente
                    # ou você pode usar uploaded (o objeto file-like)
                    "img": uploaded.getvalue()
                }
            )

        # O output do Replicate para este modelo é uma URL da imagem,
        # que o st.image pode exibir.
        st.image(output, caption="Imagem melhorada", use_column_width=True)
