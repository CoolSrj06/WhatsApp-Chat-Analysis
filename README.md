# WhatsApp Chat Analysis

A small Python project to preprocess and analyze exported WhatsApp chat files. It provides utilities to compute message statistics, generate word clouds, analyze emoji usage, and create time-based activity summaries.

## Features

- Compute basic stats: message counts, word counts, media and deleted messages.
- Monthly and daily activity summaries and heatmap-ready data.
- Word cloud generation and most-common message extraction.
- Emoji frequency analysis.


# WhatsApp Chat Analysis

Analyze WhatsApp exports quickly — either via the hosted Streamlit demo or locally.

**Live demo:** https://whatsapp-chat-analysis-by-srj.streamlit.app/

## What this project does

- Parses exported WhatsApp `.txt` chat files and converts them into a structured `pandas.DataFrame`.
- Provides analytics: message counts, word counts, media/deleted message counts, most-active months/days/hours, emoji frequency, most-common messages, and word clouds.
- Includes a Streamlit UI (`app.py`) so non-technical users can upload a chat and explore visualizations.

## Live Hosted App (recommended)

Use the hosted Streamlit demo to analyze chats without installing anything locally:

- Visit: https://whatsapp-chat-analysis-by-srj.streamlit.app/
- Upload an exported `.txt` chat file (see "Exporting chats from WhatsApp" below).
- Choose a user to filter (or select "Overall").
- Explore interactive panels: summary stats, time-series charts, heatmap, word cloud, most-common messages, and emoji analysis.

The hosted app provides the easiest way to try the project and share results.

## Demo Video

Watch a short demonstration of this project below:

<iframe width="560" height="315" src="https://www.youtube.com/embed/MxEoWaaoqPw" title="WhatsApp Chat Analysis Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Run locally

1. Clone the repository or place the project folder on your machine.
2. Create a virtual environment (recommended) and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

3. Start the Streamlit app locally:

```bash
streamlit run app.py
```

4. In the opened browser window, upload a WhatsApp exported `.txt` file and use the UI just like the hosted version.

## Quick Tour — How to use the app

- Upload: Click the file upload area and select an exported WhatsApp `.txt` file.
- Parse: The app runs the `preprocess()` function to parse messages into a DataFrame.
- Select scope: Choose a specific participant or `Overall` to analyze the whole chat.
- View Summary: Top-left (or summary panel) shows basic stats: number of messages, total words, media messages, and deleted messages.
- Time Analysis: Monthly and daily charts visualize activity over time.
- Heatmap: Shows activity by day-of-week and hour-of-day.
- Word Cloud: Visualizes the most frequent words (common placeholders and deleted/media messages are excluded).
- Most-common messages & Emoji Analysis: Lists the top repeated messages and most-used emojis.
- Export/Save: Use your browser or Streamlit options to save plots or copy results as needed.

## Exporting chats from WhatsApp

You can export chats from WhatsApp into a text file and use that exported `.txt` as input to this project. Steps to export:

- Open WhatsApp and select the chat (individual or group) you want to export.
- Access Export Options:
    - iPhone: Tap the contact or group name at the top of the screen, then scroll and select "Export Chat".
    - Android: Tap the three-dot menu in the top-right, choose "More", then select "Export chat".
- Choose whether to include media:
    - With Media: Includes photos and videos (larger file size).
    - Without Media: Exports only text messages (smaller, quicker to transfer).
- Select a sharing/saving method (email, Google Drive, iCloud, etc.) to save the exported `.txt` file to your device or cloud storage.

Once you have the exported `.txt` file, place it in the project folder or upload it to the hosted app and run the `preprocess()` function (see Run locally or Quickstart sections) to convert it to a DataFrame for analysis.

## Files in this repo

- `app.py` — Streamlit app and main entry point for the UI.
- `preprocessor.py` — parsing logic: turns exported chat text into a structured DataFrame.
- `helper.py` — analysis helpers: statistics, word cloud generation, emoji extraction, and aggregation helpers.
- `Notebook.ipynb` — interactive exploration and example analyses.
- `requirements.txt` — list of Python dependencies.

## Troubleshooting

- If parsing fails, ensure the exported file matches WhatsApp's standard export format (date, time, sender: message). Try exporting without media if the file is too large.
- If emojis do not display correctly, verify the file encoding (UTF-8) when opening the `.txt` file.
- For time parsing issues, ensure your device locale matches the date format; `preprocessor.py` attempts to handle common variations but may need adjustments for uncommon locales.




