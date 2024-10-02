import streamlit as st
import pandas as pd
import altair as alt

# Carregar os dados
data = pd.read_csv('houses_to_rent_v2.csv')

# Título do Dashboard
st.markdown("<h1 style='text-align: center; '>Dashboard de Imóveis para Aluguel</h1>", unsafe_allow_html=True)

# Subtítulos
st.markdown("<h3 style='text-align: center; color: #34495e;'>Pós-Graduação em Análise de Dados e IA - UFMA</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #34495e;'>Disciplina de Visualização de Dados</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #34495e;'>Francisco José de Cerqueira Antunes Filho</h4>", unsafe_allow_html=True)

# Espaçamento
st.markdown("")  # Adiciona um espaço em branco
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
    x=alt.X('city:N', title='Cidade'),  # Título do eixo X em português
    y=alt.Y('mean(rent amount (R$)):Q', title='Preço Médio de Aluguel (R$)'),  # Título do eixo Y em português
    color=alt.Color('city:N', title='Cidade'),  # Título da legenda de cor em português
    tooltip=[
        alt.Tooltip('city:N', title='Cidade'),  # Tooltip em português
        alt.Tooltip('mean(rent amount (R$)):Q', title='Preço Médio de Aluguel (R$)', format=',.2f')  # Tooltip formatado para 2 casas decimais
    ]
).properties(
    title='Preço Médio de Aluguel por Cidade'  # Título do gráfico em português
)

st.altair_chart(chart1, use_container_width=True)

# Gráfico 2: Quantidade de imóveis por número de quartos
st.subheader('Quantidade de Imóveis por Número de Quartos')

chart2 = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('rooms:O', title='Número de Quartos'),  # Título do eixo X em português
    y=alt.Y('count():Q', title='Quantidade de Imóveis'),  # Título do eixo Y em português
    color=alt.Color('rooms:O', title='Número de Quartos'),  # Título da legenda de cor em português
    tooltip=[
        alt.Tooltip('rooms:O', title='Número de Quartos'),  # Tooltip em português
        alt.Tooltip('count():Q', title='Quantidade de Imóveis')  # Tooltip em português
    ]
).properties(
    title='Quantidade de Imóveis por Número de Quartos'  # Título do gráfico em português
)

st.altair_chart(chart2, use_container_width=True)

# Gráfico 3: Total de despesas mensais por cidade
st.subheader('Total de Despesas Mensais por Cidade')
chart3 = alt.Chart(filtered_data).mark_boxplot().encode(
    x=alt.X('city:N', title='Cidade'),  # Título do eixo X em português
    y=alt.Y('total (R$):Q', title='Total (R$)'),  # Título do eixo Y em português
    color=alt.Color('city:N', title='Cidade'),  # Título da legenda de cor em português
    tooltip=[
        alt.Tooltip('city:N', title='Cidade'),  # Tooltip em português
        alt.Tooltip('total (R$):Q', title='Total (R$)', format=',.2f')  # Tooltip formatado para 2 casas decimais
    ]
).properties(
    title='Despesas Totais Mensais por Cidade'  # Título do gráfico em português
)

st.altair_chart(chart3, use_container_width=True)

# Gráfico 4: Relação entre Área e Preço de Aluguel
st.subheader('Relação entre Área e Preço de Aluguel')

# Gráfico de Dispersão
scatter_plot = alt.Chart(filtered_data).mark_circle(opacity=0.7).encode(
    x=alt.X('area:Q', title='Área (m²)'),  # Título do eixo X em português
    y=alt.Y('rent amount (R$):Q', title='Preço de Aluguel (R$)'),  # Título do eixo Y em português
    color=alt.Color('city:N', title='Cidade'),  # Título da legenda de cor em português
    size=alt.Size('rooms:Q', title='Número de Quartos', scale=alt.Scale(range=[50, 200])),
    tooltip=[
        alt.Tooltip('area:Q', title='Área (m²)'),  # Tooltip em português
        alt.Tooltip('rent amount (R$):Q', title='Preço de Aluguel (R$)', format=',.2f'),  # Tooltip formatado para 2 casas decimais
        alt.Tooltip('rooms:Q', title='Número de Quartos'),  # Tooltip em português
        alt.Tooltip('city:N', title='Cidade')  # Tooltip em português
    ]
).properties(
    title='Relação entre Área e Preço de Aluguel'  # Título do gráfico em português
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

    # Criar um DataFrame para o gráfico
    df_chart = animal_percentages.reset_index()
    df_chart.columns = ['Status', 'Porcentagem']  # Renomear colunas

    # Substituir os status para português
    df_chart['Status'] = df_chart['Status'].replace({
        'acept': 'Aceita Animais',
        'not acept': 'Não Aceita Animais'
    })

    # Criar um gráfico de barras
    bar_chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('Status:N', title='Status'),
        y=alt.Y('Porcentagem:Q', title='Porcentagem (%)'),
        color=alt.Color('Status:N', scale=alt.Scale(domain=['Aceita Animais', 'Não Aceita Animais'], range=['#4caf50', '#f44336'])),
        tooltip=[
            alt.Tooltip('Status:N', title='Status'),
            alt.Tooltip('Porcentagem:Q', title='Porcentagem (%)', format='.2f')  # Formatação para 2 casas decimais
        ]
    ).properties(
        title='Porcentagem de Imóveis que Aceitam Animais',
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
        x=alt.X('city:N', title='Cidade'),  # Título do eixo X em português
        y=alt.Y('property tax (R$):Q', title='Imposto Médio (R$)', axis=alt.Axis(format=',.2f')),  # Formatação para 2 casas decimais
        color=alt.Color('city:N', title='Cidade'),
        tooltip=[
            alt.Tooltip('city:N', title='Cidade'),  # Tooltip em português
            alt.Tooltip('property tax (R$):Q', title='Imposto Médio (R$)', format=',.2f')  # Tooltip formatado para 2 casas decimais
        ]
    ).properties(
        title='Comparação do Imposto Médio por Cidade',  # Título do gráfico em português
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

    

    # Criar um dicionário para substituir os nomes
    replacement_dict = {
        'furnished': 'Mobiliado',
        'not furnished': 'Não Mobiliado'
    }

    # Substituir os nomes das categorias para português
    furniture_counts.index = furniture_counts.index.map(replacement_dict)

    # Criar um DataFrame para o gráfico
    df_furniture = furniture_counts.reset_index()
    df_furniture.columns = ['Mobília', 'Quantidade']  # Renomear colunas

    # Criar um gráfico de barras
    furniture_chart = alt.Chart(df_furniture).mark_bar().encode(
        x=alt.X('Mobília:N', title='Tipo de Mobília'),
        y=alt.Y('Quantidade:Q', title='Quantidade de Imóveis',axis=alt.Axis(format='d')),
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