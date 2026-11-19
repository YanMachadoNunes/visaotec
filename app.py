"""Interface web do VisãoTec (Streamlit). Rodar com: streamlit run app.py

Cada bloco mostra o resultado assim que a função dele estiver pronta. Enquanto
ela tiver só o `raise NotImplementedError`, aparece um aviso no lugar.
"""
from contextlib import closing, contextmanager

import pandas as pd
import streamlit as st

from visaotec import db, graficos, lentes, previsao, receita, vendas

st.set_page_config(page_title="VisãoTec", layout="wide")
st.title("VisãoTec")
st.caption("Assistente técnico para óticas")

aba_receita, aba_lente, aba_vendas = st.tabs(
    ["Conferência de receita", "Recomendação de lente", "Painel de vendas"]
)


@contextmanager
def quando_pronto(funcao: str):
    """Troca a falta de implementação por um aviso, sem derrubar a página."""
    try:
        yield
    except NotImplementedError:
        st.info(f"Falta implementar `{funcao}`.")


def grau(valor: float) -> str:
    """Formata um grau com sinal e vírgula, como numa receita."""
    return f"{valor + 0.0:+.2f}".replace(".", ",")


def grau_latex(valor: float) -> str:
    return grau(valor).replace(",", "{,}")


def reais(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def campos_olho(rotulo: str, chave: str) -> receita.Olho:
    st.subheader(rotulo)
    c1, c2, c3, c4 = st.columns(4)
    esf = c1.number_input("Esférico", step=0.25, format="%.2f", key=f"{chave}_esf")
    cil = c2.number_input("Cilíndrico", step=0.25, format="%.2f", key=f"{chave}_cil")
    eixo = c3.number_input("Eixo", min_value=0, max_value=180, step=1, key=f"{chave}_eixo")
    add = c4.number_input("Adição", min_value=0.0, step=0.25, format="%.2f", key=f"{chave}_add")
    return receita.Olho(esf, cil, int(eixo), add)


def mostrar_validacao(od: receita.Olho, oe: receita.Olho) -> None:
    with quando_pronto("validar"):
        resultado = receita.validar(od, oe)
        for erro in resultado["erros"]:
            st.error(erro)
        for alerta in resultado["alertas"]:
            st.warning(alerta)
        if not resultado["erros"] and not resultado["alertas"]:
            st.success("Nenhum erro ou alerta nesta receita.")


def mostrar_conferencia(olho: receita.Olho) -> None:
    st.markdown("**Transposição de cilindro**")
    if olho.cilindro == 0:
        st.caption("Sem cilindro, não há o que transpor.")
    else:
        with quando_pronto("transpor_cilindro"):
            nova = receita.transpor_cilindro(olho)
            st.latex(
                rf"E' = E + C = ({grau_latex(olho.esferico)}) + ({grau_latex(olho.cilindro)})"
                rf" = {grau_latex(nova.esferico)}"
            )
            st.latex(rf"C' = -C = {grau_latex(nova.cilindro)}")
            st.latex(rf"\theta' = {olho.eixo}^\circ \pm 90^\circ = {nova.eixo}^\circ")

    st.markdown("**Formato para o laboratório (cilindro negativo)**")
    with quando_pronto("para_cilindro_negativo"):
        lab = receita.para_cilindro_negativo(olho)
        st.write(f"{grau(lab.esferico)} DE  {grau(lab.cilindro)} DC  eixo {lab.eixo}°")

    st.markdown("**Grau de perto**")
    if olho.adicao == 0:
        st.caption("Sem adição, não há grau de perto.")
    else:
        with quando_pronto("grau_perto"):
            perto = receita.grau_perto(olho)
            st.latex(
                rf"E_{{perto}} = E_{{longe}} + A = ({grau_latex(olho.esferico)})"
                rf" + ({grau_latex(olho.adicao)}) = {grau_latex(perto.esferico)}"
            )

    st.markdown("**Equivalente esférico**")
    with quando_pronto("equivalente_esferico"):
        ee = receita.equivalente_esferico(olho)
        st.latex(
            rf"EE = E + \frac{{C}}{{2}} = ({grau_latex(olho.esferico)})"
            rf" + \frac{{{grau_latex(olho.cilindro)}}}{{2}} = {grau_latex(ee)}"
        )


with aba_receita:
    od = campos_olho("Olho direito (OD)", "od")
    oe = campos_olho("Olho esquerdo (OE)", "oe")
    if st.button("Conferir receita", type="primary"):
        st.session_state["conferida"] = True
    if st.session_state.get("conferida"):
        st.divider()
        mostrar_validacao(od, oe)
        coluna_od, coluna_oe = st.columns(2, gap="large")
        with coluna_od:
            st.subheader("Resultado OD")
            mostrar_conferencia(od)
        with coluna_oe:
            st.subheader("Resultado OE")
            mostrar_conferencia(oe)

with aba_lente:
    grau_maximo = lentes.maior_grau(od, oe)
    st.caption("Usa a receita preenchida na primeira aba.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Maior grau da receita", f"{grau_maximo:.2f}".replace(".", ",") + " D")
    with c2, quando_pronto("escolher_indice"):
        st.metric("Índice sugerido", f"{lentes.escolher_indice(od, oe):.2f}")
    with c3, quando_pronto("contar_orcamentos"):
        st.metric("Orçamentos possíveis", lentes.contar_orcamentos())

    tipo_armacao = st.selectbox("Tipo de armação", list(lentes.LENTES_POR_ARMACAO))
    opcoes = None
    with quando_pronto("opcoes_compativeis"):
        opcoes = lentes.opcoes_compativeis(od, oe, tipo_armacao)
        st.latex(r"\text{Opções} = L_{\text{armação}} \cap L_{\text{receita}}")
        if opcoes:
            st.write("Índices compatíveis: " + ", ".join(f"{i:.2f}" for i in sorted(opcoes)))
        else:
            st.warning("Nenhuma lente atende a esta armação e a esta receita.")

    if db.banco_pronto():
        with closing(db.conectar()) as conn:
            armacoes = db.armacoes_por_montagem(conn, tipo_armacao)
        st.markdown("**Armações deste tipo no catálogo**")
        st.dataframe(
            pd.DataFrame({"Armação": [a["nome"] for a in armacoes],
                          "Preço": [reais(a["preco"]) for a in armacoes]}),
            hide_index=True,
        )

    if opcoes:
        st.markdown("**Três opções mais baratas**")
        with quando_pronto("tres_mais_baratas"):
            baratas = lentes.tres_mais_baratas(od, oe, tipo_armacao)
            st.dataframe(
                pd.DataFrame(
                    [(f"{o['indice']:.2f}", o["tipo"], o["tratamento"], reais(o["preco"]))
                     for o in baratas],
                    columns=["Índice", "Tipo", "Tratamento", "Preço"],
                ),
                hide_index=True,
            )

with aba_vendas:
    if not db.banco_pronto():
        st.info("Gere os dados com `python scripts/gerar_dados.py` e recarregue a página.")
    else:
        with closing(db.conectar()) as conn:
            df_vendas = vendas.carregar_vendas(conn)

        st.subheader("Mais vendidos")
        nome_categoria = st.radio("Categoria", ["Armações", "Lentes"], horizontal=True)
        categoria = "armacao" if nome_categoria == "Armações" else "lente"
        with quando_pronto("ranking_produtos"):
            ranking = vendas.ranking_produtos(df_vendas, categoria)
            st.pyplot(graficos.grafico_ranking(ranking))

        mensal = None
        st.subheader("Faturamento por mês")
        with quando_pronto("faturamento_mensal"):
            mensal = vendas.faturamento_mensal(df_vendas)
            st.pyplot(graficos.grafico_faturamento(mensal))
            with st.expander("Ver tabela"):
                st.dataframe(mensal, hide_index=True)

        st.subheader("Previsão de demanda")
        if mensal is None:
            st.info("A previsão usa o resultado de `faturamento_mensal`.")
        else:
            alvo = st.radio("Prever", ["Itens vendidos", "Faturamento"], horizontal=True)
            coluna = "itens" if alvo == "Itens vendidos" else "faturamento"
            formatar = (lambda v: f"{v:.1f} itens".replace(".", ",")) if coluna == "itens" else reais

            with quando_pronto("treinar, prever e avaliar"):
                treino = previsao.treinar(mensal, coluna)
                proximos = previsao.prever(treino)
                teste = previsao.avaliar(mensal, coluna)

                st.pyplot(graficos.grafico_previsao(mensal, proximos, coluna))
                st.latex(rf"y = {treino['a']:.2f}\,x + {treino['b']:.2f}".replace(".", "{,}"))
                st.caption("Regressão linear: x é o número do mês, começando em 0 no primeiro mês.")

                c1, c2, c3 = st.columns(3)
                c1.metric("Crescimento por mês", formatar(treino["a"]))
                c2.metric("R² da reta", f"{treino['r2']:.2f}".replace(".", ","))
                c3.metric(
                    "Erro nos 3 meses de teste",
                    f"{teste['erro_percentual']:.1f}%".replace(".", ","),
                    help="O modelo treina sem os 3 últimos meses e tenta acertá-los.",
                )
                st.dataframe(
                    pd.DataFrame({
                        "Mês": proximos["mes"],
                        "Previsão": [formatar(v) for v in proximos["previsto"]],
                    }),
                    hide_index=True,
                )
