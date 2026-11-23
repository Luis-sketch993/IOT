import json
import random
import time
from datetime import datetime, timezone

from awscrt import mqtt
from awsiot import mqtt_connection_builder

ENDPOINT = "a3s9qt2gqfrddr-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "estacion-iot-wsl"
TOPIC = "estacion-iot-wsl/telemetry"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath="certificados/device.pem.crt",
    pri_key_filepath="certificados/private.pem.key",
    ca_filepath="certificados/AmazonRootCA1.pem",
    client_id=CLIENT_ID,
    clean_session=True,
    keep_alive_secs=30
)

print("Conectando a AWS IoT Core...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Conectado correctamente.")

for sequence in range(1, 6):
    data = {
        "device_id": CLIENT_ID,
        "sequence": sequence,
        "temperature_c": round(random.uniform(20, 30), 2),
        "humidity_pct": round(random.uniform(40, 80), 2),
        "status": "normal",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(data),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    print(f"Lectura {sequence}: {json.dumps(data)}")
    time.sleep(3)

print("Desconectando...")
mqtt_connection.disconnect().result()
print("Estación IoT finalizada.")
