import os
import pickle
from shutil import copyfile


def load_file(file):
    try:
        file = f'data\\database_{file}.data'
        if os.path.isfile(file) and os.path.getsize(file) > 0:
            with open(file, 'rb') as database:
                return pickle.load(database)
        else:
            return {}
    except EOFError:
        file = f'data\\backup_{file}.data'
        if os.path.isfile(file) and os.path.getsize(file) > 0:
            with open(file, 'rb') as database:
                return pickle.load(database)
        else:
            return {}


def read_data_from_file(market):
    file = f'data\\{market}_data.txt'
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        with open(file) as input_data:
            data = input_data.read()
            data_indexes = data.split("\n")
            return data_indexes
    else:
        return {}


def save_data(file_name, data):
    # TODO zapis danych do osobnych plikow unikac trzymania wszystkiego w ramie
    with open(f'data\\database_{file_name}.data', 'wb') as file:
        pickle.dump(data, file)
        copyfile(f'data\\database_{file_name}.data', f'data\\backup_{file_name}.data')



