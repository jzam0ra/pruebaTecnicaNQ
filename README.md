# Prueba Técnica

Esta plantilla de app se toma de un [blog ejemplo de AWS](https://aws.amazon.com/es/blogs/big-data/end-to-end-development-lifecycle-for-data-engineers-to-build-a-data-integration-pipeline-using-aws-glue/). Para más detalles se puede visitar el link en cuestión. Usamos este ejemplo por las herramientas de IaC principalmente, dado que está pensado para ETL's en Glue, las cuales no usamos acá, además de que está pensado para una organización de múltiples cuentas, mientras que en este ejemplo sólo usamos una. Para detalles de cómo implementar este ejemplo en una cuenta propia, se puede guiar también de ese link, teniendo en cuenta que la fuente del Pipeline de datos ahora es GitHub.

![alt text](https://github.com/jzam0ra/pruebaTecnicaNQ/pictures/main/arquitectura.png?raw=true)

Acá nos centraremos en responder las siguientes preguntas:




* `aws_glue_cdk_baseline/job_scripts/tests/test_join_legislators.py`

```python
import pytest
import sys
import join_legislators
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions


@pytest.fixture(scope="module", autouse=True)
def glue_context():
    sys.argv.append('--JOB_NAME')
    sys.argv.append('test_count')

    args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    context = GlueContext(SparkContext.getOrCreate())
    job = Job(context)
    job.init(args['JOB_NAME'], args)

    yield(context)


def test_counts(glue_context):
    dyf = join_legislators.join_legislators(glue_context, 
        "s3://awsglue-datasets/examples/us-legislators/all/organizations.json",
        "s3://awsglue-datasets/examples/us-legislators/all/persons.json", 
        "s3://awsglue-datasets/examples/us-legislators/all/memberships.json")
    assert dyf.toDF().count() == 10439
```

