cancel_template = '\n\n/cancel - отмена'
new_post_template = '<b>Предложение поста</b>\n\n'

MESSAGES = {
    'start' : '''Привет, товарищ!
Это многофункционый бот СДР!''',

    'reset' : 'Сброс',

    'anonim_msg_info' : '''Напишите сообщение с предложением или жалобой для ОргКомитета
Оно будет отправленно анонимно''' + cancel_template,

    'sos_confirmation_1' : 'Введите(Без кавычек) "Да, я уверен, удалите меня" для подверждения намерений выйти из всех чатов СДР!' + cancel_template,

    'sos_confirmation_2' : 'Введите чему равняется это выражение: "{}", для подверждения намерений выйти из всех чатов СДР!' + cancel_template,

    'sos_succes' : '''Вы были исключены из всех чатов СДР.
Прощайте, товарищ!''',

    'new_post_text' : new_post_template + 'Введите текст для поста или "нет", если изначально без него' + cancel_template,

    'new_post_headline' : new_post_template + 'Введите заголовок для поста или "нет", если изначально без него' + cancel_template,

    'new_post_picture' : new_post_template + 'Отправьте изображение для поста или "нет", если изначально без него и "не будет", если пост подразумевается без изображения.' + cancel_template,

    'new_post_in_red' : '''<a href="tg://user?id={}">{}</a> предлагает пост!

<b>Заголовок:</b> {}

<b>Текст:</b> {}
'''
}