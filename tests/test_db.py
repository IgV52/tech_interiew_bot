from bot.database.db import reg_user, get_or_create_user, save_anketa

def test_reg_user(mongodb, reg_info):
    user = mongodb.users.find_one({'user_id': reg_info['user_id']})
    assert user.get('reg_info') == None
    reg_user(mongodb, reg_info)
    user = mongodb.users.find_one({'user_id': reg_info['user_id']})
    del reg_info['user_id']
    assert user['reg_info'] == reg_info

def test_get_or_create_user(mongodb, effective_user, message):
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user_exist == None
    user = get_or_create_user(mongodb, effective_user, message)
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user == user_exist

def test_save_anketa(mongodb, anketa_data):
    user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
    assert user.get('anketa') == None
    save_anketa(mongodb, anketa_data)
    user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
    del anketa_data['user_id']
    del user['anketa'][0]['time']
    assert user['anketa'][0] == anketa_data
