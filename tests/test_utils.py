from bot.utils import check_role
from bot.conversation.utils import format_text, check_phone, key_quest, get_city, get_date, search_vacan, get_use_code, pincode
from bot import constants

#Test bot.utils
def test_check_role_admin():
    user_id = 1385186381
    assert check_role(user_id) == constants.ADMIN
    assert check_role(user_id) != constants.USER

def test_check_role_user():
    user_id = 32423424265
    assert check_role(user_id) == constants.USER
    assert check_role(user_id) != constants.ADMIN

#Test bot.conversation.utils
def test_format_text():
    dicts = {'1': 'qwer', '2': 'zver', '3': 'qwerty'}
    key_num = key_quest(dicts)
    for num in key_num:
        assert format_text(dicts, num) == f"""<b>Вопрос № {num}:</b>\n {dicts[num]}"""

def test_get_city():
    job_city = ['Москва','Мск','Moscow','мск','мСк','МСК', 'МОСКВА', 'москВа']
    other_city = ['ароном', 435345345, 'asdsfsdf']
    for city in job_city:
        assert get_city(city) == True
    for city in other_city:
        assert get_city(city) == False

def test_get_date():
    date_true = '15.11.1990'
    date_false = ['1212324','21121996','sdasdaf',324234324,11121993,'11/12/1993']
    assert get_date(date_true) == True
    for date in date_false:
        assert get_date(date) == False

def test_check_phone():
    phone_true = [89200399976,'89200399976','+79200399976','9200399976']
    phone_false = ['131231313', '09200399976']
    for phone in phone_true:
        assert check_phone(phone) == True
    for phone in phone_false:
        assert check_phone(phone) == False

def test_pincode():
    pincod_true = ['111-112','asd-sadasd']
    answer_true = [['111','112'],['asd','sadasd'],['121','121']]
    pincod_false = [1231321,'sdasdsfdf']
    answer_false = [['1231321'],['sdasdsfdf']]
    for index,pin in enumerate(pincod_true):
        assert pincode(pin) == answer_true[index]
    for index,pin in enumerate(pincod_false):
        assert pincode(pin) == answer_false[index]

def test_search_vacan(test_info):
    pincod_true = ['005', '008']
    pincod_false = ['asdasda', '32r345']
    answer_false = []
    
    for index,pin in enumerate(pincod_true):
        assert search_vacan(test_info['test_info'], pin) == test_info["answer_true"][index]
    for index,pin in enumerate(pincod_false):
        assert search_vacan(test_info["test_info"], pin) == answer_false

def test_get_use_code():
    user = {'anketa':[{"pincode": "000-000"},{"pincode": "002-001"},{"pincode": "200-070"}]}
    pincod_true = ['000-000','002-001','200-070']
    pincod_false = ['223424','111-2222','asdfsd']
    for pin in pincod_true:
        assert get_use_code(user,pin) == True
    for pin in pincod_false:
        assert get_use_code(user,pin) == False
