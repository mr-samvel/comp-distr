from paho.mqtt import client as mqtt_client
from typing import Callable, Any

GAME_TOPIC = 'ping-pong'
SCORE_TOPIC = 'placar'

def broker_info():
    broker = 'mosquitto'
    port = 1883
    return broker, port

def connect(client_id: str) -> mqtt_client.Client:
    def on_connet_cb(client, userdata, flags, rc):
        if rc == 0:
            print(f'{client_id}: Conectado ao broker!')
        else:
            print(f'{client_id}: Falha ao conectar-se com o broker!!!')
    
    client = mqtt_client.Client(client_id, clean_session=True, userdata={'client_id': client_id})
    client.on_connect = on_connet_cb
    client.connect(*broker_info())
    return client

def subscribe(client: mqtt_client.Client, topic: str, on_msg_cb: Callable[[mqtt_client.Client, Any, mqtt_client.MQTTMessage], None]) -> None:
    client.subscribe(topic, qos=2)
    client.on_message = on_msg_cb

def publish(client: mqtt_client.Client, topic: str, msg: str) -> bool:
    return client.publish(topic, msg).is_published()