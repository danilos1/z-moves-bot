from z_moves.hyperlink_format import HL

hotlines = '''\
👺 Hotlines: 
КМ — Лаб №4 — 29.11''' + HL.format(link='https://classroom.google.com/c/MTUzMzM3OTA3NTEy/a/MTQ2MDc3NDgwMTM3/details?cjc=gvqmu7i', text=' ℹ') + '''
СП — КР — 01.12''' + '''
ОПП — СР — 02.12''' + HL.format(link='https://t.me/c/1164069874/209974', text=' ℹ') + '''
English — Рек. контр. — 16:15 03.12''' + HL.format(link='https://t.me/c/1269944628/1029', text=' ℹ') + '''
КС — КР — 09.12''' + '''
КМ — Лаб №5 — 19.12''' + HL.format(link='https://classroom.google.com/c/MTUzMzM3OTA3NTEy/a/MTQ2MDc3NDgwMjE4/details?cjc=gvqmu7i', text=' ℹ')

hyperlink_format = '<a href="{link}">{text}</a>'
hyperlink_format.format(link='http://foo/bar', text='linky text')

