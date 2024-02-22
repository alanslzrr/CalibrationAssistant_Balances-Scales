import json
import json
import math
import re



def cargar_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Error al cargar el archivo {filename}: {e}")

def buscar_en_sample_cals(sample_cals_data, certificado_objetivo, grupo_objetivo, nominal_objetivo, unidad_objetivo):
    """
    Busca en los datos de certificados (sample_cals_data) una medición específica.
    Parámetros:
    - sample_cals_data: Lista de certificados.
    - certificado_objetivo: Número del certificado a buscar.
    - grupo_objetivo: Grupo de medición objetivo.
    - nominal_objetivo: Valor nominal objetivo.
    - unidad_objetivo: Unidad de medida objetivo.
    Retorna:
    - La incertidumbre de la medición si se encuentra una coincidencia.
    Lanza:
    - Excepción si no se encuentra coincidencia o si la medición no tiene incertidumbre definida.
    """

    for certificado in sample_cals_data:
        if certificado['CertNo'] == certificado_objetivo:
            for datasheet in certificado['Datasheet']:
                if datasheet['Group'] == grupo_objetivo:
                    for measurement in datasheet['Measurements']:
                        if measurement['Units'] == unidad_objetivo and abs(float(measurement['Nominal']) - nominal_objetivo) < 1e-6:
                            if measurement['MeasUncert'] == '**':
                                raise Exception("No se dispone de valor para la incertidumbre de medición seleccionada.")
                            return float(measurement['MeasUncert'])
    raise Exception("No se encontró coincidencia en SampleCals.json")

def elegir_modelo(sample_cals_data):
    """
    Permite al usuario elegir un modelo de una lista basada en la entrada de texto.
    Parámetros:
    - sample_cals_data: Lista de certificados con información de modelo.
    Retorna:
    - El modelo seleccionado por el usuario.
    Lanza:
    - Excepción si no se encuentran modelos que coincidan con la búsqueda.
    """
    input_usuario = input("Ingrese las primeras letras del modelo: ").upper()
    modelos_disponibles = []
    for certificado in sample_cals_data:
        modelo = certificado['Model']
        if modelo not in modelos_disponibles and modelo.upper().startswith(input_usuario):
            modelos_disponibles.append(modelo)
    if not modelos_disponibles:
        raise Exception("No se encontraron modelos que coincidan con su búsqueda.")
    print("Modelos disponibles que coinciden con su búsqueda:")
    for i, modelo in enumerate(modelos_disponibles, start=1):
        print(f"{i}. {modelo}")
    seleccion = int(input("Seleccione el número del modelo deseado: ")) - 1
    if seleccion < 0 or seleccion >= len(modelos_disponibles):
        raise ValueError("Selección de modelo inválida.")
    return modelos_disponibles[seleccion]


def elegir_grupo(sample_cals_data, certificado_objetivo):
    """
    Muestra los grupos disponibles para un certificado específico y permite al usuario elegir uno.
    Parámetros:
    - sample_cals_data: Lista de certificados.
    - certificado_objetivo: Número del certificado para el cual buscar grupos.
    Retorna:
    - El grupo seleccionado por el usuario.
    Lanza:
    - Excepción si no se encuentran grupos para el certificado proporcionado.
    """
    grupos_disponibles = []
    for certificado in sample_cals_data:
        if certificado['CertNo'] == certificado_objetivo:
            for datasheet in certificado['Datasheet']:
                grupo = datasheet['Group']
                if grupo not in grupos_disponibles:
                    grupos_disponibles.append(grupo)
    if not grupos_disponibles:
        raise Exception("No se encontraron grupos para el certificado proporcionado.")
    print("Grupos disponibles:")
    for i, grupo in enumerate(grupos_disponibles, start=1):
        print(f"{i}. {grupo}")
    seleccion = int(input("Seleccione el número del grupo deseado: ")) - 1
    if seleccion < 0 or seleccion >= len(grupos_disponibles):
        raise ValueError("Selección de grupo inválida.")
    return grupos_disponibles[seleccion]

