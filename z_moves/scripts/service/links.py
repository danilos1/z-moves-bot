import z_moves.scripts.db as db

def get_links(user_id: int):
    links = ''
    if not db.get_links_by_id(user_id):
        links = 'На данный момент у тебя нету созданных ссылок. Выбери следующую опцию'
    else:
        links_list = db.get_links_by_id(user_id)
        links += 'В этом меню ты можешь добавлять ссылки на конференции, а по нужде и пароли к ним. Твои ссылки: \n'
        for link_no, link in enumerate(links_list):
            links += '{0}. <i>{1}</i> - <b>{2}</b> - {3}\n'.format(link_no+1, link[0], link[1], link[2])
            if link[3] != '':
                links += 'Код доступа: {}\n'.format(link[3])
            if link[4] != '':
                links += link[4] + '\n'

    return links

