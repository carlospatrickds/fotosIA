import streamlit as st
import replicate
import os
from PIL import Image
import base64 # Novo import para codificação
from io import BytesIO # Novo import para manipular a imagem

# ... (Seu código de configuração e st.set_page_config permanece o mesmo) ...

# ... (O código de st.file_uploader permanece o mesmo) ...

# --- Processamento ---
if uploaded:
    # 1. Mostrar Imagem Original
    image = Image.open(uploaded)
    st.image(image, caption="Imagem Original", use_column_width=True)
    
    st.markdown("---")

    if st.button("🚀 Melhorar com IA"):
        with st.spinner("Processando com IA..."):
            try:
                # 1. Obter os bytes do arquivo
                image_bytes = uploaded.getvalue()
                
                # 2. Codificar os bytes em Base64
                encoded_string = base64.b64encode(image_bytes).decode('utf-8')
                
                # 3. Criar o Data URI string
                # Determinando o tipo MIME (ex: image/jpeg)
                mime_type = f"image/{uploaded.type.split('/')[-1]}"
                data_uri = f"data:{mime_type};base64,{encoded_string}"
                
                # 4. Chamar o Replicate com o Data URI (String JSON serializável)
                output = replicate.run(
                    "tencentarc/gfpgan:9283a8f5c023d6be8e6f477a3d573359902316e0b79901265785317d7a9ad2e3",
                    input={
                        "img": data_uri, # Agora é uma string, que é JSON serializável
                        "scale": 2, 
                        "fidelity_weight": 0.5 
                    }
                )

                # 5. Mostrar Imagem Melhorada
                if output and isinstance(output, str):
                    st.image(output, caption="Imagem Melhorada pela IA", use_column_width=True)
                else:
                    st.error("A IA não retornou uma URL de imagem válida.")

            except replicate.exceptions.ReplicateError as e:
                st.error(f"Ocorreu um erro ao chamar a API do Replicate. Verifique o console para mais detalhes.")
                st.info(f"Erro: {e}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
                st.info("Atenção: A imagem pode ser muito grande para ser enviada via Data URI.")

st.markdown("---")
st.caption("Desenvolvido usando Streamlit e GFPGAN (via Replicate).")
