import logging
import time
import json
from config import Config
from db_connector import DBConnector
from slack_notifier import SlackNotifier

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Словарь для преобразования названий валют
currency_map = {
    'Bitcoin': 'BTC',
    'Tether': 'USDT',
    'Litecoin': 'LTC',
    'Tron': 'TRX',
    'Dogecoin': 'DOGE',
    'Binance Coin': 'BNB',
    'Ethereum': 'ETH'
}

def main():
    logger.info('Starting the script...')
    config = Config()
    db = DBConnector(config)
    slack_notifier = SlackNotifier(config)

    last_processed_id = 9189
    while True:
        transactions = db.get_risk_transactions(last_processed_id)
        if transactions:
            for transaction in transactions:
                # Обрабатываем каждую транзакцию
                last_processed_id = transaction['id']  # Обновляем перед обработкой транзакции
                logger.info(f"Processing transaction {transaction['id']}...")
                project_name = db.get_project_name(transaction['project_id'])
                currency_name = currency_map.get(transaction['currency_name'], transaction['currency_name'])
                transaction_id = db.get_transaction_id(transaction['hash_transaction'])
                external_transaction_id = transaction['external_transaction_id']
                risk_score_details = transaction['risk_score_details']
                if risk_score_details:
                    risk_score_json = json.loads(risk_score_details)
                    crystal_id = risk_score_json.get('id', 'N/A')
                else:
                    crystal_id = 'N/A'

                buttons = [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cryptonix CRM"
                        },
                        "action_id": "button_1_click",  # Уникальный идентификатор для кнопки 1
                        "url": f"https://admin.cryptonix.com/approvements/merchant/{crystal_id}"  # Ссылка для кнопки 1
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Crystal Monitor"
                        },
                        "action_id": "button_2_click",  # Уникальный идентификатор для кнопки 2
                        "url": "https://expert.crystalblockchain.com/monitor/transfers"  # Ссылка для кнопки 2
                    }
                ]


                message = (f":name_badge: Risk transaction by *{project_name}*\n"
                           f"\n"
                           f":money_with_wings: Amount: {transaction['amount']} {currency_name}\n"
                           f"```Transaction ID: {transaction_id}\n"
                           f"Transaction UUID: {external_transaction_id}\n"
                           f"Transaction ID in Crystal: {crystal_id}```")
                
                slack_notifier.send_message_with_buttons(message, buttons)
                
                logger.info(f"Message sent for transaction ID {last_processed_id}. Waiting for new transactions...")
            
            logger.info(f"Last processed transaction ID is now: {last_processed_id}")
        else:
            logger.info('No new risk_processing transactions found. Waiting for new transactions...')

        time.sleep(300)  # Пауза перед следующей проверкой

if __name__ == "__main__":
    main()
