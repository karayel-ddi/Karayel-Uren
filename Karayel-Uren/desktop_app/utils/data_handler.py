import pandas as pd

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Date', 'Tweet Id', 'Text', 'Username'])
    df.to_csv(filename, index=False)

def load_from_csv(filename):
    return pd.read_csv(filename)