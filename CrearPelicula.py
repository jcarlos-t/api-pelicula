import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Log de entrada (INFO)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {"evento": "inicio_crear_pelicula", "event": event}
        }, ensure_ascii=False))

        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de salida (INFO)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {"evento": "pelicula_creada", "pelicula": pelicula}
        }, ensure_ascii=False))

        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log de error (ERROR)
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "evento": "error_crear_pelicula",
                "detalle": str(e)
            }
        }, ensure_ascii=False))

        return {
            'statusCode': 500,
            'error': str(e)
        }
