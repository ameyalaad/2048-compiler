from Game import Game
try:
    import sly
except ImportError as error:
    print("Error importing sly, please ensure you have the library installed")

def main():
    game = Game()
    game.new_game()
    game.interactive()

if __name__ == '__main__':
    main()