import mqtt
from random import randint
from time import sleep

NAME = 'Pong'

def msg_callback(client: mqtt.mqtt_client.Client, userdata, msg: mqtt.mqtt_client.MQTTMessage) -> None:
    text = msg.payload.decode()
    if 'ping' in text:
        sleep(3)
        serve = 'pong'
        if 'errou' in text: serve += ' - saque'
        if randint(0, 3) == 0: serve += ' - errou'
        mqtt.publish(client, mqtt.GAME_TOPIC, serve) 

def main():
    try:
        client = mqtt.connect(NAME)
        mqtt.subscribe(client, mqtt.GAME_TOPIC, msg_callback)
        client.loop_forever()
    except KeyboardInterrupt:
        print(f'{NAME}: Programa encerrado manualmente.')
    except Exception as e:
        print(f'{NAME}: Programa encerrou!!! {e}')

main()