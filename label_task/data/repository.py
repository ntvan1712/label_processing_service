
from datetime import datetime
import psycopg2
from label_processor.models.product_label_model import ProductLabelModel

_dsn = "postgres://kaido1712:kaido1712@127.0.0.1:5433/asset_management?sslmode=disable"
_asset_table = "asset_label_tasks"
_task_completed_channel = "task_completed_channel"
_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = psycopg2.connect(dsn=_dsn)
    return _connection

def update_success_task(product: ProductLabelModel, task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    fields_to_update = {}
    if product.serial_number is not None:
        fields_to_update["serial_number"] = product.serial_number
    if product.manufacturer is not None:
        fields_to_update["manufacturer"] = product.manufacturer
    if product.made_in is not None:
        fields_to_update["made_in"] = product.made_in
    if product.all_words is not None:
        fields_to_update["all_words"] = product.all_words  
    
    fields_to_update["completed_at"] = datetime.now()

    set_clause = ", ".join([f"{key} = %s" for key in fields_to_update.keys()])
    values = list(fields_to_update.values()) + [task_id]

    update_query = f"""
        UPDATE {_asset_table}
        SET {set_clause}
        WHERE id = %s;
    """

    cursor.execute(update_query, values)
    conn.commit()

    print(f"[LabelTaskRepository.update_success_task] Task with ID {task_id} updated with fields {fields_to_update}")

    cursor.close()

def update_error_task(error_code: str, task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    fields_to_update = {}
    fields_to_update["error_code"] = error_code  
    fields_to_update["completed_at"] = datetime.now()

    set_clause = ", ".join([f"{key} = %s" for key in fields_to_update.keys()])
    values = list(fields_to_update.values()) + [task_id]

    update_query = f"""
        UPDATE {_asset_table}
        SET {set_clause}
        WHERE id = %s;
    """

    cursor.execute(update_query, values)
    conn.commit()

    print(f"[LabelTaskRepository.update_error_task] Task with ID {task_id} updated with fields {fields_to_update}")

    cursor.close()