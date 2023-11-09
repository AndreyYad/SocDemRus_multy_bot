from ...generic.messages import cancel_template

MESSAGES = {
    'sos_confirmation' : 'Введите(Без кавычек) "Да, я уверен, удалите меня" для подверждения намерений выйти из всех чатов СДР!' + cancel_template,

    'sos_succes' : '''Вы были исключены из всех чатов СДР.
Прощайте, товарищ!''',

    'cant_ban_owner' : 'Вас нельзя удалить из чата "<i>{}</i>", так как вы его создатель!'
}