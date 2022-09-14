import json


def load_from_json(path):
    """
    Возвращает список из файла json
    """
    with open(path, 'r', encoding='utf-8') as file:
        list_users = json.load(file)
        file.close()
    return list_users


def find_next_id(path):
    """
    Возвращает id для нового пользователя
    :param path:
    :return: id
    """
    with open(path, 'r', encoding='utf-8') as file:
        list_users = json.load(file)
        file.close()
    next_id = list_users[-1]['id'] + 1
    return next_id


def write_in_file(path, new_user):
    with open(path, "r", encoding='utf-8') as read_file:
        list_user = json.load(read_file)
        list_user.append(new_user)
        read_file.close()
    with open(path, "w", encoding='utf-8') as file:
        json.dump(list_user, file)
        file.close()


def change_by_id(path, new_data, gid):
    with open(path, "r", encoding='utf-8') as read_file:
        list_user = json.load(read_file)
        new_list = []
        for user in list_user:
            if user['id'] != gid:
                new_list.append(user)
            else:
                pass
        new_list.append(new_data)
        read_file.close()
    with open(path, "w", encoding='utf-8') as file:
        json.dump(new_list, file)
        file.close()


def delete_by_id(path, gid):
    with open(path, "r", encoding='utf-8') as read_file:
        list_user = json.load(read_file)
        new_list = []
        for user in list_user:
            if user['id'] != gid:
                new_list.append(user)
            else:
                pass
        read_file.close()
    with open(path, "w", encoding='utf-8') as file:
        json.dump(new_list, file)
        file.close()


#path = './data/test.json'
#print(find_next_id(path))
