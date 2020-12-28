from .release import TmCreator

if __name__ == "__main__":
    unx_source = input('Enter UNX file: ')
    tmx_interpreter = input('Enter interpreter TMX file: ')
    result = TmCreator(tmx_interpreter).createTmForUnxFile(unx_source)
    print(f"Turing machine has {len(result.states)} states excluding halt states")