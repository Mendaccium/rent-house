import streamlit as st
import pandas as pd
import altair as alt

# Carregar os dados
data = pd.read_csv('houses_to_rent_v2.csv')

# Título do aplicativo
st.title('Dashboard de Imóveis para Aluguel')

# Filtro: Selecionar cidade
st.sidebar.header('Filtros')
selected_city = st.sidebar.selectbox('Selecione a Cidade', ['Todas'] + data['city'].unique().tolist())

# Filtrar dados com base na cidade selecionada
if selected_city != 'Todas':
    filtered_data = data[data['city'] == selected_city]
else:
    filtered_data = data

# Apresentar informações gerais
st.subheader('Apanhado Geral das Informações')
average_rent = filtered_data['rent amount (R$)'].mean()
average_total_cost = filtered_data['total (R$)'].mean()
avg_rent_per_m2 = average_rent / (filtered_data['area'].mean() if filtered_data['area'].mean() > 0 else 1)
percentage_with_pets = (filtered_data['animal'].value_counts(normalize=True).get('acept', 0) * 100)

st.write(f"- Custo Total Médio: R$ {average_total_cost:.2f}")
st.write(f"- Média de Aluguel por M²: R$ {avg_rent_per_m2:.2f}")
st.write(f"- Porcentagem de Imóveis que Aceitam Animais: {percentage_with_pets:.2f}%")
st.write(f"- Quantidade de Imóveis: {len(filtered_data)}")

# Exibir a tabela de dados filtrados
st.subheader('Tabela de Dados')
st.dataframe(filtered_data)

# Gráfico 1: Distribuição de preços de aluguel por cidade (ou apenas a cidade selecionada)
st.subheader('Distribuição de Aluguel por Cidade')
chart1 = alt.Chart(filtered_data).mark_bar().encode(
    x='city',
    y='mean(rent amount (R$))',
    color='city',
    tooltip=['city', 'mean(rent amount (R$))']
).properties(
    title='Preço Médio de Aluguel por Cidade'
)

st.altair_chart(chart1, use_container_width=True)

# Gráfico 2: Quantidade de imóveis por número de quartos
st.subheader('Quantidade de Imóveis por Número de Quartos')
chart2 = alt.Chart(filtered_data).mark_bar().encode(
    x='rooms:O',
    y='count():Q',
    color='rooms:O',
    tooltip=['rooms:O', 'count():Q']
).properties(
    title='Número de Imóveis por Quarto'
)

st.altair_chart(chart2, use_container_width=True)

# Gráfico 3: Total de despesas mensais por cidade
st.subheader('Total de Despesas Mensais por Cidade')
chart3 = alt.Chart(filtered_data).mark_boxplot().encode(
    x='city',
    y='total (R$):Q',
    color='city',
    tooltip=['city', 'total (R$)']
).properties(
    title='Despesas Totais Mensais por Cidade'
)

st.altair_chart(chart3, use_container_width=True)

# Gráfico 4: Relação entre Área e Preço de Aluguel

st.subheader('Relação entre Área e Preço de Aluguel')

# Gráfico de Dispersão
scatter_plot = alt.Chart(filtered_data).mark_circle(opacity=0.7).encode(
    x=alt.X('area:Q', title='Área (m²)'),
    y=alt.Y('rent amount (R$):Q', title='Preço de Aluguel (R$)'),
    color='city:N',
    size=alt.Size('rooms:Q', title='Número de Quartos', scale=alt.Scale(range=[50, 200])),
    tooltip=['area', 'rent amount (R$)', 'rooms', 'city']
).properties(
    title='Gráfico de Dispersão: Área vs. Preço de Aluguel',
    width=600,
    height=400
).interactive()


st.altair_chart(scatter_plot, use_container_width=True)

# Gráfico de Porcentagem de Aluguéis que Aceitam e Não Aceitam Animais
st.subheader('Imóveis que Aceitam Animais')

# Verificar se há dados suficientes
if not filtered_data.empty:
    # Contar a quantidade de imóveis que aceitam e não aceitam animais
    animal_counts = filtered_data['animal'].value_counts()

    # Garantir que existam entradas para 'acept' e 'not acept'
    animal_counts = animal_counts.reindex(['acept', 'not acept'], fill_value=0)

    # Calcular porcentagens
    total_count = animal_counts.sum()
    animal_percentages = (animal_counts / total_count) * 100

    # Exibir as porcentagens para depuração
    

    # Criar um DataFrame para o gráfico
    df_chart = animal_percentages.reset_index()
    df_chart.columns = ['Status', 'Porcentagem']  # Renomear colunas

    # Criar um gráfico de barras
    bar_chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('Status:N', title='Status'),
        y=alt.Y('Porcentagem:Q', title='Porcentagem (%)'),
        color=alt.Color('Status:N', scale=alt.Scale(domain=['acept', 'not acept'], range=['#4caf50', '#f44336'])),
        tooltip=['Status:N', 'Porcentagem:Q']
    ).properties(
        title='Porcentagem de Imóveis que Aceitam Animais x Imóveis que Não Aceitam Animais',
        width=600,
        height=400
    ).configure_title(
        fontSize=20,
        anchor='start'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Exibir o gráfico
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.write("Nenhum dado disponível para a cidade selecionada.")

# Gráfico de Comparação do Imposto Médio por Cidade
st.subheader('Comparação do Imposto Médio por Cidade')

# Verificar se há dados suficientes
if not filtered_data.empty:
    # Calcular a média dos impostos por cidade
    avg_tax_comparison = filtered_data.groupby('city')['property tax (R$)'].mean().reset_index()


    # Criar um gráfico de barras
    avg_tax_chart = alt.Chart(avg_tax_comparison).mark_bar().encode(
        x=alt.X('city:N', title='Cidade'),
        y=alt.Y('property tax (R$):Q', title='Imposto Médio (R$)'),
        color='city:N',
        tooltip=['city:N', 'property tax (R$):Q']
    ).properties(
        title='Comparação do Imposto Médio por Cidade',
        width=600,
        height=400
    ).configure_title(
        fontSize=20,
        anchor='start'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Exibir o gráfico
    st.altair_chart(avg_tax_chart, use_container_width=True)
else:
    st.write("Nenhum dado disponível para a cidade selecionada.")

# Gráfico de Distribuição de Mobília
st.subheader('Distribuição de Mobília dos Imóveis')

# Verificar se há dados suficientes
if not filtered_data.empty:
    # Contar a quantidade de imóveis mobiliados e não mobiliados
    furniture_counts = filtered_data['furniture'].value_counts()


    # Criar um DataFrame para o gráfico
    df_furniture = furniture_counts.reset_index()
    df_furniture.columns = ['Mobília', 'Quantidade']  # Renomear colunas

    # Criar um gráfico de barras
    furniture_chart = alt.Chart(df_furniture).mark_bar().encode(
        x=alt.X('Mobília:N', title='Tipo de Mobília'),
        y=alt.Y('Quantidade:Q', title='Quantidade de Imóveis'),
        color='Mobília:N',
        tooltip=['Mobília:N', 'Quantidade:Q']
    ).properties(
        title='Distribuição de Mobília dos Imóveis',
        width=600,
        height=400
    ).configure_title(
        fontSize=20,
        anchor='start'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Exibir o gráfico
    st.altair_chart(furniture_chart, use_container_width=True)
else:
    st.write("Nenhum dado disponível para a cidade selecionada.")