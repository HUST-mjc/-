import pygame
import sys
import random
import tkinter as tk

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('一起努力，用爱发电~')
hei  = pygame.font.SysFont("SimHei", 32)
hei_s = pygame.font.SysFont("SimHei", 24)

white = (255, 255, 255)
avatar_size = 200
avatar_lian  = pygame.transform.scale(pygame.image.load("害羞.png"),   (avatar_size, avatar_size))
avatar_youyi = pygame.transform.scale(pygame.image.load("暗中观察.png"), (avatar_size, avatar_size))

# 每局状态
class GameState:
    def __init__(self):
        self.reset()
    def reset(self):
        self.mi = 0
        self.ma = 280
        self.bomb = random.randint(0, 280)
        self.current_player = 1      # 1 梨安  2 又一
        self.game_over = False
        self.winner = None
        self.input_text = ""         # 当前输入的数字串
state = GameState()

def draw_scene():
    DISPLAYSURF.fill(white)
    if state.game_over:
        # 爆炸画面
        exp = pygame.transform.scale(pygame.image.load("exposure.jpg"), (300, 400))
        DISPLAYSURF.blit(exp, (100, 100))
        print_text(hei, 100, 50, "BOMB !!!", (255, 0, 0))
    else:
        # 气球（固定大小即可，仅作装饰）
        balloon = pygame.transform.scale(pygame.image.load("balloon.jpg"), (150, 213))
        DISPLAYSURF.blit(balloon, (100, 100))

    # 当前玩家头像
    avatar = avatar_lian if state.current_player == 1 else avatar_youyi
    DISPLAYSURF.blit(avatar, (800, 200))

    # 区间提示
    print_text(hei_s, 600, 80, f"当前区间：{state.mi} ~ {state.ma}", (0, 0, 255))
    prompt = "轮到 梨安 pupu" if state.current_player == 1 else "轮到 又一 打嗝"
    print_text(hei_s, 600, 110, prompt, (0,128,0))
    # 输入框
    print_text(hei_s, 600, 140, f"输入：{state.input_text}", (50, 50, 50))
    print_text(hei_s, 600, 180, "回车确认  ← 退格", (100, 100, 100))

    pygame.display.update()

def print_text(font, x, y, text, color=(0, 0, 0)):
    DISPLAYSURF.blit(font.render(text, True, color), (x, y))

def message_box(winner):
    root = tk.Tk()
    root.title("游戏结束")
    root.geometry('300x150+500+300')
    root.configure(bg='white')
    tk.Label(root, text=f"{winner} 获胜！", bg='white', font='hei 14').pack()
    tk.Button(root, text='再来一局', bg='gray', command=lambda: (root.destroy(), state.reset())).pack(pady=20)
    root.mainloop()

# 主循环
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state.game_over:
            continue  # 等 tk 窗口关闭后重置

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state.input_text = state.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if state.input_text == "":
                    continue
                try:
                    val = int(state.input_text)
                except ValueError:
                    state.input_text = ""
                    continue

                if val <= state.mi or val >= state.ma:
                    # 越界，继续输入
                    continue
                if val == state.bomb:
                    state.game_over = True
                    state.winner = "又一" if state.current_player == 1 else "梨安"
                    draw_scene()
                    message_box(state.winner)
                else:
                    if val < state.bomb:
                        state.mi = val
                    else:
                        state.ma = val
                    state.current_player = 3 - state.current_player  # 1↔2
                    state.input_text = ""
            elif event.unicode.isdigit():
                state.input_text += event.unicode

    draw_scene()
    clock.tick(30)