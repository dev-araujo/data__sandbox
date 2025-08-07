import pandas as pd
import streamlit as st




def calc_financial_metrics(df:pd.DataFrame):
    
    df_data = df.groupby(by="Data")[["Valor"]].sum()
    df_data["lag_1"] = df_data["Valor"].shift(1)
    df_data["Diferença mensal Abs."] = df_data["Valor"] - df_data["lag_1"]
    df_data["Média 6m Diferença mensal Abs."] = df_data['Diferença mensal Abs.'].rolling(6).mean()
    df_data["Média 12m Diferença mensal Abs."] = df_data['Diferença mensal Abs.'].rolling(12).mean()
    df_data["Média 24m Diferença mensal Abs."] = df_data['Diferença mensal Abs.'].rolling(54).mean()
    df_data["Diferença mensal Rel."] = df_data["Valor"] / df_data["lag_1"] - 1
    df_data["Evolução 6m Total"] = df_data['Valor'].rolling(6).apply(lambda x:   x.iloc[-1] - x.iloc[0])
    df_data["Evolução 12m Total"] = df_data['Valor'].rolling(12).apply(lambda x: x.iloc[-1] - x.iloc[0])
    df_data["Evolução 24m Total"] = df_data['Valor'].rolling(54).apply(lambda x: x.iloc[-1] - x.iloc[0])
    df_data["Evolução 6m Rel."] = df_data['Valor'].rolling(6).apply(lambda x:   x.iloc[-1] / x.iloc[0] - 1)
    df_data["Evolução 12m Rel."] = df_data['Valor'].rolling(12).apply(lambda x: x.iloc[-1] / x.iloc[0] - 1)
    df_data["Evolução 24m Rel."] = df_data['Valor'].rolling(54).apply(lambda x: x.iloc[-1] / x.iloc[0] - 1)

    df_data = df_data.drop("lag_1", axis=1)

    return df_data


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


    # Estatísticas Gerais
    expanderGeneralStats = st.expander("Estatísticas Gerais")
    df_stats = calc_financial_metrics(df)

    conlumns_config = {
       "Valor":st.column_config.NumberColumn("Valor.", format="R$ %f"),
       "Diferença mensal Abs.":st.column_config.NumberColumn("Diferença mensal Abs.", format="R$ %f"),
       "Média 6m Diferença mensal Abs." :st.column_config.NumberColumn("Média 6m Diferença mensal Abs.", format="R$ %f"),
       "Média 12m Diferença mensal Abs.":st.column_config.NumberColumn("Média 12m Diferença mensal Abs.", format="R$ %f"),
       "Média 24m Diferença mensal Abs.":st.column_config.NumberColumn("Média 24m Diferença mensal Abs.", format="R$ %f"),
       "Evolução 6m Total":st.column_config.NumberColumn("Evolução 6m Total", format="R$ %f"),
       "Evolução 12m Total":st.column_config.NumberColumn("Evolução 12m Total", format="R$ %f"),
       "Evolução 24m Total":st.column_config.NumberColumn("Evolução 24m Total", format="R$ %f"),
       "Diferença mensal Rel.":st.column_config.NumberColumn("Diferença mensal Rel.", format="percent"),
       "Evolução 6m Rel.":st.column_config.NumberColumn("Evolução 6m Rel.", format="percent"),
       "Evolução 12m Rel.":st.column_config.NumberColumn("Evolução 12m Rel.", format="percent"),
       "Evolução 24m Rel.":st.column_config.NumberColumn("Evolução 24m Rel.", format="percent")

    }

    expanderGeneralStats.dataframe(df_stats, column_config=conlumns_config)
    

  