def elegir_nominal(sample_cals_data, certificado_objetivo, grupo_objetivo):
    """
    Muestra los valores nominales disponibles para un grupo específico y permite al usuario elegir uno.
    Parámetros:
    - sample_cals_data: Lista de certificados.
    - certificado_objetivo: Número del certificado.
    - grupo_objetivo: Grupo para el cual buscar valores nominales.
    Retorna:
    - El valor nominal seleccionado por el usuario.
    Lanza:
    - Excepción si no se encuentran valores nominales para el grupo proporcionado.
    """
    nominales_disponibles = []
    for certificado in sample_cals_data:
        if certificado['CertNo'] == certificado_objetivo:
            for datasheet in certificado['Datasheet']:
                if datasheet['Group'] == grupo_objetivo:
                    for measurement in datasheet['Measurements']:
                        nominal = measurement['Nominal']
                        if nominal not in nominales_disponibles:
                            nominales_disponibles.append(nominal)
    if not nominales_disponibles:
        raise Exception("No se encontraron nominales para el grupo proporcionado.")
    print("Valores nominales disponibles:")
    for i, nominal in enumerate(nominales_disponibles, start=1):
        print(f"{i}. {nominal} {datasheet['Measurements'][0]['Units']}")
    seleccion = int(input("Seleccione el número del valor nominal deseado: ")) - 1
    if seleccion < 0 or seleccion >= len(nominales_disponibles):
        raise ValueError("Selección de nominal inválida.")
    return nominales_disponibles[seleccion]

def elegir_unidad():
    """
    Muestra las unidades de medida disponibles y permite al usuario elegir una.
    Retorna:
    - La unidad de medida seleccionada por el usuario.
    Lanza:
    - Excepción si la selección es inválida.
    """
    unidades_disponibles = ['g', 'kg', 'lb']  # Define aquí las unidades que aplican a tu caso
    print("Unidades disponibles:")
    for i, unidad in enumerate(unidades_disponibles, start=1):
        print(f"{i}. {unidad}")
    seleccion = int(input("Seleccione el número de la unidad deseada: ")) - 1
    if seleccion < 0 or seleccion >= len(unidades_disponibles):
        raise ValueError("Selección de unidad inválida.")
    return unidades_disponibles[seleccion]

def convertir_a_gramos(valor, unidad):
    """
    Convierte un valor a gramos según la unidad proporcionada.
    Parámetros:
    - valor: Valor a convertir.
    - unidad: Unidad de origen ('g', 'kg', 'lb').
    Retorna:
    - El valor convertido a gramos.
    Lanza:
    - Excepción si la unidad no es reconocida.
    """

    conversiones = {
        'g': 1,
        'kg': 1e3,
        'lb': 453.59237
    }
    factor_conversion = conversiones.get(unidad)
    if factor_conversion is None:
        raise ValueError(f"Unidad '{unidad}' no reconocida.")
    return valor * factor_conversion

def identificar_id_en_certificado_balance(certificado_balance_data, nominal_en_gramos):
    """
    Identifica el ID y CMC de un rango que incluya el valor nominal en gramos.
    Parámetros:
    - certificado_balance_data: Lista de rangos y CMCs.
    - nominal_en_gramos: Valor nominal en gramos a buscar.
    Retorna:
    - ID y CMC del rango encontrado.
    Lanza:
    - Excepción si no se encuentra un rango adecuado.
    """
    for registro in certificado_balance_data:
        minimo = float(registro['Range']['Min'])
        maximo = float(registro['Range']['Max'])
        if minimo <= nominal_en_gramos <= maximo:
            return registro['ID'], registro['CMC']
    raise Exception("No se encontró un rango adecuado en CertificadoBalance.json")

def convertir_unidad_a_gramos(valor, unidad):
    """
    Convierte un valor a gramos desde distintas unidades, incluyendo unidades compuestas.
    Parámetros:
    - valor: Valor a convertir.
    - unidad: Unidad de origen.
    Retorna:
    - El valor convertido a gramos.
    """
    conversiones = {
        'µg': 1e-6,
        'μg': 1e-6,
        'mg': 1e-3,
        'g': 1,
        'kg': 1e3
    }

    # Casos especiales para unidades compuestas
    if '/' in unidad:
        unidad_base, unidad_referencia = unidad.split('/')
        valor_base = valor * conversiones.get(unidad_base.strip(), 0)

        # Extraer la parte numérica de la unidad de referencia
        numero_referencia = re.findall(r'\d+', unidad_referencia)
        if numero_referencia:
            numero_referencia = float(numero_referencia[0])
        else:
            # Si no hay número, asumir que el factor de referencia es 1 (como en 'μg/g')
            numero_referencia = 1.0

        if 'kg' in unidad_referencia:
            return valor_base / (numero_referencia * conversiones['kg'])
        elif 'g' in unidad_referencia:
            return valor_base / (numero_referencia * conversiones['g'])
    else:
        # Casos estándar
        return valor * conversiones.get(unidad, 0)

