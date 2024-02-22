# Asistente  Calibración de Balanzas

## Descripción
Este proyecto desarrolla un asistente de software diseñado para facilitar y mejorar la precisión en el proceso de calibración de balanzas para inspectores de calibración. Se centra en el cálculo preciso de la incertidumbre de medición, siguiendo las directrices de la ISO/IEC 17025:2017, y ofrece un método sistemático para validar y ajustar instrumentos de medición de peso.

## Características Principales

- **Extracción y análisis de datos:** Procesamiento de datos de calibración desde archivos JSON, interpretando y analizando la incertidumbre de medición ('Meas Uncert') y el CMC (Capacidad de Medición y Calibración).

- **Cálculo de incertidumbre de medición:** Implementación de algoritmos avanzados para calcular la incertidumbre asociada a las mediciones de las balanzas, siguiendo las directrices de la ISO.

- **Conversión y normalización de unidades:** Capacidad para convertir y normalizar diversas unidades de medida a un estándar común, garantizando precisión y consistencia.

- **Adaptabilidad y escalabilidad:** Diseño flexible para adaptarse a diferentes tipos y rangos de balanzas, permitiendo su uso en variados contextos industriales.

## Preparación

### Datos Clave
Identificar y comprender los datos clave para el cálculo de la incertidumbre, incluyendo:
- 'Meas Uncert' del instrumento.
- CMC para el rango de medición, incluyendo componentes fijos y proporcionales.

### Estructura de Datos
Organización y acceso a datos en archivos JSON (`SampleCals.json` y `CertificadoBalance.json`) que contienen información relevante sobre las balanzas y sus incertidumbres asociadas.

### Conversión de Unidades
Métodos para convertir unidades a un estándar común (gramos), dada la variabilidad de unidades en la incertidumbre y las mediciones.

### Descomposición del CMC
Comprensión y descomposición del CMC en componentes fijos y proporcionales al valor nominal.

### Suma Cuadrática para Incertidumbre Total
Cálculo de la incertidumbre total mediante la suma cuadrática de 'Meas Uncert', CMC fijo, CMC proporcional, y otras fuentes de incertidumbre.

## Funciones Principales del Código

### `cargar_json(filename)`
Carga y valida datos desde archivos JSON, asegurando que la estructura de los datos sea compatible con los requerimientos del análisis.

### `buscar_en_sample_cals(sample_cals_data, certificado_objetivo, grupo_objetivo, nominal_objetivo, unidad_objetivo)`
Realiza una búsqueda detallada dentro de los datos de calibración, permitiendo identificar la incertidumbre específica asociada a un certificado, grupo, valor nominal, y unidad.

### `elegir_modelo(sample_cals_data)`
Permite al usuario seleccionar un modelo de equipo de una lista basada en los datos disponibles, facilitando el filtrado y la búsqueda específica por modelos de balanza.

### `convertir_a_gramos(valor, unidad)`
Convierte valores entre diferentes unidades de medida a gramos, utilizando un método que garantiza la precisión y consistencia en las conversiones.

### `calcular_incertidumbre(valor_nominal, cmc_fijo, cmc_proporcional, meas_uncert)`
Calcula la incertidumbre total de una medición combinando los componentes de incertidumbre 'Meas Uncert', el CMC fijo, el CMC proporcional, y cualquier otra fuente de incertidumbre relevante.

## Implementación

El desarrollo de este asistente automatizado se centra en la creación de un conjunto cohesivo de herramientas y funciones que se integran para formar un flujo de trabajo eficiente para la calibración de balanzas. Cada componente ha sido diseñado para ser modular, permitiendo su adaptación o extensión según sea necesario para acomodar nuevos tipos de balanzas o requisitos de calibración.

## Uso del Asistente

Para utilizar el asistente, el usuario deberá seguir un proceso sistemático que comienza con la carga de los archivos de datos JSON relevantes, seguido de la selección de parámetros específicos de calibración como el modelo de balanza, el grupo de medición, el valor nominal, y la unidad de medida. A partir de esta información, el asistente calculará y presentará la incertidumbre de la medición conforme a las normas **ISO/IEC 17025:2017**.


