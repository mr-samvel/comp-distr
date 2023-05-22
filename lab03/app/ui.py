import mqtt

NAME = 'UI'

def msg_callback(client: mqtt.mqtt_client.Client, userdata, msg: mqtt.mqtt_client.MQTTMessage) -> None:
    text = msg.payload.decode()
    topic = msg.topic
    if topic == mqtt.SCORE_TOPIC:
        text = text.split()
        ping_score = text[0]
        pong_score = text[2]
        print('')
        print('Ponto!')
        print(f'Placar: {ping_score} (Ping) x {pong_score} (Pong)')
        print('')
    elif topic == mqtt.GAME_TOPIC:
        out = '\t\t' if 'pong' in text else ''
        if 'errou' in text:
            out += 'ERROU'
        elif 'saque' in text:
            out += 'SAQUE'
        else:
            out += text.upper()
        print(out)

def main():
    try:
        client = mqtt.connect(NAME)
        mqtt.subscribe(client, mqtt.GAME_TOPIC, msg_callback)
        mqtt.subscribe(client, mqtt.SCORE_TOPIC, msg_callback)
        client.loop_forever()
    except KeyboardInterrupt:
        print(f'{NAME}: Programa encerrado manualmente.')
    except Exception as e:
        print(f'{NAME}: Programa encerrou!!! {e}')

main()