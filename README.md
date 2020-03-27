# aiomanybots
Library for running bots concurrently on aiogram, 
based on https://github.com/Senderman/manybotslib

###Installation:
    `pip istall e git://github.com/drforse/aiogram_many_bots_lib#egg=aiomanybots`
###Uninstallation:
    `pip uninstall aiomanybots`

###Examples
Look for examples in /examples

###Падения
При падении одного из ботов, все админы приложения получат уведомление о падении, а так же кол-во оставшихся рестартов бота, и, в зависимости от начальной конфигурации, стектрейс. Уведомления приходят от "главного" бота, которого необходимо задать. Менять главного бота можно в любое время в функцию назначения главного бота необходимо передать команду, при получении которой бот будет отправлять админу статус работы всех ботов Бот не отправит статус, если админы не были назначены либо команду вызвал не админ

Eсли главного бота не задать, уведомления работать не будут!

runner.set_main_bot(admin_bot, 'status')

###Статус работы ботов
В любой момент можно получить как словарь {string: boolean} о работе ботов, где ключ - имя бота, значение - true, если работает, false, если отключен, обративщись к полю bots_status:

status = runner.get_status()

Кроме того, можно получить красиво отформатированную информацию о статусе всех ботов:

status_text = runner.format_status()

######TODO:
[ ] метод для вытягивания логов с хероку