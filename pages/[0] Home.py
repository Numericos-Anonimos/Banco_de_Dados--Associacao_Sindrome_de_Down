import streamlit as st
from PIL import Image
import base64
from io import BytesIO


#st.set_page_config(page_title="Sistema ASIN", page_icon="Imagens/LogoASIN.png", layout="wide")
#st.html('''<style>
#            #MainMenu {visibility: hidden;}
#            footer {visibility: hidden;}
#            header {visibility: hidden;} 
#        </style>''')


# Função para converter a imagem para base64
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()




st.title("ASIN - Associação Sindrome de Down")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap='small')

with col1:
        with st.container(border=True):
            st.page_link("pages/[1] Atendidos.py", label="📋 **Atendidos**")
            st.caption("Área para a visualização dos atentidos")
        with st.container(border=True):
            st.page_link("pages/[2] Colaboradores.py", label="👥 **Colaboradores**")
            st.caption("Área para a visualização dos colaboradores")
        with st.container(border=True):
            st.page_link("pages/[5] Projetos.py", label="📊 **Projetos**")
            st.caption("Visualização das projetos realizados")

with col2:
        with st.container(border=True):
            st.page_link("pages/[4] Oficinas.py", label="🛠️ **Oficinas**")
            st.caption("Visualização das Oficinas disponibilizadas")
        with st.container(border=True):
            st.page_link("pages/[3] Eventos.py", label="🎉 **Eventos**")
            st.caption("Visualização das eventos realizados")


st.markdown("---")
st.subheader("Introdução ao ASIN: Entenda Sua Importância")
st.write("Trata-se de uma associação sem fins lucrativos que, desde sua fundação em 1990, tem desempenhado um papel crucial no atendimento assistencial a pessoas com Síndrome de Down e outras deficiências. Além disso, a ASIN oferece um suporte fundamental às famílias dessas pessoas, atuando na cidade de São José dos Campos – SP. A missão da organização vai além do atendimento básico: ela busca promover a inclusão plena de pessoas com deficiência intelectual tanto no ambiente familiar quanto no meio social, proporcionando oportunidades para seu desenvolvimento, autonomia e participação ativa na sociedade. Por meio de suas ações, a ASIN assegura que esses indivíduos tenham seus direitos à cidadania plenamente garantidos, colaborando para a construção de uma sociedade mais inclusiva e igualitária.		")



st.markdown("<br>", unsafe_allow_html=True)
# Carregar e redimensionar a imagem
imagem = Image.open("Imagens/pilates.jpg")
imagem = imagem.resize((700, 500))

# Exibir a imagem com borda, cantos arredondados e centralização usando markdown
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/jpeg;base64,{}" width="700" height="450" style="border: 1px solid #002b3d; border-radius: 10px;">
    </div>
    """.format(image_to_base64(imagem)),
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("**Objetivo do Projeto**")
st.write("""
Nosso principal foco é o gerenciamento dos horários dos atendidos, e isso será feito de três maneiras principais:
- Integrando os horários com os registros de presença diários, facilitando o envio das informações obrigatórias ao governo.
- Criando listas organizadas para que as cuidadoras acompanhem os atendidos às próximas oficinas de maneira eficiente.
- Visualizando a programação semanal de um atendido, permitindo um planejamento otimizado e personalizado.

Essa estrutura permite um controle ainda mais rigoroso, um acompanhamento mais preciso e uma eficiência significativamente aprimorada para as atividades cotidianas da instituição, garantindo uma gestão mais organizada, transparente e eficaz. A centralização das informações e a automação de processos possibilita uma redução no tempo gasto com tarefas manuais, além de minimizar erros e inconsistências que podem surgir com métodos tradicionais. Dessa forma, a equipe poderá se concentrar em atividades estratégicas e no atendimento direto às necessidades dos atendidos e suas famílias.
""")

st.markdown("---")
st.title("Conheça Nossa Equipe")

st.markdown("""
        <div style="text-align: justify;">
            Queremos prestar todo o nosso apoio aos usuários, nos colocando à disposição para ajudar no que for necessário. Nosso compromisso é garantir que a experiência no site seja a melhor possível, oferecendo suporte contínuo, ouvindo feedbacks e buscando sempre melhorias. Acreditamos que um ambiente colaborativo e acessível é essencial para que todos possam aproveitar ao máximo as ferramentas e recursos que disponibilizamos. Para isso, deixamos abaixo os contatos dos criadores, para que você possa entrar em contato sempre que precisar, seja para esclarecer dúvidas, sugerir melhorias ou apenas trocar ideias. Estamos aqui para ajudar!
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if "show_contacts" not in st.session_state:
        st.session_state["show_contacts"] = False

if st.button("Mostrar Contatos"):
        st.session_state["show_contacts"] = not st.session_state["show_contacts"]

if st.session_state["show_contacts"]:
    st.markdown("""
            <style>
                .contact-box {
                    border: 2px solid #4CAF50;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    margin-top: 10px;
                    text-align: left;
                    background-color: transparent;
                }
                .contact-container {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .contact-item {
                    font-size: 16px;
                    font-weight: bold;
                }
                .contact-item a {
                    text-decoration: none;
                    color: #4CAF50;
                }
                .contact-item a:hover {
                    text-decoration: underline;
                }
            </style>

            <div class="contact-box">
                <h4>👥 Contatos dos Criadores</h4>
                <div class="contact-container">
                    <div class="contact-item">
                        - João Victor Assaoka Ribeiro / <a href="https://linkedin.com/in/assaoka" target="_blank">LinkedIn</a> / <a href="https://github.com/Assaoka" target="_blank">Github</a>
                    </div>
                    <div class="contact-item">
                        - Lucas Molinari / <a href="https://linkedin.com/in/lucas-molinari-dev" target="_blank">LinkedIn</a> / <a href="https://github.com/molhinari" target="_blank">Github</a>
                    </div>
                    <div class="contact-item">
                        - Miguel Gustavo Santos Rangel / <a href="https://linkedin.com/in/miguel-rangel-534218217" target="_blank">LinkedIn</a> / <a href="https://github.com/mr-miguelrangel" target="_blank">Github</a>
                    </div>
                    <div class="contact-item">
                        - Thomas Pires Correia / <a href="https://linkedin.com/in/thomas-pires-correia-84ab55226" target="_blank">LinkedIn</a> / <a href="https://github.com/Th0m4sma" target="_blank">Github</a>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)








with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)