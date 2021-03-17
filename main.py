import sys
from datetime import timedelta

from  timeloop import Timeloop

from gmocoin_bot.bot import GMOCoinBot, EBotState
from gmocoin_bot.simulator import GMOCoinBotSimulator

bot: GMOCoinBot

SIMULATION_FLG = True

tl = Timeloop()

@tl.job(interval=timedelta(minutes=50))
def extend_token():
    if not SIMULATION_FLG and bot.get_state() == EBotState.Running:
        bot.extend_token()

@tl.job(interval=timedelta(minutes=1))
def cancel_order_check():
    if not SIMULATION_FLG and bot.get_state() == EBotState.Running:
        bot.cancel_order_check()

@tl.job(interval=timedelta(minutes=5))
def update_positions():
    if not SIMULATION_FLG and bot.get_state() == EBotState.Running:
        bot.update_positions()

@tl.job(interval=timedelta(minutes=1))
def ws_connection_check():
    if not SIMULATION_FLG and bot.get_state() == EBotState.Running:
        bot.ws_check_connection()

@tl.job(interval=timedelta(minutes=1))
def check_server_status():
    if not SIMULATION_FLG:
        if bot.get_state() == EBotState.Running and bot.get_server_status() != 'OPEN':
            bot.pause()
        elif bot.get_state() == EBotState.Paused and bot.get_server_status() == 'OPEN':
            bot.run()

@tl.job(interval=timedelta(minutes=1))
def monitoring():
    bot.chart.print_candles_by_index()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python main.py <simulation_flag>")
        exit(-1)

    if sys.argv[1] == '1':
        SIMULATION_FLG = True
    elif sys.argv[1] == '0':
        SIMULATION_FLG = False

    if SIMULATION_FLG:
        print("Bot Simulation Start.")
        bot = GMOCoinBotSimulator('configs/gmobot-simulation.json')
    else:
        print("****REAL BOT START*****")
        bot = GMOCoinBot('configs/gmobot-master.json')

    tl.start(block=False)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        del bot
