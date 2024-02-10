from datetime import datetime
import pytest
from telegram import User, Message, Chat


@pytest.fixture
def effective_user():
    return User(
        id=123, first_name="Odin", is_bot=False, last_name="Grom", username="Qwerty"
    )


@pytest.fixture
def message():
    return Message(
        message_id=1,
        date=datetime(2022, 7, 26, 20, 22, 19, 705000),
        chat=Chat(id=1, type="private"),
        chat_id=12121,
    )


@pytest.fixture
def reg_info():
    return {
        "user_name": "Иванов Иван Иванович",
        "birth_date": "14.11.1986",
        "location": "Каманут",
        "relocation": "нет",
        "format_job": "Удаленка",
        "salary": "50-100",
        "number_phone": "+79811399976",
    }


@pytest.fixture
def anketa_data():
    return {
        "company": "AO ASD",
        "vacan": "Proty",
        "answer": {"1": "q", "2": "w", "3": "e"},
        "question": {"1": "who?", "2": "try", "3": "qwerty"},
        "pincode": "001-000",
        "userfile": "File.docx",
    }


@pytest.fixture
def test_info():
    return {
        "test_info": [
            {
                "slots": {
                    "Perl Developer": {
                        "1": "Проверка",
                        "2": "Проверка",
                        "3": "Проверка",
                    }
                },
                "date": {"$date": {"$numberLong": "1656107056666"}},
                "pincode": "005",
            },
            {
                "slots": {
                    "Дизайнер": {"1": "Проверка", "2": "Проверка", "3": "Проверка"}
                },
                "date": {"$date": {"$numberLong": "1656107056666"}},
                "pincode": "008",
            },
        ],
        "answer_true": [
            [{"Perl Developer": {"1": "Проверка", "2": "Проверка", "3": "Проверка"}}],
            [{"Дизайнер": {"1": "Проверка", "2": "Проверка", "3": "Проверка"}}],
        ],
    }


@pytest.fixture
def file_vacancy():
    return {
        "company": "АльфаБанк",
        "pincode": "001",
        "vacancy": {
            "slots": {
                "Системный Аналитик": {
                    "1": "Проверка",
                    "2": "Проверка",
                    "3": "Проверка",
                }
            },
            "date": "1656107056666",
            "pincode": "000",
        },
    }
