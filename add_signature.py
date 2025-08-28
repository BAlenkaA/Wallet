import hashlib


def compute_signature(account_id: int, amount: int, transaction_id: str, user_id: int, secret_key: str) -> str:
    """
        Вычисляет цифровую подпись для транзакции.

        Формирует строку из параметров транзакции и секретного ключа,
        затем вычисляет SHA-256 хеш этой строки.

        Args:
            account_id (int): Уникальный идентификатор счета пользователя
            amount (int): Сумма пополнения счета пользователя
            transaction_id (str): Уникальный идентификатор транзакции в “сторонней системе”
            user_id (int): Уникальный идентификатор счета пользователя
            secret_key (str): Подпись объекта

        Returns:
            str: SHA-256 хеш в виде шестнадцатеричной строки
        """
    signature_string = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
    computed_signature = hashlib.sha256(signature_string.encode()).hexdigest()
    return computed_signature

if __name__ == "__main__":
    params = {
        'account_id': 2,
        'amount': 500,
        'transaction_id': "b73ddede-ecbb-402e-8a92-b44655c1f440",
        'user_id': 1,
        'secret_key': "gfdmhghif38yrf9ew0jkf32"
    }

    signature = compute_signature(
        account_id=params['account_id'],
        amount=params['amount'],
        transaction_id=params['transaction_id'],
        user_id=params['user_id'],
        secret_key=params['secret_key']
    )
    print(f"Signature: {signature}")