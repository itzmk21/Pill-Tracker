PATH_OF_CONFIG: str = './config.txt'
PATH_OF_LOG: str = './log.txt'


def list_to_str_overwrite(file_name, list_name, joiner) -> None:
    with open(f'{file_name}.txt', 'w') as f:
        f.write(joiner.join(list_name))


def read_config() -> list:
    global config
    with open(PATH_OF_CONFIG) as f:
        config = f.read().split(' ')
    return config


def handle_config(list_pos, replacement, list_pos2=None, replacement2=None) -> None:
    config_ = read_config()

    config_[list_pos] = replacement
    if type(list_pos2) == int:
        config_[list_pos2] = replacement2

    list_to_str_overwrite(file_name='config', list_name=config_, joiner=' ')


def read_log() -> list:
    with open(PATH_OF_LOG) as f:
        log = f.read().split('\n\n')
    return log


def reset_txt(file_txt, reset_text) -> None:
    with open(f'{file_txt}.txt', 'w') as f:
        f.write(reset_text)
