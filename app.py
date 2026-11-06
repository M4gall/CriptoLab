import math
import streamlit as st

# ------------------------------------------------------------
# CriptoLab | Laboratório didático de criptografia
# Cifra de Hill com letras e números (módulo 36)
# ------------------------------------------------------------

st.set_page_config(
    page_title="CriptoLab | Laboratório de Criptografia",
    page_icon="🔐",
    layout="wide",
)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MODULUS = len(ALPHABET)  # 36


def clean_text(text: str) -> str:
    """Mantém letras A-Z e números 0-9, convertendo letras para maiúsculas."""
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


def text_to_numbers(text: str) -> list[int]:
    """A=0, B=1, ..., Z=25, 0=26, ..., 9=35."""
    return [ALPHABET.index(ch) for ch in text]


def numbers_to_text(numbers: list[int]) -> str:
    """Converte números de 0 a 35 de volta para caracteres."""
    return "".join(ALPHABET[n % MODULUS] for n in numbers)


def mod_inverse(value: int, modulus: int) -> int:
    """Encontra o inverso multiplicativo módulo n."""
    value %= modulus
    for candidate in range(1, modulus):
        if (value * candidate) % modulus == 1:
            return candidate
    raise ValueError(f"{value} não possui inverso módulo {modulus}.")


def matrix_inverse_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    """Calcula a inversa modular de uma matriz 2x2."""
    a, b = matrix[0]
    c, d = matrix[1]
    determinant = (a * d - b * c) % modulus
    gcd_value = math.gcd(determinant, modulus)

    if gcd_value != 1:
        raise ValueError(
            f"A matriz não é inversível módulo {modulus}: "
            f"det(K) ≡ {determinant} e mdc({determinant}, {modulus}) = {gcd_value}. "
            "Escolha outros valores para a matriz."
        )

    det_inv = mod_inverse(determinant, modulus)

    # Inversa = determinante^-1 × adjunta, tudo módulo 36.
    return [
        [(det_inv * d) % modulus, (det_inv * (-b)) % modulus],
        [(det_inv * (-c)) % modulus, (det_inv * a) % modulus],
    ]


def hill_transform(
    text: str,
    matrix: list[list[int]],
    pad_odd_length: bool = True,
) -> tuple[str, str, list[int]]:
    """Aplica K × bloco (mod 36), usando blocos de dois caracteres."""
    prepared = clean_text(text)

    if not prepared:
        raise ValueError("Digite pelo menos uma letra ou um número.")

    if len(prepared) % 2 != 0:
        if not pad_odd_length:
            raise ValueError(
                "O texto cifrado precisa ter uma quantidade par de caracteres."
            )
        prepared += "X"

    values = text_to_numbers(prepared)
    output = []

    for i in range(0, len(values), 2):
        x1, x2 = values[i], values[i + 1]
        y1 = (matrix[0][0] * x1 + matrix[0][1] * x2) % MODULUS
        y2 = (matrix[1][0] * x1 + matrix[1][1] * x2) % MODULUS
        output.extend([y1, y2])

    return numbers_to_text(output), prepared, output


