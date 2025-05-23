import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

st.set_page_config(page_title="Análisis de Datos", layout="wide")
st.title("Aplicación de Análisis de Datos 📊")

# Subida de archivo
st.sidebar.header("Sube tu archivo de datos")
file = st.sidebar.file_uploader("Elige un archivo", type=["txt", "csv", "xlsx"])

# Función para leer archivo
@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.txt'):
        return pd.read_csv(file, delimiter="\t")
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        return None

if file:
    df = load_data(file)
    st.write("### Vista previa de los datos:")
    st.dataframe(df.head())

    st.sidebar.subheader("Selecciona columnas")
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    selected_x = st.sidebar.selectbox("Eje X", numeric_columns)
    selected_y = st.sidebar.selectbox("Eje Y", numeric_columns)

    plot_type = st.sidebar.radio("Tipo de gráfico", ["Dispersión", "Boxplot", "Barras", "Distribución", "Ajuste"])

    fig, ax = plt.subplots()
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'serif'

    if plot_type == "Dispersión":
        sns.scatterplot(data=df, x=selected_x, y=selected_y, ax=ax)
        ax.set_title(r"Gr\'afico de Dispersi\'on")

    elif plot_type == "Boxplot":
        sns.boxplot(data=df[[selected_x, selected_y]], ax=ax)
        ax.set_title(r"Boxplot")

    elif plot_type == "Barras":
        mean_vals = df.groupby(selected_x)[selected_y].mean().reset_index()
        sns.barplot(data=mean_vals, x=selected_x, y=selected_y, ax=ax)
        ax.set_title(r"Gr\'afico de Barras")

    elif plot_type == "Distribución":
        sns.histplot(df[selected_y], kde=True, ax=ax)
        ax.set_title(r"Distribuci\'on de " + selected_y)

    elif plot_type == "Ajuste":
        sns.regplot(data=df, x=selected_x, y=selected_y, ax=ax)
        ax.set_title(r"Ajuste Lineal")

    ax.set_xlabel(r"$" + selected_x + r"$")
    ax.set_ylabel(r"$" + selected_y + r"$")
    st.pyplot(fig)

    st.subheader("Estadísticas Descriptivas")
    st.write(df.describe())
