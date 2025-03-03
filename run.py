import argparse
from infras import rabbit_mq


import json

from graceful_shutdown import ShutdownProtection

def on_message_callback(ch, method, properties, body):
    rabbit_mq.ack_message(channel=ch, delivery_tag= method.delivery_tag)
    with ShutdownProtection(max_exec_time=3, run_at_exit= True) as protected_block:
        try:
            print(f"[Consumer.on_message_callback] Start callback on queue name {method.routing_key}. Task :{json.loads(body)}")
        except (SystemExit, KeyboardInterrupt) as ex:
            print("error_code.SYSTEM_IS_TURNED_USING_THE_KEYBOARD")
        protected_block.allow_break()


if __name__ == '__main__':
    # Get RabbitMQ channel
    channel = rabbit_mq.get_rabbit_mq_channel()
    # Declare the completed task queue with priority for push notification
    channel.queue_declare(queue=rabbit_mq.label_task_queue_name, 
                          durable=True, 
                          arguments={"x-max-priority": 10})
    

    # Start consuming the task queue
    rabbit_mq.consume_task_queue(queue_name=rabbit_mq.label_task_queue_name,
                                        on_message_callback= on_message_callback,
                                        prefetch_count=1)