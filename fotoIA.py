import streamlit as st
import replicate
import os
from PIL import Image

# Configuração do Replicate API Token
# O Streamlit lida com st.secrets automaticamente ao implantar na nuvem.
# Para rodar localmente, certifique-se de que "REPLICATE_API_TOKEN" está no arquivo .streamlit/secrets.toml
try:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
except FileNotFoundError:
    st.error("Erro: O arquivo secrets.toml não foi encontrado ou a chave 'REPLICATE_API_TOKEN' está faltando. Verifique sua configuração.")
    st.stop()
except KeyError:
    st.error("Erro: A chave 'REPLICATE_API_TOKEN' não está configurada nos seus segredos (secrets.toml).")
    st.stop()


# --- Configurações da Página ---
st.set_page_config(page_title="Melhorar Foto com IA", layout="centered")
st.title("✨ Melhorar Foto com IA com GFPGAN")
st.write("Envie uma foto borrada e a IA irá aprimorar rostos automaticamente.")

# --- Componente de Upload ---
uploaded = st.file_uploader(
    "Envie uma imagem (JPG ou PNG)",
    type=["jpg", "jpeg", "png"]
)

# --- Processamento ---
if uploaded:
    # 1. Mostrar Imagem Original
    image = Image.open(uploaded)
    st.image(image, caption="Imagem Original", use_column_width=True)
    
    st.markdown("---")

    if st.button("🚀 Melhorar com IA"):
        with st.spinner("Processando com IA... Isso pode levar alguns segundos."):
            try:
                # CORREÇÃO CRÍTICA: 
                # Passamos os bytes do arquivo usando uploaded.getvalue() para o Replicate.
                # Também especificamos uma versão estável do modelo.
                output = replicate.run(
                    "tencentarc/gfpgan:9283a8f5c023d6be8e6f477a3d573359902316e0b79901265785317d7a9ad2e3",
                    input={
                        "img": uploaded.getvalue(), # Passa os bytes do arquivo
                        "scale": 2, # Opcional: fator de escala. 2 é o padrão.
                        "fidelity_weight": 0.5 # Opcional: equilíbrio entre fidelidade e restauração.
                    }
                )

                # 2. Mostrar Imagem Melhorada
                if output and isinstance(output, str):
                    st.image(output, caption="Imagem Melhorada pela IA", use_column_width=True)
                else:
                    st.error("A IA não retornou uma URL de imagem válida.")

            except replicate.exceptions.ReplicateError as e:
                st.error(f"Ocorreu um erro ao chamar a API do Replicate: {e}")
                st.info("Verifique se seu token de API do Replicate está correto e se o serviço está ativo.")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

st.markdown("---")
st.caption("Desenvolvido usando Streamlit e GFPGAN (via Replicate).")
