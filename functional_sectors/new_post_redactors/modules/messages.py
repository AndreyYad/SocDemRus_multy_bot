from ...generic.messages import new_post_template, cancel_template

MESSAGES = {
    'new_post_text' : new_post_template + 'Введите текст для поста или "нет", если изначально без него' + cancel_template,

    'new_post_headline' : new_post_template + 'Введите заголовок для поста или "нет", если изначально без него' + cancel_template,

    'new_post_picture' : new_post_template + 'Отправьте изображение для поста или "нет", если изначально без него и "не будет", если пост подразумевается без изображения.' + cancel_template,

    'new_post_in_red' : '''<a href="tg://user?id={}">{}</a> предлагает пост!

<b>Заголовок:</b> <i>{}</i>

<b>Текст:</b> <i>{}</i>
'''
}