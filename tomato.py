#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import sys
import time
import subprocess

WORK_MINUTES = 25
BREAK_MINUTES = 5


def main():
    try:
        # sys.argv 代表参数列表，当没有提供额外参数时，sys.argv 的长度为1（sys.argv[0] 存储的是被执行的 Python 脚本的文件名）
        # 执行 ./tomato.py
        if len(sys.argv) <= 1:
            print(f'🍅 tomato {WORK_MINUTES} minutes. Ctrl+C to exit')
            tomato(WORK_MINUTES, 'It is time to take a break')
            print(f'🛀 break {BREAK_MINUTES} minutes. Ctrl+C to exit')
            tomato(BREAK_MINUTES, 'It is time to work')
        # 执行 ./tomato.py -t
        elif sys.argv[1] == '-t':
            # 区别 ./tomato.py -t 和 ./tomato.py -t <n>
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            print(f'🍅 tomato {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to take a break')
        # 执行 ./tomato.py -b
        elif sys.argv[1] == '-b':
            # 区别 ./tomato.py -b 和 ./tomato.py -b <n>
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            print(f'🛀 break {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to work')
        # 执行 ./tomato.py -h
        elif sys.argv[1] == '-h':
            help()
        # 其他情况：表明参数输入错误，直接调用 help()
        else:
            help()
    # 按下 Ctrl+c 会触发 KeyboardInterrupt 异常
    except KeyboardInterrupt:
        print('\n👋 goodbye')
    except Exception as ex:
        print(ex)
        exit(1)


def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        seconds_slot = int(left_seconds % 60)
        seconds_str = str(seconds_slot) if seconds_slot >= 10 else '0{}'.format(seconds_slot)

        countdown = '{}:{} ⏰'.format(int(left_seconds / 60), seconds_str)
        duration = min(minutes, 25)
        # 调用 progressbar 函数显示进度条
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)

    notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def notify_me(msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
            subprocess.run(['say', '-v', 'Daniel', msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
        else:
            # windows?
            # TODO: windows notification
            pass

    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== Tomato Clock ======')
    print('====== Modified:LSK ======')
    print(f'{appname}         # start a {WORK_MINUTES} minutes tomato clock + {BREAK_MINUTES} minutes break')
    print(f'{appname} -t      # start a {WORK_MINUTES} minutes tomato clock')
    print(f'{appname} -t <n>  # start a <n> minutes tomato clock')
    print(f'{appname} -b      # take a {BREAK_MINUTES} minutes break')
    print(f'{appname} -b <n>  # take a <n> minutes break')
    print(f'{appname} -h      # help')


if __name__ == "__main__":
    main()
