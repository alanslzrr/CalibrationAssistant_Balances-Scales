import streamlit as st
from ScalesBalances import cargar_json, buscar_en_sample_cals, convertir_a_gramos, identificar_id_en_certificado_balance, extraer_cmc_fijo_proporcional, calcular_incertidumbre
from htmlTemplates import CSS_STYLES, LOGO_TITLE_HTML, get_image_base64

# Obtener las imágenes en base64
background_base64 = get_image_base64("background.png")

st.markdown(CSS_STYLES, unsafe_allow_html=True)
st.markdown(LOGO_TITLE_HTML, unsafe_allow_html=True)  # Se mantiene esta línea



# Inicializar el estado de la sesión si es necesario
if 'opcion' not in st.session_state:
    st.session_state.opcion = 'Ingresar número de certificado'
if 'numero_certificado' not in st.session_state:
    st.session_state.numero_certificado = ''

# Cargar datos
sample_cals_data = cargar_json("SampleCals.json")
certificado_balance_data = cargar_json("CertificadoBalance.json")

# Título de la aplicación
st.title('Asistente de Calibración')

# Menú de navegación
opcion = st.sidebar.radio('Seleccione una opción:', ['Ingresar número de certificado', 'Buscar certificado por modelo', 'Salir'], index=0 if 'opcion' not in st.session_state else ['Ingresar número de certificado', 'Buscar certificado por modelo', 'Salir'].index(st.session_state.opcion))

if opcion == 'Ingresar número de certificado':
    st.header('Búsqueda por Certificado')
    certificado_objetivo = st.text_input("Ingrese el número del certificado objetivo:", value=st.session_state.numero_certificado if 'numero_certificado' in st.session_state else '')
    
    if certificado_objetivo:
        certificados_filtrados = [cert for cert in sample_cals_data if cert['CertNo'] == certificado_objetivo]
        if certificados_filtrados:
            grupo_seleccionado = st.selectbox('Grupo Objetivo:', ['Seleccionar grupo'] + sorted({g['Group'] for cert in certificados_filtrados for g in cert['Datasheet']}))
            
            if grupo_seleccionado != 'Seleccionar grupo':
                nominal_seleccionado = st.selectbox('Valor Nominal Objetivo:', ['Seleccionar valor nominal'] + sorted({m['Nominal'] for cert in certificados_filtrados for g in cert['Datasheet'] if g['Group'] == grupo_seleccionado for m in g['Measurements']}, key=float))
                
                if nominal_seleccionado != 'Seleccionar valor nominal':
                    unidad_seleccionada = st.selectbox('Unidad Objetivo:', ['Seleccionar unidad'] + sorted({m['Units'] for cert in certificados_filtrados for g in cert['Datasheet'] if g['Group'] == grupo_seleccionado for m in g['Measurements'] if m['Nominal'] == nominal_seleccionado}))
                    
                    if unidad_seleccionada != 'Seleccionar unidad' and st.button('Realizar cálculo'):
                        try:
                            nominal_seleccionado_float = float(nominal_seleccionado)
                            meas_uncert = buscar_en_sample_cals(sample_cals_data, certificado_objetivo, grupo_seleccionado, nominal_seleccionado_float, unidad_seleccionada)
                            nominal_en_gramos = convertir_a_gramos(nominal_seleccionado_float, unidad_seleccionada)
                            id_cmc, cmc_string = identificar_id_en_certificado_balance(certificado_balance_data, nominal_en_gramos)
                            cmc_fijo, cmc_proporcional = extraer_cmc_fijo_proporcional(cmc_string)
                            total_uncertainty = calcular_incertidumbre(nominal_en_gramos, cmc_fijo, cmc_proporcional, meas_uncert)
                            
                            st.success(f"""
                            Grupo Objetivo: {grupo_seleccionado}\n
                            Valor Nominal Objetivo: {nominal_seleccionado} {unidad_seleccionada}\n
                            Incertidumbre de Medición: {meas_uncert} g\n
                            CMC utilizado: {cmc_string}\n
                            Incertidumbre Total: {total_uncertainty[0]}, {total_uncertainty[1]}, {total_uncertainty[2]}
                            """)
                        except ValueError as e:
                            st.error(f"Error: {e}")
        else:
            st.warning("No se encontró el certificado objetivo.")

elif opcion == 'Buscar certificado por modelo':
    st.header('Búsqueda por Modelo')
    modelo_objetivo = st.text_input("Ingrese el modelo objetivo:")

    if modelo_objetivo:
        modelos_disponibles = [cert['Model'] for cert in sample_cals_data if modelo_objetivo.lower() in cert['Model'].lower()]
        if modelos_disponibles:
            modelo_seleccionado = st.selectbox('Modelos disponibles:', modelos_disponibles)
            certificados_modelo = [cert for cert in sample_cals_data if cert['Model'] == modelo_seleccionado]

            certificado_opciones = [f"{cert['CertNo']} - {cert['AssetDescription']}" for cert in certificados_modelo]
            certificado_seleccionado = st.selectbox("Certificados disponibles:", certificado_opciones, index=0)

            if st.button('¿Usar este número de certificado?'):
                # Extraer el número de certificado de la selección
                numero_certificado = certificado_seleccionado.split(" - ")[0]
                # Guardar el número de certificado en el estado de la sesión para reutilizarlo
                st.session_state['numero_certificado'] = numero_certificado
                # Cambiar la opción seleccionada en la barra lateral para llevar al usuario a la búsqueda por certificado
                st.session_state['opcion'] = 'Ingresar número de certificado'
                # Forzar el recargo de la página para actualizar la selección en la barra lateral
                st.rerun()
        else:
            st.warning("No se encontraron modelos que coincidan con su búsqueda.")