# ------------------------------------------------------------
# Aparência
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp { background: #100D1C; color: #F2EFFF; }
    [data-testid="stHeader"] { background: rgba(16,13,28,.88); }
    [data-testid="stSidebar"] { background: #171226; border-right: 1px solid #36264F; }
    [data-testid="stSidebar"] * { color: #F2EFFF; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp p, .stApp label, .stApp li,
    [data-testid="stMarkdownContainer"] { color: #F2EFFF; }
    .hero {
        padding: 2rem 2.2rem;
        border-radius: 22px;
        background: linear-gradient(115deg, #281B49 0%, #43236B 65%, #241B36 100%);
        border: 1px solid #65468E;
        box-shadow: 0 12px 34px rgba(0,0,0,.22);
        margin-bottom: 1.2rem;
    }
    .hero h1 { color: #F2EFFF; margin-bottom: .3rem; }
    .hero p { color: #E5D5FF; font-size: 1.05rem; margin-bottom: 0; }
    .metric-card {
        background: #241B36;
        border: 1px solid #493365;
        border-radius: 16px;
        padding: 1rem 1.1rem;
    }
    .small-note { color: #C6B5DC; font-size: .9rem; }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: #C6B5DC; }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #9D70D0;
        background: #8050B8;
        color: #FFFFFF;
        font-weight: 600;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: #9C65D5;
        border-color: #D8B8FF;
        color: #FFFFFF;
    }
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background-color: #241B36;
        border-color: #60457E;
        color: #F2EFFF;
    }
    input, textarea { color: #F2EFFF !important; caret-color: #D8B8FF; }
    input::placeholder, textarea::placeholder { color: #A99ABF !important; }
    [data-baseweb="tab-list"] { border-bottom: 1px solid #493365; }
    button[data-baseweb="tab"] { color: #D5C4EA; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #D8B8FF; }
    [data-testid="stCodeBlock"] { border: 1px solid #493365; border-radius: 12px; }
    [data-testid="stAlert"] { border-radius: 12px; }
    a { color: #D8B8FF; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cabeçalho
st.markdown(
    """
    <div class="hero">
      <h1>🔐 CriptoLab</h1>
      <p>Um laboratório interativo para descobrir como a matemática transforma
      mensagens em informação protegida.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Navegação")
    page = st.radio(
        "Escolha uma seção",
        ["Início", "Fundamentos", "Laboratório Hill", "Aplicações", "Desafio"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Projeto acadêmico • Python + Streamlit")
    st.caption("Demonstração didática — não use para proteger dados reais.")

# ------------------------------------------------------------
# Páginas
# ------------------------------------------------------------

if page == "Início":
    st.subheader("Bem-vindo ao laboratório")
    st.write(
        "A criptografia transforma uma mensagem original em uma mensagem cifrada. "
        "Neste projeto, exploramos como matrizes e aritmética modular podem realizar "
        "essa transformação. Nosso alfabeto inclui letras de A a Z e números de 0 a 9."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="metric-card">**Matrizes**<br><span class="small-note">'
            'Transformam blocos de dois caracteres.</span></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="metric-card">**Módulo 36**<br><span class="small-note">'
            'Mantém os resultados entre 0 e 35.</span></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card">**Cifra de Hill**<br><span class="small-note">'
            'Combina álgebra linear e congruências.</span></div>',
            unsafe_allow_html=True,
        )

    st.info(
        "Comece por **Fundamentos** ou vá direto ao **Laboratório Hill** "
        "para criptografar suas próprias mensagens."
    )

elif page == "Fundamentos":
    st.subheader("Os conceitos por trás da criptografia")

    with st.expander("1. O que é criptografia?", expanded=True):
        st.write(
            "É o processo de transformar uma mensagem original (texto claro) "
            "em uma mensagem cifrada, usando um método e uma chave. "
            "A descriptografia tenta recuperar a mensagem original."
        )

    with st.expander("2. Aritmética modular"):
        st.latex(r"a \equiv b \pmod{36}")
        st.write(
            "Dois números são congruentes módulo 36 quando possuem o mesmo resto "
            "na divisão por 36. Usamos A=0, B=1, ..., Z=25 e 0=26, ..., 9=35. "
            "Assim, cada resultado é reduzido ao intervalo de 0 a 35."
        )
        st.latex(r"41 \bmod 36 = 5")

    with st.expander("3. Matrizes inversíveis"):
        st.write(
            "A matriz-chave precisa possuir uma inversa módulo 36 para que "
            "seja possível desfazer a transformação e recuperar a mensagem."
        )
        st.latex(r"K^{-1}K \equiv I \pmod{36}")

    st.warning(
        "A condição para uma matriz 2×2 ser inversível módulo 36 é "
        "mdc(det(K), 36) = 1. Ter determinante diferente de zero, por si só, "
        "não é suficiente na aritmética modular."
    )

    st.markdown("**Exemplo de chave válida:**")
    st.latex(r"K=\begin{bmatrix}5&7\\2&3\end{bmatrix}")
    st.write("Seu determinante é 5·3 − 7·2 = 1. Como mdc(1, 36) = 1, ela é inversível módulo 36.")

elif page == "Laboratório Hill":
    st.subheader("Laboratório: Cifra de Hill")
    st.write(
        "Digite uma mensagem com letras e/ou números e escolha uma matriz-chave 2×2. "
        "O programa converte os caracteres em números, agrupa em pares e aplica "
        "a multiplicação matricial módulo 36."
    )

    st.markdown("**Alfabeto utilizado**")
    st.code("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    st.caption(
        "Mapeamento: A=0, B=1, ..., Z=25 e 0=26, 1=27, ..., 9=35. "
        "Espaços e pontuação são ignorados; letras minúsculas viram maiúsculas."
    )

    left, right = st.columns([1, 1])

    with left:
        st.markdown("**Matriz-chave K**")
        st.caption("A chave padrão abaixo é válida para módulo 36.")
        row1 = st.columns(2)
        a = row1[0].number_input("k₁₁", value=5, step=1)
        b = row1[1].number_input("k₁₂", value=7, step=1)
        row2 = st.columns(2)
        c = row2[0].number_input("k₂₁", value=2, step=1)
        d = row2[1].number_input("k₂₂", value=3, step=1)

    key = [[int(a), int(b)], [int(c), int(d)]]

    with right:
        st.markdown("**Como funciona**")
        st.write("1. Cada caractere recebe um número de 0 a 35.")
        st.write("2. Os números são agrupados em pares.")
        st.write("3. A matriz-chave transforma cada par.")
        st.write("4. Reduzimos os resultados módulo 36.")
        st.latex(
            r"\begin{bmatrix}y_1\\y_2\end{bmatrix}"
            r"\equiv K\begin{bmatrix}x_1\\x_2\end{bmatrix}\pmod{36}"
        )

    try:
        inverse = matrix_inverse_mod(key, MODULUS)
        determinant = (key[0][0] * key[1][1] - key[0][1] * key[1][0]) % MODULUS
        st.success(
            f"Esta matriz é válida! det(K) ≡ {determinant} (mod 36) "
            f"e mdc({determinant}, 36) = 1."
        )
    except ValueError as error:
        inverse = None
        st.error(str(error))

    encrypt_tab, decrypt_tab = st.tabs(["🔒 Criptografar", "🔓 Descriptografar"])

    with encrypt_tab:
        message = st.text_input(
            "Digite sua mensagem",
            value="CRIPTO2026",
            max_chars=100,
            key="message_to_encrypt",
        )
        if st.button("Criptografar mensagem", use_container_width=True, key="encrypt"):
            if inverse is None:
                st.error("Corrija a matriz-chave antes de criptografar.")
            else:
                try:
                    cipher, prepared, encrypted_numbers = hill_transform(message, key)
                    st.success("Mensagem criptografada!")
                    st.markdown("**Mensagem preparada (após remover espaços e pontuação)**")
                    st.code(prepared)
                    st.markdown("**Texto cifrado**")
                    st.code(cipher)
                    st.caption(
                        "Se a mensagem preparada tinha quantidade ímpar de caracteres, "
                        "foi acrescentado X ao final para completar o último par."
                    )
                    with st.expander("Ver os números gerados"):
                        st.write("Mensagem preparada:", text_to_numbers(prepared))
                        st.write("Resultado numérico:", encrypted_numbers)
                except ValueError as error:
                    st.error(str(error))

    with decrypt_tab:
        cipher_input = st.text_input(
            "Digite ou cole a mensagem cifrada",
            max_chars=100,
            key="cipher_to_decrypt",
        )
        if st.button("Descriptografar mensagem", use_container_width=True, key="decrypt"):
            if inverse is None:
                st.error("Corrija a matriz-chave antes de descriptografar.")
            else:
                try:
                    decrypted, prepared_cipher, decrypted_numbers = hill_transform(
                        cipher_input, inverse, pad_odd_length=False
                    )
                    st.success("Mensagem descriptografada!")
                    st.markdown("**Texto recuperado**")
                    st.code(decrypted)
                    st.caption(
                        "Se a mensagem original tinha quantidade ímpar de caracteres, "
                        "o X acrescentado no preenchimento aparecerá no final. "
                        "Remova esse X se ele tiver sido usado apenas como preenchimento."
                    )
                    with st.expander("Ver os números recuperados"):
                        st.write("Texto cifrado preparado:", prepared_cipher)
                        st.write("Resultado numérico:", decrypted_numbers)
                except ValueError as error:
                    st.error(str(error))

elif page == "Aplicações":
    st.subheader("Onde a criptografia aparece?")

    st.markdown("#### Proteção de senhas")
    st.write(
        "Serviços não devem guardar senhas em texto puro. Em geral, utilizam "
        "funções de hash próprias para armazenamento de senhas, com salt e "
        "parâmetros de custo. Isso é diferente da Cifra de Hill."
    )

    st.markdown("#### Transações bancárias")
    st.write(
        "A criptografia moderna ajuda a proteger a comunicação entre aplicativos, "
        "servidores e instituições financeiras, contribuindo para a confidencialidade "
        "e a integridade das informações."
    )

    st.markdown("#### Mensagens em aplicativos")
    st.write(
        "Protocolos modernos podem usar criptografia ponta a ponta para que o "
        "conteúdo das mensagens seja acessível apenas aos participantes autorizados."
    )

    st.info(
        "A Cifra de Hill é usada aqui para fins educacionais. Sistemas reais "
        "utilizam algoritmos e protocolos modernos, como AES e construções "
        "criptográficas baseadas em curvas elípticas."
    )

elif page == "Desafio":
    st.subheader("Desafio rápido")
    st.write(
        "Usando a convenção A=0, B=1, ..., Z=25 e 0=26, ..., 9=35, "
        "qual é o resultado de 41 módulo 36?"
    )
    answer = st.radio("Escolha uma resposta:", ["3", "4", "5", "6"], horizontal=True)

    if st.button("Conferir resposta"):
        if answer == "5":
            st.success("Isso mesmo! 41 dividido por 36 deixa resto 5.")
        else:
            st.error("Não é essa. Pense no resto da divisão de 41 por 36.")

    st.divider()
    st.markdown(
        "**Pergunta para discussão:** por que a matriz-chave precisa ser "
        "inversível módulo 36?"
    )
    st.caption(
        "Dica: pense em como recuperar o texto original depois da criptografia."
    )

st.divider()
st.caption(
    "CriptoLab • Projeto acadêmico demonstrativo. A Cifra de Hill não é adequada "
    "para proteger senhas, dados bancários ou comunicações reais."
)
