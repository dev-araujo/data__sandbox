import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finanças", page_icon=":moneybag:", layout="wide")


st.markdown(
    """
# Finanças :moneybag:

Aplicação de finanças permite que você visualize e analise seus dados financeiros de forma interativa.
"""
)

file_upload = st.file_uploader("Faça upload da planilha", type=["csv"])

if file_upload:
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce").dt.date

    # exibir os dados brutos
    expanderBrutesData = st.expander("Dados - Brutos")
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %f")}
    expanderBrutesData.dataframe(df, hide_index=True, column_config=columns_fmt)

    # visão da instituição
    expanderInstitutionsData = st.expander("Dados - Instituição")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")


    tab_data, tab_history, tb_share = expanderInstitutionsData.tabs(["Dados", "Histórico", "Distribuição"])
    with tab_data:
        st.markdown("### Dados por Instituição")
        st.dataframe(df_instituicao)
    with tab_history:
        st.markdown("### Histórico por Instituição")
        st.line_chart(df_instituicao)
    with tb_share:
        st.markdown("### Distribuição por Instituição")
        date = st.date_input("Selecione uma data", min_value=df_instituicao.index.min(), max_value=df_instituicao.index.max())


        if date not in df_instituicao.index:
            st.warning("Data não encontrada nos dados.")
        else:
            st.bar_chart(df_instituicao.loc[date])

        

  
