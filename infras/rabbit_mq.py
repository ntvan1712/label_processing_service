import pika
import pika.exceptions

title_log = "RabbitMQInfras"

# Định nghĩa tên của queue và các thông tin kết nối
label_task_queue_name = "label_task_queue"
_credentials = pika.PlainCredentials('asset_label_service', 'kaido1712')
_parameters = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    virtual_host='asset_management',
    credentials=_credentials,
    heartbeat=60 * 5,
)

_connection = None
_channel = None

def close_existing_connection():
    global _connection, _channel
    if _channel is not None and not _channel.is_closed:
        try:
            _channel.close()
        except pika.exceptions.ChannelClosedByBroker:
            pass 
    if _connection is not None and not _connection.is_closed:
        try:
            _connection.close()
        except pika.exceptions.ConnectionClosedByBroker:
            pass 

def init():
    global _connection, _channel
    # Đóng kết nối hiện tại nếu nó đang mở
    close_existing_connection()
    
    # Tạo kết nối và channel mới
    _connection = pika.BlockingConnection(_parameters)
    _channel = _connection.channel()
    return _channel

def get_rabbit_mq_channel():
    global _channel
    if _channel is None or _channel.is_closed:
        _channel = init()
    return _channel


def consume_task_queue(on_message_callback, prefetch_count, queue_name):
    while True:
        try:
            print(f'[{title_log}.consume_task_queue] Start connect queue name {queue_name}')
            channel = get_rabbit_mq_channel()
            # Set consumer chỉ nhận tối đa một số lượng task nhất định (prefetch_count)
            channel.basic_qos(prefetch_count=prefetch_count)
            # Register callback function và bắt đầu tiêu thụ message
            channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)
            
            try:
                print(f'[{title_log}.consume_task_queue] Queue {queue_name}. Waiting for messages. To exit press CTRL+C')
                channel.start_consuming()
            except Exception as e:
                print(f'[{title_log}.consume_task_queue] Error: Unknown - {str(e)}')
                channel.stop_consuming()

            _connection.close()
            # print("_connection.close()")
            
        except KeyboardInterrupt:
            print(f'[{title_log}.consume_task_queue] Stop: User terminate')
            break
        except pika.exceptions.ConnectionClosedByBroker:
            print(f'[{title_log}.consume_task_queue] Error: ConnectionClosedByBroker')
            continue
        except pika.exceptions.AMQPChannelError as e:
            print(f'[{title_log}.consume_task_queue] Error: AMQPChannelError {e}')
            continue
        except pika.exceptions.ConnectionBlockedTimeout:
            print(f'[{title_log}.consume_task_queue] Error: ConnectionBlockedTimeout')
            continue
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            print(f'[{title_log}.consume_task_queue] Error: AMQPConnectionError')
            continue
        except Exception as e:
            print(f'[{title_log}.consume_task_queue] Error: Unknown - {str(e)}')
            continue


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag=delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass