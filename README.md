# Prueba Técnica

Esta plantilla de app se toma de un [blog ejemplo de AWS](https://aws.amazon.com/es/blogs/big-data/end-to-end-development-lifecycle-for-data-engineers-to-build-a-data-integration-pipeline-using-aws-glue/). Para más detalles se puede visitar el link en cuestión. Usamos este ejemplo por las herramientas de IaC principalmente, dado que está pensado para ETL's en Glue, las cuales no usamos acá, además de que está pensado para una organización de múltiples cuentas, mientras que en este ejemplo sólo usamos una. Para detalles de cómo implementar este ejemplo en una cuenta propia, se puede guiar también de ese link, teniendo en cuenta que la fuente del Pipeline de datos ahora es GitHub.




Acá nos centraremos en responder las siguientes preguntas:

1. Alcance del proyecto y captura de datos
Los datos usados para este proyecto fueron extraídos de [datos abiertos colombia, precipitación](https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Precipitaci-n/s54a-sgyg/about_data). Los datos utilizados fueron suministrados por el Instituto de Hidrología, Meteorología y Estudios Ambientales. Estos corresponden a un histórico de registro de precipitaciones en distintos sensores de monitoreo a nivel Nacional. El propósito es poder hacer una ingesta, limpieza y transformación de estos datos de manera que se disponibilicen como base de datos de fuentes de verdad para usos de análisis o monitoreo.


2. Explorar y evaluar los datos, el EDA.

• En este aspecto no se llegó a gran profundidad dado principalmente a que las ETLs escogidas fueron esencialmente sencillas, esto de nuevo dado a que se prefirió dar un enfoque al diseño de una arquitectura costo-eficiente en la nube. Algunas de las validaciones hechas para verificar la calidad de los datos requeridos en las transformaciones fueron:

* `aws_cdk_baseline/project_files/lambda/lambda/lam_data_extraction.py`
```python
        print("Performing data cleaning...")
        data['fechaobservacion'] = pd.to_datetime(data['fechaobservacion'], errors='coerce')
        data = data.dropna(subset=['fechaobservacion'])  
        data['dt_key'] = data['fechaobservacion'].dt.strftime('%Y%m%d%H')
        data = data.drop_duplicates() 

        print("Performing data cleaning...")
        data['valorobservado'] = pd.to_datetime(data['valorobservado'], errors='coerce')
        data = data.dropna(subset=['valorobservado'])
```


3. Definir el modelo de datos

El modelo de datos escogido para este caso es sencillo ya que se quiso dar un poco más de importancia a la arquitectura en sí del proceso mas que a la complejidad de las transformaciones. Por ello se escogieron dos tablas de transformación más la tabla originalmente extraída:

![alt text](https://github.com/jzam0ra/pruebaTecnicaNQ/blob/main/pictures/modelodatos.png?raw=true)


La arquitectura escogida consta de los siguientes recursos en la nube:

![alt text](https://github.com/jzam0ra/pruebaTecnicaNQ/blob/main/pictures/arquitectura.png?raw=true)


• Los servicios escogidos en la arquitectura se decidieron dado que se ha experimentado que son algunos de los servicios que resultan más costo-eficientes para tareas de preprocesamientos, ingestas y volúmenes de consulta pequeños. Es por esto que se determinó usar:
    * Lambda para el procesamiento de datos, ya que permite desplegar paquetes pequeños, y su costo es bajo.
    * El catálogo de glue permite tener hasta 1 millón de objetos almacenados en su capa gratuita, por lo cual al juntar esto con la metadata que nos permite trabajar athena, podemos consultar los datos almacenados con el motor de consulta de athena por un bajo precio, evitando tener que manejar bases de datos en Dynamo o Redshift. Un ejemplo de cómo se disponibilizarían los datos desde athena para este ejemplo se ve a continuación:

![alt text](https://github.com/jzam0ra/pruebaTecnicaNQ/blob/main/pictures/tablas.png?raw=true)

    * Las herramientas de orquestación como el EventBridge o StepFunctions, son comúnmente usadas para programar flujos de trabajo porque permiten funcionar basado en eventos, lo cual es una aspiración primordial en la nube, y por otro lado, estos servicios evitan tener que manejar un ambiente de Airflow en AWS.
• Proponga con qué frecuencia deben actualizarse los datos y por qué.
    * Los datos, como se propone en esta arquitectura podrían actualizarse, en caso de que el caso de uso no lo vea tan necesario, una vez cada día. En situaciones NRT se podría hacer cada hora, y para monitoreo en tiempo real, como lo formula una pregunta posterior, se puede usar el servicio de streaming Kinesis.


4. Completar la redacción del proyecto

• ¿Cuál es el objetivo del proyecto?
* Lo que se pretende es tener un seguimiento de las precipitaciones en Colombia, esto con el fín de poder predecir tendencias o comportamientos atípicos.

• ¿Qué preguntas quieres hacer?
* ¿Qué tanto ha llovido por departamento o municipio, en los últimos días en Colombia?, con los datos históricos, ¿qué tipo de análisis predictivos se pueden hacer?

• ¿Por qué eligió el modelo que eligió?
* fue un modelo sencillo pensado en proponer enfoques distintos a estudiar un fenómeno importante en este momento de la historia. Este permitía ilustrar un enfoque costo-eficiente de una arquitectura de datos en la plataforma AWS, teniendo en cuenta prácticas DevOps y CI/CD.

• Incluya una descripción de cómo abordaría el problema de manera diferente en los siguientes
escenarios:
o Si los datos se incrementaran en 100x.
* Se puede abordad la arquitectura desde 2 enfoques distintos: Usar AWS Glue para los trabajos de ETL, ya que Spark está diseñado para trabajar en Big Data. 

o Si las tuberías se ejecutaran diariamente en una ventana de tiempo especifica.
* Actualmente la arquitectura contempla esto, con una ejecución recurrente diaria. Se puede también modificar para que sea basada en eventos, y se ejecute la ingesta principal NRT (cada hora).

o Si la base de datos necesitara ser accedido por más de 100 usuarios funcionales.
* Se pueden implementar clústeres en RedShift para tener un sistema de bases de datos robustas, distinto a utilizar el catálogo de glue y Athena como motor de consulta.

o Si se requiere hacer analítica en tiempo real, ¿cuales componentes cambiaria a su arquitectura propuesta?
* Si se requiere en tiempo real, se puede usar AWS Kinesis, ya que este permite ingerir, procesar y almacenar datos en tiempo real. Esto junto con una modificación a la arquitectura para que sea basada en eventos y no en programación, se puede lograr con los mismo componentes en Lambda. 