def extraer_cmc_fijo_proporcional(cmc):
    """
    Extrae los componentes fijo y proporcional del CMC.

    Parámetros:
    cmc (str): Cadena del CMC en formato "fijo μg + proporcional μg/g".

    Retorna:
    (float, float): Componente fijo y componente proporcional del CMC.
    """
    partes = cmc.split('+')
    cmc_fijo = float(partes[0].strip().split(' ')[0])  # Extraer el componente fijo
    cmc_proporcional = float(partes[1].strip().split(' ')[0])  # Extraer el componente proporcional

    return cmc_fijo, cmc_proporcional
def calcular_incertidumbre(valor_nominal, cmc_fijo, cmc_proporcional, meas_uncert):
    """
    Calcula la incertidumbre combinada a partir de los componentes fijo y proporcional del CMC, y la incertidumbre de la medición.
    Parámetros:
    - valor_nominal: Valornominal en gramos.
    - cmc_fijo: Componente fijo del CMC.
    - cmc_proporcional: Componente proporcional del CMC.
    - meas_uncert: Incertidumbre de la medición.
    Retorna:
    - Incertidumbre combinada en gramos, miligramos y microgramos.
    """
    valor_nominal = float(valor_nominal)
    cmc_fijo_g = convertir_unidad_a_gramos(cmc_fijo, 'μg')  # Usar función para conversión
    cmc_proporcional_g = convertir_unidad_a_gramos(cmc_proporcional, 'μg/g')  # Usar función para conversión
    meas_uncert_g = float(meas_uncert)

    cmc_total = cmc_fijo_g + (cmc_proporcional_g * valor_nominal)
    incertidumbre_combinada = math.sqrt(cmc_total**2 + meas_uncert_g**2)

    # Formatear los resultados directamente como cadenas
    incertidumbre_combinada_str = f"{incertidumbre_combinada:.4f} g"
    incertidumbre_combinada_mg_str = f"{incertidumbre_combinada * 1000:.4f} mg"
    incertidumbre_combinada_ug_str = f"{incertidumbre_combinada * 1e6:.4f} μg"

    return incertidumbre_combinada_str, incertidumbre_combinada_mg_str, incertidumbre_combinada_ug_str



