"""Interface web do VisãoTec (Streamlit). Rodar com: streamlit run app.py"""
import streamlit as st

from visaotec import receita, lentes  # noqa: F401  (vendas, previsao, db entram depois)

st.set_page_config(page_title="VisãoTec", layout="wide")
st.title("VisãoTec")
st.caption("Assistente técnico para óticas")

aba_receita, aba_lente, aba_vendas = st.tabs(
    ["Conferência de receita", "Recomendação de lente", "Painel de vendas"]
)


def campos_olho(rotulo: str, chave: str) -> receita.Olho:
    st.subheader(rotulo)
    c1, c2, c3, c4 = st.columns(4)
    esf = c1.number_input("Esférico", step=0.25, format="%.2f", key=f"{chave}_esf")
    cil = c2.number_input("Cilíndrico", step=0.25, format="%.2f", key=f"{chave}_cil")
    eixo = c3.number_input("Eixo", min_value=0, max_value=180, step=1, key=f"{chave}_eixo")
    add = c4.number_input("Adição", min_value=0.0, step=0.25, format="%.2f", key=f"{chave}_add")
    return receita.Olho(esf, cil, int(eixo), add)


with aba_receita:
    od = campos_olho("Olho direito (OD)", "od")
    oe = campos_olho("Olho esquerdo (OE)", "oe")
    if st.button("Conferir receita"):
        try:
            # TODO: mostrar validação, transposição, grau de perto e EE de cada olho,
            # com a fórmula usada (st.latex) e a conta explicada
            st.write(receita.equivalente_esferico(od), receita.equivalente_esferico(oe))
        except NotImplementedError:
            st.info("Cálculos da receita ainda não implementados.")

with aba_lente:
    # TODO: maior grau → índice; filtro de armação → interseção; contagem e 3 mais baratas
    st.info("Em construção.")

with aba_vendas:
    # TODO: ranking, faturamento mensal, previsão (gráficos com st.pyplot)
    st.info("Em construção.")
