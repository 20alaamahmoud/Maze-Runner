import random

import pygame.mixer
from moviepy.editor import VideoFileClip

import button

# Define colors
BEBYBLUE =(221, 230, 237)
BLUE =(39, 55, 77)
GOLD =(227,207,87)
TRANSPARENT_BLACK = (0, 0, 0, 150)


# Maze generation code
def generate_maze(width, height):
    # Initialize the maze grid
    maze = [['#' for _ in range(width)] for _ in range(height)]


    #cell positions
    def carve(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2

            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                maze[y + dy][x + dx] = ' '
                maze[ny][nx] = ' '
                carve(nx, ny)

    start_x, start_y = 1, 1
    end_x, end_y = width - 2, height - 2
    carve(start_x, start_y)
    carve(end_x, end_y)
    maze[start_y][start_x] = 'S'  # Mark the start point
    maze[end_y][end_x] = 'E'  # Mark the end point
    return maze

pygame.init() # Initialize Pygame
pygame.mixer.init() # Initialize the mixer module


# Set the width and height of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")


# Maze generation parameters
maze_width = (screen_width // 20) - 1
maze_height = (screen_height // 20) - 1
maze_cell_size = min(screen_width // maze_width, screen_height // maze_height)
maze_offset_x = (screen_width - maze_width * maze_cell_size) // 2
maze_offset_y = (screen_height - maze_height * maze_cell_size) // 2

# Generate the maze
maze = generate_maze(maze_width, maze_height)

# Video
video_path = "welcomeVideo.mp4"
video_clip = VideoFileClip(video_path)
video_clip.preview(fps=50) # Play the video

# background image
congrats_background_image = pygame.image.load("backg.jpeg")
congrats_background_image = pygame.transform.scale(congrats_background_image, (screen_width, screen_height))

# Font initialization
font = pygame.font.SysFont("Arial", 40)

# Game states
game_started = False
game_over = False
score = 0

# Button
start_img = pygame.image.load('start_btn.png').convert_alpha()
player_x = 1  #create button instances
player_y = 1

# Start Game button rectangle
button_width = start_img.get_width()
button_height = start_img.get_height()
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2

start_button = button.Button(button_width,button_height ,start_img, 0.8)
start_button.rect.center = (button_x + button_width // 2, button_y + button_height // 2)


#End the Game
intro_finished = False
while not intro_finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_finished = True

    screen.blit(congrats_background_image, (0, 0))
    pygame.display.update()

    # Check if the music has finished playing
    if pygame.mixer.music.get_busy() == 0:
        intro_finished = True

# music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1) # Play background music indefinitely

# Game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started and not game_over:
            if start_button.rect.collidepoint(event.pos):
                game_started = True
        elif event.type == pygame.KEYDOWN and game_started and not game_over:
            if event.key == pygame.K_UP:
                if player_y > 1 and maze[player_y - 1][player_x] != '#':
                    player_y -= 1
            elif event.key == pygame.K_DOWN:
                if player_y < maze_height - 2 and maze[player_y + 1][player_x] != '#':
                    player_y += 1
            elif event.key == pygame.K_LEFT:
                if player_x > 1 and maze[player_y][player_x - 1] != '#':
                    player_x -= 1
            elif event.key == pygame.K_RIGHT:
                if player_x < maze_width - 2 and maze[player_y][player_x + 1] != '#':
                    player_x += 1

    # Clear the screen
    screen.fill(BEBYBLUE)

    if not game_started:
        start_button.draw(screen)

    else:
        # Draw the maze
        for y in range(maze_height):
            for x in range(maze_width):
                cell = maze[y][x]
                rect = pygame.Rect(
                    maze_offset_x + x * maze_cell_size,
                    maze_offset_y + y * maze_cell_size,
                    maze_cell_size,
                    maze_cell_size
                )
                if cell == '#':
                    pygame.draw.rect(screen, BLUE, rect)
                elif cell == 'S':
                    pygame.draw.rect(screen, GOLD, rect)
                elif cell == 'E':
                    pygame.draw.rect(screen, GOLD, rect)

        # Draw the player
        player_rect = pygame.Rect(
            maze_offset_x + player_x * maze_cell_size,
            maze_offset_y + player_y * maze_cell_size,
            maze_cell_size,
            maze_cell_size
        )
        pygame.draw.rect(screen, GOLD, player_rect)

        # Check if the player reached the end point
        if maze[player_y][player_x] == 'E':
            game_over = True
            score += 100

            screen.blit(congrats_background_image, (0, 0))

            # Draw congratulations message
            congrats_text = font.render("Congratulations!", True, GOLD)
            congrats_rect = congrats_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
            screen.blit(congrats_text, congrats_rect)

            # Draw score message
            score_text = font.render(f"Score: {score}", True, GOLD)
            score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2+100))
            screen.blit(score_text, score_rect)

            # Draw play again message
            replay_text = font.render("Play Again? (Y/N)", True, GOLD)
            replay_rect = replay_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))
            screen.blit(replay_text, replay_rect)


    # Update the display
    pygame.display.flip()

    if game_over:
        # Ask the player to play again
        replay = False
        while not replay:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        replay = True
                        game_started = False
                        game_over = False
                        # Generate a new maze
                        maze = generate_maze(maze_width, maze_height)
                        player_x = 1
                        player_y = 1
                    elif event.key == pygame.K_n:
                        running = False
                        replay = True

# Quit the game
pygame.quit()


