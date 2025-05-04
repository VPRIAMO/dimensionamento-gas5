
import streamlit as st
import math

# Funções auxiliares para cálculos de velocidade e diâmetro

def calcular_velocidade(vazao_nm3_dia, diametro_m):
    # Conversão da vazão para m³/s
    vazao_m3_s = vazao_nm3_dia / (24 * 3600)
    area = math.pi * (diametro_m/2)**2
    velocidade = vazao_m3_s / area
    return velocidade

def calcular_diametro(vazao_nm3_dia, velocidade_m_s):
    vazao_m3_s = vazao_nm3_dia / (24 * 3600)
    area = vazao_m3_s / velocidade_m_s
    diametro = (4 * area / math.pi)**0.5
    return diametro

# Interface Streamlit
st.title("App de Dimensionamento de Linhas de Produção de Gás")
st.subheader("Baseado em critérios da ANP e API RP 14E")

# Entradas do usuário
vazao_nm3_dia = st.number_input("Vazão (Nm³/dia)", value=10000)
criterio = st.selectbox("Critério de dimensionamento:", ["Verificar velocidade", "Determinar diâmetro"])

if criterio == "Verificar velocidade":
    diametro_pol = st.number_input("Diâmetro da linha (pol)", value=4.0)
    diametro_m = diametro_pol * 0.0254
    velocidade = calcular_velocidade(vazao_nm3_dia, diametro_m)
    st.write(f"Velocidade do escoamento: **{velocidade:.2f} m/s**")

    # Comparação com limites típicos API
    if velocidade < 5:
        st.success("Velocidade adequada (abaixo do limite erosional para gás úmido)")
    elif velocidade < 10:
        st.warning("Velocidade moderada – atenção ao regime de escoamento")
    else:
        st.error("Velocidade excessiva – risco de erosão!")

elif criterio == "Determinar diâmetro":
    velocidade_limite = st.number_input("Velocidade desejada (m/s)", value=10.0)
    diametro_m = calcular_diametro(vazao_nm3_dia, velocidade_limite)
    diametro_pol = diametro_m / 0.0254
    st.write(f"Diâmetro necessário: **{diametro_pol:.2f} polegadas**")
    
    # Sugestão de diâmetro comercial
    diametros_padrao = [2, 3, 4, 6, 8, 10, 12, 16, 20, 24]
    sugerido = min(d for d in diametros_padrao if d >= diametro_pol)
    st.write(f"Sugerido: **{sugerido}'' (tubo padrão API)**")
