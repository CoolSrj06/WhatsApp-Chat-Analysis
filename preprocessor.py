import re, pandas as pd


def preprocess(data):
    # regex to match WhatsApp exported message lines (handles M/D/YYYY or M/D/YY, 12h or 24h time, optional seconds)
    pattern = r'(?m)^(?P<date>\d{1,2}/\d{1,2}/\d{2,4}), (?P<time>\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?) - (?P<sender>[^:]+?): (?P<message>.*)'
    regex = re.compile(pattern)

    # example: parse first few messages
    messages = [m.groupdict() for m in regex.finditer(data)]
    
    df = pd.DataFrame(messages)

    # normalize whitespace in time, parse combined datetime, and extract components
    df['time_clean'] = df['time'].str.replace('\u202f', ' ').str.replace('\xa0', ' ', regex=False).str.strip()
    df['datetime'] = pd.to_datetime(df['date'].str.strip() + ' ' + df['time_clean'], dayfirst=True, errors='coerce')

    df['day']   = df['datetime'].dt.day
    df['month'] = df['datetime'].dt.month
    df['year']  = df['datetime'].dt.year
    df['time'] = df['datetime'].dt.strftime('%H:%M')
    url_pattern = r'(https?://\S+)'
    df['urls'] = df['message'].str.findall(url_pattern)

    df = df.drop(['time_clean', 'datetime', 'date'], axis=1)

    return df