from bot.database.db import reg_user, get_or_create_user, save_anketa, get_or_create_job, info_vacan_in_company, check_company

def test_reg_user(mongodb, reg_info):
    reg_info['user_id'] = 12121213
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
    anketa_data['user_id'] = 12121213
    user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
    assert user.get('anketa') == None
    save_anketa(mongodb, anketa_data)
    user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
    del anketa_data['user_id']
    del user['anketa'][0]['time']
    assert user['anketa'][0] == anketa_data

def test_update_save_anketa(mongodb, anketa_data):
    anketa_data['user_id'] = 1212121
    user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
    assert len(user['anketa']) == 1
    save_anketa(mongodb, anketa_data)
    user = mongodb.users.find_one({"user_id" : anketa_data['user_id']})
    assert len(user['anketa']) == 2

def test_get_or_create_job(mongodb, file_vacancy):
    job = mongodb.jobs.find_one({'company' : file_vacancy['company']})
    assert job == None
    job = get_or_create_job(mongodb, file_vacancy)
    assert bool(job) == True
    assert job['vacancy'][0] == file_vacancy['vacancy']
    assert job['company'] == file_vacancy['company']
    assert job['pincode'] == file_vacancy['pincode']
    result = get_or_create_job(mongodb, file_vacancy)
    assert result == None
    job = mongodb.jobs.find_one({'company' : file_vacancy['company']})
    assert len(job['vacancy']) == 1
    file_vacancy["vacancy"]["pincode"] = "001"
    get_or_create_job(mongodb, file_vacancy)
    job = mongodb.jobs.find_one({'company' : file_vacancy['company']})
    assert len(job['vacancy']) == 2

def test_info_vacan_in_company(mongodb):
    pincode = ["000", "000"]
    fake_pincode = ["001", "000"]
    job = info_vacan_in_company(mongodb, pincode)
    assert bool(job) == True
    job = info_vacan_in_company(mongodb, fake_pincode)
    assert bool(job) == False

def test_check_company(mongodb):
    company = "Первое знакомство"
    fake_company = "Сбер"
    info = check_company(mongodb, company)
    assert info[0] == True
    assert info[1]['pincode'] == "000"
    assert len(info) == 2
    info = check_company(mongodb, fake_company)
    assert info[0] == False
    assert len(info) == 1











