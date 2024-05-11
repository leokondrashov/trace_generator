import logging as log
import pandas as pd
import random
import string

log.basicConfig(
        level=log.INFO,
        format='(%(asctime)s) Trace generator -- [%(levelname)s] %(message)s'
    )

def load_data(path):
    return pd.read_csv(path)

def save_data(data, path):
    try:
        data.to_csv(path, index=False)
        log.info(f'Saved to {path}')
    except:
        log.warn(f'Failed to save to {path}')

def hash_generator(size):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))