def main():
    """
    Función principal que implementa un menú interactivo para interactuar con datos de certificados.
    
    La función carga datos de certificados de calibración y balance desde archivos JSON, y luego
    presenta un menú principal con tres opciones:
    
    1. Realizar búsqueda en SampleCals por certificado: Permite al usuario buscar información
       específica de medición y calcular la incertidumbre total basada en el certificado, grupo,
       valor nominal, y unidad seleccionados.
    
    2. Realizar búsqueda en SampleCals por modelo: Facilita al usuario la búsqueda de certificados
       por modelo de equipo. Después de seleccionar un modelo, muestra los certificados asociados y
       permite realizar una búsqueda detallada para calcular la incertidumbre total.
    
    3. Salir: Termina la ejecución del programa.
    
    En cada opción, se utilizan varias funciones auxiliares para solicitar y procesar la entrada
    del usuario, realizar búsquedas en los datos, y mostrar resultados relevantes.
    """
    sample_cals_data = cargar_json("SampleCals.json")
    certificado_balance_data = cargar_json("CertificadoBalance.json")

    while True:
        print("\nMenú Principal:")
        print("1. Realizar búsqueda en SampleCals por certificado")
        print("2. Realizar búsqueda en SampleCals por modelo")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            certificado_objetivo = input("Ingrese el certificado objetivo: ")
            try:
                grupo_objetivo = elegir_grupo(sample_cals_data, certificado_objetivo)
                nominal_objetivo = float(elegir_nominal(sample_cals_data, certificado_objetivo, grupo_objetivo))
                unidad_objetivo = elegir_unidad()

                meas_uncert = buscar_en_sample_cals(sample_cals_data, certificado_objetivo, grupo_objetivo, nominal_objetivo, unidad_objetivo)
                nominal_en_gramos = convertir_a_gramos(nominal_objetivo, unidad_objetivo)
                id_cmc, cmc_string = identificar_id_en_certificado_balance(certificado_balance_data, nominal_en_gramos)
                cmc_fijo, cmc_proporcional = extraer_cmc_fijo_proporcional(cmc_string)
                total_uncertainty = calcular_incertidumbre(nominal_en_gramos, cmc_fijo, cmc_proporcional, meas_uncert)

                print(f"Incertidumbre de Medición: {meas_uncert} g")
                print(f"CMC utilizado: {cmc_string}")
                print(f"Incertidumbre Total: {total_uncertainty[0]}, {total_uncertainty[1]}, {total_uncertainty[2]}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif opcion == "2":
            try:
                modelo_objetivo = elegir_modelo(sample_cals_data)
                certificados_modelo = []
                print(f"\nCertificados para el modelo '{modelo_objetivo}':")
                for certificado in sample_cals_data:
                    if certificado['Model'] == modelo_objetivo:
                        info_cert = f"CertNo: {certificado['CertNo']}, Descripción: {certificado['AssetDescription']}, Rango de Operación: {certificado['OperatingRange']}"
                        print(info_cert)
                        certificados_modelo.append(certificado['CertNo'])
                
                if certificados_modelo:
                    usar_certificado = input("¿Desea usar alguno de estos números de certificado para una búsqueda en SampleCals? (s/n): ")
                    if usar_certificado.lower() == 's':
                        print("Certificados disponibles:")
                        for i, certNo in enumerate(certificados_modelo, 1):
                            print(f"{i}. {certNo}")
                        seleccion_certificado = int(input("Seleccione el número del certificado deseado: ")) - 1
                        if seleccion_certificado < 0 or seleccion_certificado >= len(certificados_modelo):
                            raise ValueError("Selección de certificado inválida.")
                        certificado_objetivo = certificados_modelo[seleccion_certificado]
                        
                        try:
                            grupo_objetivo = elegir_grupo(sample_cals_data, certificado_objetivo)
                            nominal_objetivo = float(elegir_nominal(sample_cals_data, certificado_objetivo, grupo_objetivo))
                            unidad_objetivo = elegir_unidad()

                            meas_uncert = buscar_en_sample_cals(sample_cals_data, certificado_objetivo, grupo_objetivo, nominal_objetivo, unidad_objetivo)
                            nominal_en_gramos = convertir_a_gramos(nominal_objetivo, unidad_objetivo)
                            id_cmc, cmc_string = identificar_id_en_certificado_balance(certificado_balance_data, nominal_en_gramos)
                            cmc_fijo, cmc_proporcional = extraer_cmc_fijo_proporcional(cmc_string)
                            total_uncertainty = calcular_incertidumbre(nominal_en_gramos, cmc_fijo, cmc_proporcional, meas_uncert)

                            print(f"Incertidumbre de Medición: {meas_uncert} g")
                            print(f"CMC utilizado: {cmc_string}")
                            print(f"Incertidumbre Total: {total_uncertainty[0]}, {total_uncertainty[1]}, {total_uncertainty[2]}")
                        except Exception as e:
                            print(f"Error al buscar detalles del certificado: {e}")
                    elif usar_certificado.lower() == 'n':
                        print("Regresando al menú principal.")
                    else:
                        print("Opción no válida, regresando al menú principal.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    main()

"""
Interacción con el menú:
- Elija una opción del menú principal tecleando 1, 2 o 3 y presione Enter.

Opción 1: Búsqueda por certificado
  1.1 Ingrese el número de certificado específico.
  1.2 Seleccione un grupo de medición de la lista proporcionada.
  1.3 Elija un valor nominal de los disponibles para el grupo seleccionado.
  1.4 Seleccione la unidad de medida (g, kg, lb).
  1.5 El sistema buscará y mostrará la incertidumbre de medición correspondiente, junto con el CMC utilizado y la incertidumbre total calculada.

Opción 2: Búsqueda por modelo
  2.1 Escriba las primeras letras del modelo y seleccione de la lista filtrada.
  2.2 Se mostrarán los certificados asociados al modelo seleccionado.
  2.3 Elija un número de certificado de la lista para realizar una búsqueda detallada, repitiendo los pasos 1.2 a 1.5 para este certificado específico.

Opción 3: Salir del programa
- Utilice esta opción para finalizar la ejecución del programa en cualquier momento.
"""