from bot.database.db import reg_user, get_or_create_user, save_anketa

def test_reg_user(mongodb, reg_info):
    id_user = reg_info['user_id']
    user = mongodb.users.find_one({'user_id': reg_info['user_id']})
    assert user.get('reg_info') == None
    reg_user(mongodb, reg_info)
    user = mongodb.users.find_one({'user_id': id_user})
    assert user['reg_info'] == reg_info

def test_get_or_create_user(mongodb, effective_user, message):
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user_exist == None
    user = get_or_create_user(mongodb, effective_user, message)
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user == user_exist

def test_save_anketa(mongodb, anketa_data, reg_info):
	anketa_data['reg_info'] = reg_info
	user_id = anketa_data['user_id']
	user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
	assert user.get('anketa') == None
	save_anketa(mongodb, anketa_data)
	user = mongodb.users.find_one({"user_id" : user_id})
	del anketa_data['reg_info']
	del user['anketa'][0]['time']
	del anketa_data['time']
	assert user['anketa'][0] == anketa_data
