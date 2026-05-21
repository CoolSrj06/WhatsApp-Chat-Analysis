import pandas as pd


def _filtered_chat(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    return df

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    # number of messages
    num_messages = df.shape[0]

    # total words 
    df['word_count'] = df['message'].str.split().apply(len)
    total_words = df['word_count'].sum()

    # total media messages
    media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # total message deleted
    deleted_messages = df[df['message'] == 'This message was deleted'].shape[0]
    
    return num_messages, total_words, media_messages, deleted_messages

def month_chat_frequency(df):
    monthly_chat = df.groupby(['year', 'month']).size().reset_index(name='message_count')
    monthly_chat['date'] = pd.to_datetime(monthly_chat[['year', 'month']].assign(day=1))
    monthly_chat = monthly_chat.sort_values('date')
    monthly_chat['year_month'] = monthly_chat['date'].dt.strftime('%B %Y')

    return monthly_chat[['date', 'year_month', 'message_count']]

def top_10_most_active_month(df):
    monthly_chat = month_chat_frequency(df)
    top_months = (
        monthly_chat
        .sort_values('message_count', ascending=False)
        .head(10)
        .sort_values('date')
    )
    return top_months

def most_active_days_of_week(df):
    date_series = pd.to_datetime(df[['year', 'month', 'day']])
    active_days = date_series.dt.day_name().value_counts().reset_index()
    active_days.columns = ['day_of_week', 'message_count']

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    active_days['day_of_week'] = pd.Categorical(active_days['day_of_week'], categories=day_order, ordered=True)
    return active_days.sort_values('day_of_week')

def heatmap_data(df):
    heatmap_df = df.copy()
    heatmap_df['day_of_week'] = pd.to_datetime(heatmap_df[['year', 'month', 'day']]).dt.day_name()
    heatmap_df['hour'] = pd.to_datetime(heatmap_df['time'], format='%H:%M', errors='coerce').dt.hour

    heatmap_data = (
        heatmap_df
        .groupby(['day_of_week', 'hour'])
        .size()
        .unstack(fill_value=0)
        .reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    )

    return heatmap_data

def wordcloud_data(df, selected_user='Overall'):
    from wordcloud import WordCloud
    excluded_messages = ["<Media omitted>", "This message was deleted", "POLL:", "You deleted this message"]
    filtered_messages = _filtered_chat(df, selected_user)
    filtered_messages = filtered_messages[~filtered_messages['message'].isin(excluded_messages)].copy()
    filtered_messages['message'] = (filtered_messages['message']
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )
    filtered_messages = filtered_messages[filtered_messages['message'] != '']
    if filtered_messages.empty:
        all_messages = 'No messages available'
    else:
        all_messages = ' '.join(filtered_messages['message'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_messages)
    
    return wordcloud

def most_common_messages(df, selected_user='Overall', n=20):
    excluded_messages = [
        "<Media omitted>",
        "This message was deleted",
        "POLL:",
        "You deleted this message"
    ]

    filtered_messages = _filtered_chat(df, selected_user).copy()

    # Convert to lowercase for consistent filtering
    filtered_messages['message'] = filtered_messages['message'].str.lower()

    # Remove unwanted messages
    excluded_messages = [msg.lower() for msg in excluded_messages]

    filtered_messages = filtered_messages[
        ~filtered_messages['message'].isin(excluded_messages)
    ]

    # Clean text
    filtered_messages['message'] = (
        filtered_messages['message']
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    # Remove empty messages
    filtered_messages = filtered_messages[
        filtered_messages['message'] != ''
    ]

    if filtered_messages.empty:
        return pd.DataFrame(columns=['message', 'count'])

    # Count full messages
    message_counts = (
        filtered_messages['message']
        .value_counts()
        .head(n)
        .reset_index()
    )

    message_counts.columns = ['message', 'count']

    return message_counts

def emoji_analysis(df, selected_user='Overall'):
    import emoji
    from collections import Counter

    def extract_emojis(text):
        return [char for char in text if char in emoji.EMOJI_DATA]

    filtered_messages = _filtered_chat(df, selected_user).copy()
    filtered_messages['emojis'] = filtered_messages['message'].apply(extract_emojis)
    all_emojis = [emoji for sublist in filtered_messages['emojis'] for emoji in sublist]
    if not all_emojis:
        return pd.DataFrame(columns=['emoji', 'count'])
    emoji_counts = Counter(all_emojis).most_common(20)
    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])
    
    return emoji_df.head(10)