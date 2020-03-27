# All rights for this file belong to George Imedashvili <george.lifeslice@gmail.com>. Do NOT edit these comments
# You can copy this file, modify it (but don't edit these comments) and use in your own project for free

from manybots import BotsRunner
from manybots.core import NotANewBotException
import logging
import asyncio
import traceback


class AioBotsRunner(BotsRunner):
    def __init__(self, admins=tuple(), retries=0, show_traceback=False, loop=asyncio.get_event_loop()):
        super().__init__(admins, retries, show_traceback)
        self._bots = self._BotsRunner__bots
        self._bots_status = self._BotsRunner__bots_status
        self._main_bot = self._BotsRunner__main_bot
        self._admins = self._BotsRunner__admins
        self._retries = self._BotsRunner__retries
        self._show_traceback = self._BotsRunner__show_traceback
        self._bots_disptachers = {}
        self._main_dp = None
        self.loop = loop

    def add_bot(self, name, bot, dispatcher):
        """
        method for adding a bot to the concurrent runner
        :param name: bot's name for status and services, can't repeat another bot's name
        :param bot: Bot-object from aiogram
        :param dispatcher: Dispathcer-object from aiogram
        :return: None
        """
        if bot in self._bots:
            raise NotANewBotException()
        self._bots[name] = bot
        self._bots_disptachers[name] = dispatcher
        self._bots_status[name] = False

    def add_bots(self, bot_dict, dispatchers_dict):
        """
        method for adding many bots at the same time
        :param bot_dict: {name: bot} (see description of the variables in the add_bot method)
        :param dispatchers_dict: {name: dispatcher} (see description of the variables in the add_bot method)
        :return: None
        """
        for botname in bot_dict:
            try:
                self.add_bot(botname, bot_dict[botname], dispatchers_dict[botname])
            except NotANewBotException:
                logging.warning(f'{botname} wasn\'t added, caused by NotANewBotException')
                continue

    def set_main_bot(self, bot, dispatcher, status_command: str):
        """
        method for setting the main bot
        needed for getting status and failure-reports through this bot
        :param bot: Bot-object from aiogram
        :param dispatcher: Dispathcer-object from aiogram
        :param status_command: commands to get status
        :return: None
        """
        self._main_bot = bot
        self._main_dp = dispatcher

        @self.__message_handler(self._main_dp, commands=[status_command])
        async def send_status(m):
            if m.from_user.id not in self._admins:
                return
            await self._main_bot.send_message(m.chat.id, self.format_status())

    def run(self, skip_updates=False):
        """
        method to start polling, doesn't keep your program alive,
            to keep programm alive you should use asyncio.get_event_loop().run_forever()
        :param skip_updates: does your bot need to skip_updates after start? see more in aiogram documentation
        :return: None
        """
        for botname in self._bots:
            if not self._bots_status[botname]:
                print('going to poll', botname)
                asyncio.gather(*(self.__poll(botname, skip_updates), ))

    def __warn_about_fail(self, botname):
        if self._main_bot is None:
            return
        text = f'Бот {botname} отвалился!\n\n{self.format_status()}'
        if self._show_traceback:
            with open(f'{botname}_traceback.txt', 'w') as traceback_file:
                traceback_file.write(traceback.format_exc())
        for adm in self._admins:
            self.loop.create_task(self._main_bot.send_document(adm, document=f'{botname}_traceback.txt',
                                                               caption=text, parse_mode="HTML"))

    def __tell_about_restart(self, botname, local_retries):
        if self._main_bot is None:
            return
        for adm in self._admins:
            self.loop.create_task(self._main_bot.send_message(
                adm,
                "♻️ Рестарт бота " + botname +
                ". Осталось " + local_retries + " падений до необходимости рестарта приложения"
            ))

    async def __poll(self, botname, skip_updates=False):
        local_retries = self._retries
        while True:
            dp = self._bots_disptachers[botname]
            try:
                self._bots_status[botname] = True
                if skip_updates:
                    await dp.skip_updates()
                await dp.start_polling()
            except Exception:
                print('here')
                self._bots_status[botname] = False
                self.__warn_about_fail(botname)
                if local_retries > 0:
                    local_retries -= 1
                    self.__tell_about_restart(botname, local_retries)
                    continue
                dp.stop_polling()
                break

    @staticmethod
    def __message_handler(mainbot_dp, *custom_filters, commands=None, regexp=None, content_types=None,
                          state=None, run_task=None, **kwargs):

        def decorator(callback):
            filters_set = mainbot_dp.filters_factory.resolve(mainbot_dp.message_handlers,
                                                             *custom_filters,
                                                             commands=commands,
                                                             regexp=regexp,
                                                             content_types=content_types,
                                                             state=state,
                                                             **kwargs)
            mainbot_dp.message_handlers.register(mainbot_dp._wrap_async_task(callback, run_task), filters_set, index=0)
            return callback

        return decorator
