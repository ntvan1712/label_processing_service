import argparse
from infras import rabbitmq

from label_task.model.label_task_model import LabelTaskModel
from label_task.processing import process_label_task
import json

from graceful_shutdown import ShutdownProtection

def on_message_callback(ch, method, properties, body):
    rabbitmq.ack_message(channel=ch, delivery_tag= method.delivery_tag)
    with ShutdownProtection(max_exec_time=3, run_at_exit= True) as protected_block:
        try:
            print(f"[Consumer.on_message_callback] Start callback on queue name {method.routing_key}. Task :{json.loads(body)}")
            task = LabelTaskModel(json.loads(body)) 
            process_label_task(task= task)
        except (SystemExit, KeyboardInterrupt) as ex:
            print("error_code.SYSTEM_IS_TURNED_USING_THE_KEYBOARD")
        protected_block.allow_break()


if __name__ == '__main__':
    # Get RabbitMQ channel
    channel = rabbitmq.get_rabbit_mq_channel()
    
    # Start consuming the task queue
    rabbitmq.consume_task_queue(queue_name=rabbitmq.label_task_queue_name,
                                        on_message_callback= on_message_callback,
                                        prefetch_count=1)