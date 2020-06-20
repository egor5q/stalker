import config
from botutil import BotUtil

bot = BotUtil(config.environ['TELEGRAM_TOKEN'], config.admins[1])
if 'DYNO' in config.environ:
    heroku = True
    bot.report('Heroku initialization...')
else:
    heroku = False
    bot.report('Local initialization...')

from timeit import default_timer as timer
start_time = timer()

from manybotslib import BotsRunner
import hi
import wen
import steal_zhabka

bots_to_start = {
    'Hi': hi.bot,
    'Wen': wen.bot,
    'Жабка':steal_zhabka.bot
}

runner = BotsRunner(admins=config.admins, show_traceback=True)
runner.add_bots(bots_to_start)
runner.set_main_bot(hi.bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.\nВремени использовано: {} секунд.'.format(timer() - start_time))
runner.run()
