from .main import RabbitMQMessagingConfig,ExchangeType
from .controllers.controller import ConsumersHandler
import asyncio

async def worker():
    rabbitmq_conn=await RabbitMQMessagingConfig.get_rabbitmq_connection()
    rabbitmq_msg_obj=RabbitMQMessagingConfig(rabbitMQ_connection=rabbitmq_conn)

    # Exchanges
    exchanges=[
        {'name':'shops.inventory.products.exchange','exc_type':ExchangeType.TOPIC},
        {'name':'inventory.inventory.products.exchange','exc_type':ExchangeType.TOPIC},
        {'name':'purchase.purchase.products.exchange','exc_type':ExchangeType.TOPIC},
        {'name':'suppliers.purchase.products.exchange','exc_type':ExchangeType.TOPIC},
    ]

    for exchange in exchanges:
        await rabbitmq_msg_obj.create_exchange(name=exchange['name'],exchange_type=exchange['exc_type'])

    # Queues
    queues=[
        {'exc_name':'shops.inventory.products.exchange','q_name':'shops.inventory.products.queue','r_key':'shops.inventory.*.*.v1'},
        {'exc_name':'inventory.inventory.products.exchange','q_name':'inventory.inventory.products.queue','r_key':'inventory.inventory.*.*.v1'},
        {'exc_name':'purchase.purchase.products.exchange','q_name':'purchase.purchase.products.queue','r_key':'purchase.purchase.*.*.v1'},
        {'exc_name':'suppliers.purchase.products.exchange','q_name':'suppliers.purchase.products.queue','r_key':'suppliers.purchase.*.*.v1'},
    ]

    for queue in queues:
        queue=await rabbitmq_msg_obj.create_queue(
            exchange_name=queue['exc_name'],
            queue_name=queue['q_name'],
            routing_key=queue['r_key']
        )

    # Consumers
    consumers=[
        {'q_name':'shops.inventory.products.queue','handler':ConsumersHandler.main_handler},
        {'q_name':'inventory.inventory.products.queue','handler':ConsumersHandler.main_handler},
        {'q_name':'purchase.purchase.products.queue','handler':ConsumersHandler.main_handler},
        {'q_name':'suppliers.purchase.products.queue','handler':ConsumersHandler.main_handler},
    ]

    for consumer in consumers:
        await rabbitmq_msg_obj.consume_event(queue_name=consumer['q_name'],handler=consumer['handler'])

    await asyncio.Event().wait()

if __name__=="__main__":
    asyncio.run(worker())

    



    