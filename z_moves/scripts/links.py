import z_moves.scripts.db as db

def get_links(user_id: int):
    links = None
    if not db.get_links_by_id(user_id):
        links = 'На данный момент у тебя нету созданных ссылок. Выбери следующую опцию'
    else:
        links_list = db.get_links_by_id(user_id)
        links += 'Твои ссылки: \n'
        for link_no, link in enumerate(links_list):
            links += '{0}. <i>{1}</i> - {2} - {3}\n'.format(link_no+1, link[0], link[1], link[2])

    return links

