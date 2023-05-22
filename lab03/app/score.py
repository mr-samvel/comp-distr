import mqtt

NAME = 'Placar'
SCORE = [0, 0]

def msg_callback(client: mqtt.mqtt_client.Client, userdata, msg: mqtt.mqtt_client.MQTTMessage) -> None:
    text = msg.payload.decode()
    if 'errou' in text:
        if 'pong' in text:
            SCORE[0] += 1
        elif 'ping' in text:
            SCORE[1] += 1
        mqtt.publish(client, mqtt.SCORE_TOPIC, f'{SCORE[0]} x {SCORE[1]}')

def main():
    client = mqtt.connect(NAME)
    mqtt.subscribe(client, mqtt.GAME_TOPIC, msg_callback)
    client.loop_forever()

main()