import streamlit as st
from datetime import date
from time import sleep

st.session_state['current_page'] = "Home"

dados_funcionarios = [
    {
        "Cod": 1,
        "Nome": "João Assaoka",
        "CPF": "123.456.789-00",
        "Endereço": "Rua 1, 123",
        "Observações": "Nenhuma",
        "Salário": 1500.00,
        "Contatos": [(31999999999, "WhatsApp da mãe"), (12222222222, "Telefone fixo do trabalho do pai")],
        "Oficinas": {
            "SEG - 09:00 ÀS 10:00": "Informática",
            "QUA - 09:00 ÀS 10:00": "Música",
        },
        "Ponto": [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    },
    {
        "Cod": 2,
        "Nome": "Thomas Pires Correia",
        "CPF": "987.654.321-00",
        "Endereço": "Rua 2, 456",
        "Observações": "Trabalha meio período",
        "Salário": 2000.00,
        "Contatos": [(31988888888, "Próprio"), (11977777777, "Telefone fixo")],
        "Oficinas": {
            "TER - 14:00 ÀS 15:00": "Programação",
            "QUI - 10:00 ÀS 11:00": "Matemática",
        },
        "Ponto": [date(2021, 6, 1), date(2021, 6, 8), date(2021, 6, 15), date(2021, 6, 22)],
    },
    {
        "Cod": 3,
        "Nome": "Lucas Molinari",
        "CPF": "111.222.333-45",
        "Endereço": "Rua 3, 789",
        "Observações": "Nenhuma",
        "Salário": 1800.00,
        "Contatos": [(31955555555, "Celular"), (11944444445, "Telefone fixo")],
        "Oficinas": {
            "SEG - 10:00 ÀS 11:00": "Física",
            "SEX - 09:00 ÀS 10:00": "Química",
        },
        "Ponto": [date(2021, 7, 5), date(2021, 7, 12), date(2021, 7, 19), date(2021, 7, 26)],
    },
    {
        "Cod": 4,
        "Nome": "Marcelo Gustavo Felipe Campos",
        "CPF": "333.444.555-66",
        "Endereço": "Rua 4, 101",
        "Observações": "Nenhuma",
        "Salário": 2200.00,
        "Contatos": [(31955555556, "Celular"), (11944444446, "Telefone fixo")],
        "Oficinas": {
            "SEG - 10:00 ÀS 11:00": "Química",
            "SEX - 09:00 ÀS 10:00": "Física",
        },
        "Ponto": [date(2021, 8, 5), date(2021, 8, 12), date(2021, 8, 19), date(2021, 8, 26)],
    },
    {
        "Cod": 5,
        "Nome": "Miguel Costa Silva",
        "CPF": "444.555.666-77",
        "Endereço": "Rua 5, 202",
        "Observações": "Nenhuma",
        "Salário": 2500.00,
        "Contatos": [(31955555557, "Celular"), (11944444447, "Telefone fixo")],
        "Oficinas": {
            "TER - 14:00 ÀS 15:00": "Matemática",
            "QUI - 10:00 ÀS 11:00": "Programação",
        },
        "Ponto": [date(2021, 9, 5), date(2021, 9, 12), date(2021, 9, 19), date(2021, 9, 26)],
    },
    {
        "Cod": 6,
        "Nome": "Lucas Castelani Souza",
        "CPF": "555.666.777-88",
        "Endereço": "Rua 6, 303",
        "Observações": "Nenhuma",
        "Salário": 3000.00,
        "Contatos": [(31955555558, "Celular"), (11944444448, "Telefone fixo")],
        "Oficinas": {
            "SEG - 10:00 ÀS 11:00": "Física",
            "SEX - 09:00 ÀS 10:00": "Química",
        },
        "Ponto": [date(2021, 10, 5), date(2021, 10, 12), date(2021, 10, 19), date(2021, 10, 26)],
    },
]
















def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

# Função para formatar CPF e RG
def formatar_cpf(cpf):
    return f"{cpf:011d}"[:3] + '.' + f"{cpf:011d}"[3:6] + '.' + f"{cpf:011d}"[6:9] + '-' + f"{cpf:011d}"[9:]

def formatar_cep(cep):
    return f"{cep:08d}"[:5] + '-' + f"{cep:08d}"[5:]

def formatar_telefone(telefone):
    telefone = f"{telefone:011d}"
    return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"


def Listar(dados_funcionarios):
    
    # Se o botão "Alterar" ou "Ver" for pressionado, limpe a página e mostre o formulário
    on_click_alterar = st.session_state.get("alterar_funcionario", None)
    on_click_ver = st.session_state.get("ver_funcionario", None)

    if on_click_ver:
        # Limpar a tela e exibir detalhes do funcionário
        st.empty()
        funcionario_selecionado = next(item for item in dados_funcionarios if item["Cod"] == on_click_ver)
        st.markdown(f"<h1 style='font-size: 40px;'>{funcionario_selecionado['Nome']}</h1>", unsafe_allow_html=True)

    
        # Exibindo os detalhes do funcionário
        col1_detalhes, col2_detalhes =st.columns(2)
        col1_detalhes.write(f"**Nome Completo:** {funcionario_selecionado['Nome']}")
        col2_detalhes.write(f"**CPF:** {funcionario_selecionado['CPF']}")

        st.write(f"Endereço: {funcionario_selecionado['Endereço']}")
        st.write(f"Salário: {funcionario_selecionado['Salário']}")
        st.write(f"Observações: {funcionario_selecionado['Observações']}")

        # Contatos
        st.subheader("**Contatos**")
        cols = st.columns(3)
        for idx, (telefone, descricao) in enumerate(funcionario_selecionado['Contatos']):
            formatted_telefone = formatar_telefone(telefone)
            with cols[idx % 3].container(border=True):
                st.markdown(f"**{descricao}:**")
                st.write(formatted_telefone)

        # Oficinas
        st.subheader("**Oficinas**")
        for horario, oficina in funcionario_selecionado['Oficinas'].items():
            st.write(f"- **{horario}**: {oficina}")
        
        # Presenças
        st.subheader("**Pontos**")
        min_date, max_date = min(funcionario_selecionado['Ponto']), max(funcionario_selecionado['Ponto'])

        cols = st.columns(2)
        intervalo_datas = [cols[0].date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")]
        intervalo_datas.append(cols[1].date_input("Data Final", max_date, min_value=intervalo_datas[0], max_value=max_date, format="DD/MM/YYYY"))

        # Contabilizando as presenças no intervalo
        st.write(f"Pontos no intervalo selecionado: {len([i for i in funcionario_selecionado['Ponto'] if intervalo_datas[0] <= i <= intervalo_datas[1]])}")

        with st.expander("Datas de Ponto"):
            for i in funcionario_selecionado['Ponto']:
                if intervalo_datas[0] <= i <= intervalo_datas[1]:
                    st.write(i.strftime('%d/%m/%Y'))  # Exibindo a data no formato desejado

        submit_button = st.button("Voltar")

        if submit_button:
            st.session_state["ver_funcionario"] = None  # Limpar o estado de visualização para voltar à lista
            st.rerun()

    elif on_click_alterar:
        # Limpar a página (realmente limpar)
        st.empty()

        # Obter os dados do funcionário selecionado
        funcionario_selecionado = next(item for item in dados_funcionarios if item["Cod"] == on_click_alterar)

        # Exibir o formulário de alteração
        st.header(f"Alterando dados de: {funcionario_selecionado['Nome']}")
        
        # Criando o formulário para alterar dados do funcionário
        with st.form(key=f"alterar_{funcionario_selecionado['Cod']}"):
            nome = st.text_input("Nome", value=funcionario_selecionado["Nome"])
            cpf = st.text_input("CPF", value=funcionario_selecionado["CPF"])
            endereco = st.text_input("Endereço", value=funcionario_selecionado["Endereço"])
            salario = st.number_input("Salário", value=funcionario_selecionado["Salário"], step=100.0)
            observacoes = st.text_area("Observações", value=funcionario_selecionado["Observações"])

            # Informações atualizadas:
            # nome,cpf,endereco,salario,observacoes

            # Submissão do formulário
            submit_button = st.form_submit_button(label="Salvar Alterações")

            if submit_button:
                # Aqui você pode salvar as alterações em uma estrutura de dados ou banco de dados
                st.success(f"Alterações salvas para {nome}!")
                st.session_state["alterar_funcionario"] = None  # Limpar o estado de alteração para voltar à lista
                sleep(1)
                st.rerun()

    else:
        st.title("Gestão de Funcionários")
        st.markdown("<hr>", unsafe_allow_html=True)
        # Mostrar os dados de cada funcionário
        columns = st.columns([1, 3, 2, 1.5, 1.5, 1, 1.5])
        campos = ["Nº", "Nome", "CPF", "Salário", "Oficinas", "Ver", "Alterar"]

        # Cabeçalho da tabela
        for col, campo_nome in zip(columns, campos):
            col.write(campo_nome)

        # Mostrar a tabela com os dados
        for item in dados_funcionarios:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 1.5, 1.5, 1, 1.5])
            quantidade_oficinas = len(item["Oficinas"])

            col1.write(item["Cod"])
            col2.write(item["Nome"])
            col3.write(item["CPF"])
            col4.write(item["Salário"])
            col5.write(quantidade_oficinas)

            button_space_ver = col6.empty() 
            on_click_ver = button_space_ver.button("Ver", "btmVer" + str(item["Cod"]))
            button_space_alterar = col7.empty() 
            on_click_alterar = button_space_alterar.button("Alterar", "btmAlterar" + str(item["Cod"]))

            # Ação para o botão "Ver"
            if on_click_ver:
                st.session_state["ver_funcionario"] = item["Cod"]
                st.rerun()

            # Ação para o botão "Alterar"
            if on_click_alterar:
                st.session_state["alterar_funcionario"] = item["Cod"]
                st.rerun()  # Reinicia a página para exibir o formulário de alteração
        st.markdown("<hr>", unsafe_allow_html=True)

# Inicialização da variável de estado
if "alterar_funcionario" not in st.session_state:
    st.session_state["alterar_funcionario"] = None
    st.session_state["ver_funcionario"] = None

# Iniciar a execução da função Listar
Listar(dados_funcionarios)



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)