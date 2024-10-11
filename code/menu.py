import pygame, sys
from button import Button
from main import Game

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Hình nền
BG = pygame.image.load("images/assets/Background.png")

# Hàm lấy font
def get_font(size):  # Trả về font với kích thước mong muốn
    return pygame.font.Font("images/assets/font.ttf", size)

# Hàm chính của menu
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        # Vị trí chuột
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Văn bản tiêu đề menu
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Tạo nút "Play" và "Quit"
        PLAY_BUTTON = Button(image=pygame.image.load("images/assets/Play Rect.png"), pos=(640, 300), 
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/assets/Quit Rect.png"), pos=(640, 500), 
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Hiển thị tiêu đề menu
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Cập nhật và hiển thị các nút
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Xử lý các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game = Game()  # Tạo đối tượng game từ main.py
                    game.run()  # Bắt đầu game
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Cập nhật màn hình
        pygame.display.update()

# Chạy hàm menu
main_menu()
