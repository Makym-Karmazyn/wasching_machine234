"""Симулятор пральної машинки за допомогою pyglet --by Karmazyn Maksym--"""

import time
import random

import pyglet
from pyglet import window
from pyglet.window import key
from pyglet import gl

from data_base import NewUser

# Параметри вікна
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700

# Initialize the windowСтворення вікна
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

#Глобальні змінні
input_text = ""
input_text2 = ""
time_wash = ""
mode = ""
time_wash1 = None
mode1 = ""
stage = 0
program_stage = 0
answer = None
time_escape = 0
error_log = "input your name after press 'Enter', input password and press 'Enter' agin"
random_number = None
random_mode = None
timer_work = False

#Фото та звуки
start_img = pyglet.image.load('sound_photo/start_btn2.jpg')

start_sprite = pyglet.sprite.Sprite(start_img,
                                    x=window.width // 2 - 185,
                                    y=window.height // 2 - 110)
start_sprite.scale = 0.5

machine_sound = pyglet.media.load('sound_photo/macine_sound_1.mp3')
machine_signal = pyglet.media.load('sound_photo/signal.mp3')
fail = pyglet.media.load('sound_photo/fail.mp3')
victory = pyglet.media.load('sound_photo/win.mp3')

base_machine = pyglet.image.load('sound_photo/base_machine.jpg')
base_machine_sprite = pyglet.sprite.Sprite(base_machine,
                                           x=window.width // 2 - 1000,
                                           y=window.height // 2 - 530)

broke_machine1 = pyglet.image.load('sound_photo/broken.jpg')
broke_machine = pyglet.sprite.Sprite(broke_machine1,
                                     x=window.width // 2 - 300,
                                     y=window.height // 2 - 530)

clean_machine = pyglet.image.load('sound_photo/clean.jpg')
clean_machine1 = pyglet.sprite.Sprite(clean_machine,
                                      x=window.width // 2 - 300,
                                      y=window.height // 2 - 430)

start_washing = pyglet.image.load('sound_photo/start_washing.jpg')
start_washing_sprite = pyglet.sprite.Sprite(start_washing,
                                            x=window.width // 2 + 480,
                                            y=window.height // 2 + 140)


machine_gif = pyglet.image.load_animation('sound_photo/machine.gif')
gif_animation = pyglet.image.Animation.from_image_sequence(machine_gif.frames, duration=0.1)
machine_gif_sprite = pyglet.sprite.Sprite(machine_gif,
                                          x=window.width // 2 - 1000,
                                          y=window.height // 2 - 530)
#Функції для нажимання кнопок за допомогою миші
@window.event
def on_mouse_press(x, y, button, modifiers):
    global program_stage,input_text, input_text2, stage,\
        program_stage,password,us_name,time_wash,mode,time_wash1,mode1
    if program_stage == 4:
        if (start_sprite.x - 20 <= x <= start_sprite.x + start_sprite.width * start_sprite.scale + 115 and
            start_sprite.y <= y <= start_sprite.y + start_sprite.height * start_sprite.scale + 45):
            print("Кнопка натиснута!")
        program_stage = 5
    elif program_stage == 5 or program_stage == 7:
        if (start_washing_sprite.x - 20 <= x <= start_washing_sprite.x + start_washing_sprite.width * start_washing_sprite.scale + 115 and
            start_washing_sprite.y <= y <= start_washing_sprite.y + start_washing_sprite.height * start_washing_sprite.scale + 45):
            print("Кнопка пралка!")
            if program_stage == 5:
                time_wash1 = time_wash
                mode1 = mode
                mode = ""
                time_wash = ""
                program_stage = 6
            else:
                program_stage = 9
        print(f"click program stage: {program_stage}")

# Функції клавіатури для введення даних наприклад для входу чи для введення часу та режиму
@window.event
def on_key_press(symbol, modifiers):
    global input_text, input_text2, stage, program_stage,password,us_name,time_wash,mode,time_wash1,mode1
    if program_stage == 0:
        if stage == 0:
            if symbol == key.ENTER:
                stage = 1
            elif symbol == key.BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 20:
                    input_text += chr(symbol)
        else:
            if symbol == key.ENTER:
                password = input_text2
                us_name = input_text
                stage = 0
                input_text = ""
                input_text2 = ""
                program_stage = 1
            elif symbol == key.BACKSPACE:
                input_text2 = input_text2[:-1]
            else:
                if len(input_text2) < 30:
                    input_text2 += chr(symbol)
    else:
        if stage == 0:
            if symbol == key.ENTER:
                stage = 1
            elif symbol == key.BACKSPACE:
                time_wash = time_wash[:-1]
            else:
                if len(time_wash) < 3:
                    time_wash += chr(symbol)
        else:
            if symbol == key.ENTER:

                stage = 0
            elif symbol == key.BACKSPACE:
                mode = mode[:-1]
            else:
                if len(mode) < 11:
                    mode += chr(symbol)

#Функція start_timer запускає функцію update_timer яка буде оновлюватися кожної секунди
def start_timer(time,new_stage):
    global time_escape, program_stage,timer_started
    time_escape = time
    pyglet.clock.schedule_interval(update_timer, 1,new_stage)

#функція update timer запускається за допомогою функції start_timer і оновлюється кожної секунди
# віднімаючи від time_escape 1 і коли time_escape буде менше 1 то таймер припеняє оновлюватися
#і перекидає користувача на задану завчасно сторінку:program_stage = new_stage
def update_timer(dt, new_stage):
    global time_escape, program_stage
    if program_stage != 5 and program_stage != 7:
        if time_escape > 1:
            time.sleep(.1)
            time_escape -= 1
        else:
            time_escape = 0
            pyglet.clock.unschedule(update_timer)
            program_stage = new_stage


#Тут відображаються всі функції та сторінки
@window.event
def on_draw():
    global program_stage, input_text,clean_machine1, input_text2, answer, time_escape,password,us_name,error_log,time_wash,mode,broke_machine,time_wash1,mode1,random_number, random_mode, machine_signal
    window.clear()

    #program_stage == 0: вхід в аккаунт
    if program_stage == 0:
        label = pyglet.text.Label("Your name: " + input_text,
                                  font_name='Arial',
                                  font_size=24,
                                  x=70,
                                  y=500)
        label1 = pyglet.text.Label("Password: " + input_text2,
                                   font_name='Arial',
                                   font_size=24,
                                   x=70,
                                   y=300)
        red = (255, 0, 0, 255)
        error_label = pyglet.text.Label("" + error_log,
                                   font_name='Arial',
                                   font_size=19,
                                   color=red,
                                   x=70,
                                   y=150)
        error_label.draw()
        label.draw()
        label1.draw()

    #program_stage == 1 та program_stage == 3: превірка чи ввійшов користувач якщо користувач ввійшов перенаправляє на program_stage = 2 якщо ні то наprogram_stage = 0
    elif program_stage == 1:
        answer = NewUser(us_name,password)
        program_stage = 3
    elif program_stage == 3:
        if answer == "I'm sorry, but this name is prematurely used, or you input incorrect password.\nTry agin":
            error_log = "I'm sorry, but this name is prematurely used, or you input incorrect password.\nTry agin"
            program_stage = 0
        else:

            program_stage = 2

    #program_stage == 2: Таймер та перенесення на program_stage == 4:
    elif program_stage == 2:
        log_res = pyglet.text.Label(answer,
                                    font_name='Arial',
                                    font_size=30,
                                    x=window.width // 2,
                                    y=window.height // 2,
                                    anchor_x='center', anchor_y='center')
        log_res.draw()
        if time_escape == 0:
            start_timer(4, 4)

            # Відображення таймера
        if time_escape > 0:
            timer_label = pyglet.text.Label(f'Time left: {time_escape}',
                                            font_name='Arial',
                                            font_size=30,
                                            x=window.width // 2,
                                            y=window.height // 2 - 50,
                                            anchor_x='center', anchor_y='center')
            timer_label.draw()

    #program_stage == 4: коротко про симулятор та перенесення на program_stage == 5 якщо нажати на кнопку

    elif program_stage == 4:
        welcome_label = pyglet.text.Label("The washing machine stimulate",
                                        font_name='Arial',
                                        font_size=39,
                                        x=window.width // 2 ,
                                        y=window.height // 2 + 280,
                                        anchor_x='center', anchor_y='center')

        info_label = pyglet.text.Label(f'This is a washing machine simulator that simulates the sounds, movements of turning on and off the washing machine, washing modes and their duration. You will also need to complete tasks.\nSoooooooooooo good luck in this exciting simulator',
                                                font_name='Arial',
                                                font_size=20,
                                                width=600,
                                                multiline=True,
                                                x=window.width // 2,
                                                y=window.height // 2 +130,
                                                anchor_x='center', anchor_y='center')

        info_label.draw()
        welcome_label.draw()
        start_sprite.draw()

    #program_stage == 5: Основна сторінка з пральною на якій потрібно ввести значення які тобі надають та нажати на кнопку
    #щоб запустити прання або ж зламати машинку
    elif program_stage == 5:
        gl.glClearColor(0.0, 0.749, 0.678, 1.0)
        if random_number == None and random_mode == None:
            random_number = random.randint(10, 30)
            random_mode = random.choice(["rinsing", "spin", "classic"])

        washing_task = pyglet.text.Label(
            f'do a wash that will last "{random_number}" seconds and in the "{random_mode}" mode',font_name='Arial',font_size=40,
            width=1100,
            multiline=True,
            x=window.width // 2 - 600,
            y=window.height // 2 + 290, )

        washing_task3 = pyglet.text.Label(
            f'you can switch between "time" and "mode" using the "enter" key',font_name='Arial',font_size=27,
            width=1100,
            multiline=True,
            x=window.width // 2 - 600,
            y=window.height // 2 + 160, )
        washing_time_inp = pyglet.text.Label(
            f'time:' + time_wash,
            font_name='Arial',
            font_size=34,
            width=600,
            multiline=True,
            x=window.width // 2 - 70,
            y=window.height // 2 - 130, )
        washing_regime_inp = pyglet.text.Label(
            f'mode:' + mode,
            font_name='Arial',
            font_size=34,
            width=600,
            multiline=True,
            x=window.width // 2 - 70,
            y=window.height // 2 - 230, )
        start_washing_sprite.scale = 0.4
        base_machine_sprite.scale = 1
        start_washing_sprite.draw()

        base_machine_sprite.draw()
        washing_regime_inp.draw()
        washing_time_inp.draw()
        washing_task.draw()
        washing_task3.draw()

    #program_stage == 6: Сторінка миття з відтворенням звуку та відео пралки по закінченню таймера викликається program_stage == 7:
    elif program_stage == 6:

        time_wash = ""
        mode = ""
        stage = 0
        try:
            if mode1 == random_mode and int(time_wash1) == int(random_number):
                gl.glClearColor(0.0, 0.749, 0.678, 1.0)

                washing_task1 = pyglet.text.Label(
                        f'Washing...',
                        font_name='Arial',
                        font_size=40,
                        width=600,
                        multiline=True,
                        x=window.width // 2 - 600,
                        y=window.height // 2 + 290, )

                washing_mode = pyglet.text.Label(
                        mode1,
                        font_name='Arial',
                        font_size=40,
                        width=600,
                        multiline=True,
                        x=window.width // 2 - 600,
                        y=window.height // 2 + 220, )
                if time_escape == 0:
                    start_timer(int(time_wash1), 7)

                    # Відображення таймера
                if time_escape > 0:
                    washing_time1 = pyglet.text.Label(f"{time_escape} /  {random_number}",
                            font_name='Arial',
                            font_size=40,
                            width=600,
                            multiline=True,
                            x=window.width // 2 - 600,
                            y=window.height // 2 + 150, )
                    program_stage = 6
                start_washing_sprite.scale = 0.4
                machine_gif_sprite.scale = 1.1
                start_washing_sprite.draw()
                washing_task1.draw()
                washing_time1.draw()
                washing_mode.draw()

                machine_sound.play()

                machine_gif_sprite.draw()
            else:
                program_stage = 8


        except:
            print("exeptddddddddddddddddddddddddddd")
            program_stage = 8


    #program_stage == 8: Якщо ти ввів неправельне значиня то активується ця сторінка з зламаною пральною машинкою
    #по закінчені таймера переносить на program_stage == 5: основна сторінка
    elif program_stage == 8:
        gl.glClearColor(1, 1, 1, 1)
        black = (0, 0, 0, 255)
        washing_task1 = pyglet.text.Label(
            f'Whoops, it looks like you broke the washing machine by entering the wrong values, try again but with the values that the program gave you',
            font_name='Arial',
            font_size=30,
            width=500,
            multiline=True,
            x=window.width // 2 - 600,
            y=window.height // 2 + 290, color=black)
        washing_task2 = pyglet.text.Label(
            f'Machine repair...',
            font_name='Arial',
            font_size=34,
            width=600,
            multiline=True,
            x=window.width // 2 + 110,
            y=window.height // 2 + 280, color=black)
        if time_escape == 0:
            start_timer(18, 5)

        if time_escape > 0:
            timer_label1 = pyglet.text.Label(f'Time to repair: {time_escape}',
                                             font_name='Arial',
                                             font_size=30,
                                             x=window.width // 2 + 110,
                                             y=window.height // 2 + 240, color=black)

        broke_machine.scale = 1.5
        broke_machine.draw()
        washing_task1.draw()
        washing_task2.draw()
        timer_label1.draw()

    #program_stage == 7: викликається при закінченні прання супроводжується звуковими ефектами, якщо нажати
    #на кнопку викличиться program_stage == 9:
    elif program_stage == 7:
        random_number = None
        random_mode = None
        gl.glClearColor(0.0, 0.749, 0.678, 1.0)

        washing_task = pyglet.text.Label(
            f'Turn off the washing machine',
            font_name='Arial',
            font_size=40,
            width=600,
            multiline=True,
            x=window.width // 2 - 600,
            y=window.height // 2 + 290, )

        start_washing_sprite.scale = 0.4
        base_machine_sprite.scale = 1.1
        start_washing_sprite.draw()
        washing_task.draw()
        base_machine_sprite.draw()
        # washing_regime_inp.draw()
        # washing_time_inp.draw()
        machine_signal.play()

        washing_task.draw()

    #program_stage == 9: фінальна сторінка в якій тебе вітають з виконаним пранням і по закінченні таймера переносять на program_stage == 5:
    elif program_stage == 9:
        gl.glClearColor(1, 1, 1, 1)
        black = (0, 0, 0, 255)
        washing_task1 = pyglet.text.Label(
            f'Congratulations, you have successfully clean clothes',
            font_name='Arial',
            font_size=30,
            width=500,
            multiline=True,
            x=window.width // 2 - 650,
            y=window.height // 2 + 290, color=black)

        if time_escape == 0:
            start_timer(8, 5)

        if time_escape > 0:
            timer_label1 = pyglet.text.Label(f'time to transfer: {time_escape}',
                                             font_name='Arial',
                                             font_size=30,
                                             x=window.width // 2 - 650,
                                             y=window.height // 2 + 150, color=black)

        clean_machine1.scale = 1.5
        clean_machine1.draw()
        washing_task1.draw()
        timer_label1.draw()

        # washing_regime_inp.draw()
        # washing_time_inp.draw()

#Запуск
pyglet.app.run()

# сумарна робота над проектом десь 18 - 19 год