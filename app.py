import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from helper import month_chat_frequency, top_10_most_active_month, most_active_days_of_week

# Sidebar title
st.sidebar.title("WhatsApp Chat Analyzer")

# Upload file
uploaded_file = st.sidebar.file_uploader(
    "Upload your WhatsApp chat file",
    type=["txt"]
)

# Process file
if uploaded_file is not None:

    # Read uploaded chat
    chat_data = uploaded_file.read().decode("utf-8")

    # Import preprocess function
    from preprocessor import preprocess

    # Create dataframe
    df = preprocess(chat_data)

    # ----------------------------------------
    # User selection
    # ----------------------------------------
    users = df['sender'].unique().tolist()

    users.sort()

    users.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox(
        "Select a user to view messages",
        users
    )

    # ----------------------------------------
    # Show messages
    # ----------------------------------------
    if selected_user == 'Overall':

        st.subheader("Messages from Overall")

        st.dataframe(df.drop(columns=['urls']))

    else:

        user_messages = df[df['sender'] == selected_user]

        st.subheader(f"Messages from {selected_user}")

        st.dataframe(
            user_messages[
                ['time', 'message', 'day', 'month', 'year']
            ].head()
        )

    # ----------------------------------------
    # Show analysis button
    # ----------------------------------------
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False

    if 'analysis_section' not in st.session_state:
        st.session_state.analysis_section = 'Overview'

    def show_analysis_panel():
        st.session_state.show_analysis = True

    def set_analysis_section(section_name):
        st.session_state.analysis_section = section_name

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            border: none;
            border-radius: 14px;
            padding: 0.7rem 1rem;
            font-weight: 700;
            color: white;
            background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25);
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(79, 70, 229, 0.32);
            color: white;
        }
        [data-testid="stSidebar"] .stButton > button:active {
            transform: translateY(0px);
        }
        [data-testid="stSidebar"] .stButton > button:focus {
            outline: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.button("Show Analysis", on_click=show_analysis_panel)

    if st.session_state.show_analysis:

        if selected_user == 'Overall':
            valid_sections = [
                'Active Users',
                'Monthly Chat',
                'Top Months',
                'Active Days',
                'Heatmap',
                'Word Cloud',
                'Messages',
                'Emojis'
            ]
            default_section = 'Active Users'
        else:
            valid_sections = [
                'Links',
                'Word Cloud',
                'Messages',
                'Emojis'
            ]
            default_section = 'Links'

        if st.session_state.analysis_section not in valid_sections:
            st.session_state.analysis_section = default_section

        from helper import fetch_stats

        # Fetch statistics
        num_messages, total_words, media_messages, deleted_messages = fetch_stats(
            selected_user,
            df
        )

        # ----------------------------------------
        # Top stats
        # ----------------------------------------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", num_messages)

        with col2:
            st.metric("Total Words", total_words)

        with col3:
            st.metric("Media Shared", media_messages)

        with col4:
            st.metric("Deleted Messages", deleted_messages)

        # ----------------------------------------
        # Section selector
        # ----------------------------------------
        st.subheader("Analysis Sections")
        section_buttons = valid_sections

        st.markdown(
            """
            <style>
            .stButton > button {
                padding-left: 0rem;
                padding-right: 0rem;
                min-height: 2.2rem;
                font-size: 0.82rem;
                border-radius: 12px;
                border: 1px solid rgba(79, 70, 229, 0.20);
                background: rgba(79, 70, 229, 0.06);
            }
            .stButton > button:hover {
                border-color: rgba(79, 70, 229, 0.45);
                background: rgba(79, 70, 229, 0.12);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        button_cols = st.columns(len(section_buttons), gap="small")
        for col, section_name in zip(button_cols, section_buttons):
            with col:
                if st.button(section_name, use_container_width=True, key=f"section_{section_name}"):
                    set_analysis_section(section_name)

        st.caption(f"Selected section: {st.session_state.analysis_section}")

        # ----------------------------------------
        # Links Shared Analysis
        # ----------------------------------------
        # Store link details
        link_data = []

        if st.session_state.analysis_section == 'Links' and selected_user != 'Overall':
            st.header("Links Shared Analysis")

            # Filter dataframe
            if selected_user == 'Overall':
                temp_df = df
            else:
                temp_df = df[df['sender'] == selected_user]

            # Iterate rows
            for _, row in temp_df.iterrows():

                # urls column already exists
                if isinstance(row['urls'], list):

                    for link in row['urls']:

                        if pd.notna(link):

                            link_data.append({
                                "Link": link,
                                "Date": f"{row['day']}-{row['month']}-{row['year']}",
                                "Time": row['time']
                            })

        # Create dataframe
        links_df = pd.DataFrame(link_data)

        # ----------------------------------------
        # Display table
        # ----------------------------------------
        if st.session_state.analysis_section == 'Links' and not links_df.empty and selected_user != 'Overall':

            st.subheader(f"Total Links Shared: {len(links_df)}")

            # Render clickable links: convert Link column to HTML anchors
            links_df_display = links_df.copy()
            links_df_display['Link'] = links_df_display['Link'].apply(
                lambda x: f'<a href="{x}" target="_blank" rel="noopener">{x}</a>'
            )

            # Use HTML table rendering with escape=False so anchors are not escaped
            html_table = links_df_display.to_html(index=False, escape=False)

            # Wrap table in a scrollable container to avoid full-page expansion
            # Add CSS to left-align the Link column and increase Date column width
            style = (
                "<style>"
                ".table-container table{border-collapse:collapse;width:100%;}"
                ".table-container th,.table-container td{padding:12px;text-align:center;}"
                ".table-container th:nth-child(1),.table-container td:nth-child(1){text-align:left;}"
                ".table-container th:nth-child(2),.table-container td:nth-child(2){min-width:220px;width:220px;}"
                ".table-container a{color:#1f77b4;text-decoration:underline;}"
                "</style>"
            )

            scrollable_html = (
                f'<div class="table-container" style="max-height:320px; overflow:auto; border:1px solid #ddd; padding:8px;">'
                f'{style}{html_table}'
                '</div>'
            )

            st.markdown(scrollable_html, unsafe_allow_html=True)

        else:
            if st.session_state.analysis_section == 'Links' and selected_user != 'Overall':
                st.write("No links shared.")

        # ----------------------------------------
        # Active users analysis
        # ----------------------------------------

        if st.session_state.analysis_section == 'Active Users' and selected_user == 'Overall':

            col1, col2 = st.columns(2)
            
            with col1:
            
                st.header("Top Most Active Users")

                user_message_counts = df['sender'].value_counts().head(10)

                st.bar_chart(user_message_counts)

            with col2:
                user_activity_pct = (df['sender'].value_counts(normalize=True) * 100).round(2)
                user_activity_df = user_activity_pct.rename_axis('sender').reset_index(name='percentage')

                st.subheader("Percentage Share of Messages per User")
                st.dataframe(user_activity_df)

            # ----------------------------------------
            # Monthly chat frequency analysis
            # ----------------------------------------
        if st.session_state.analysis_section == 'Monthly Chat' and selected_user == 'Overall':
            st.header("Monthly Chat Frequency")
            monthly_chat = month_chat_frequency(df)
            fig = px.line(
                monthly_chat,
                x='date',
                y='message_count',
                title='Monthly Chat Frequency',
                markers=True
            )
            fig.update_traces(line=dict(color='#d62728', width=3))
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Message Count',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

            # ----------------------------------------
            # Top 10 most active months analysis
            # ----------------------------------------
        if st.session_state.analysis_section == 'Top Months' and selected_user == 'Overall':
            st.header("Top 10 Most Active Months")
            top_months = top_10_most_active_month(df)
            fig = px.bar(
                top_months,
                x='year_month',
                y='message_count',
                title='Top 10 Most Active Months',
                color='message_count',
                color_continuous_scale='Oranges'
            )
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Message Count',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # ----------------------------------------
            # Most active days of the week analysis
            # ----------------------------------------
        if st.session_state.analysis_section == 'Active Days' and selected_user == 'Overall':
            st.header("Most Active Days of the Week")
            active_days = most_active_days_of_week(df)
            fig = px.bar(
                active_days,
                x='day_of_week',
                y='message_count',
                title='Most Active Days of the Week',
                color='message_count',
                color_continuous_scale='Greens'
            )
            fig.update_layout(
                xaxis_title='Day of Week',
                yaxis_title='Message Count',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # ----------------------------------------
            # Heatmap of activity by day of week and hour
            # ----------------------------------------
        if st.session_state.analysis_section == 'Heatmap' and selected_user == 'Overall':
            st.header("Activity Heatmap by Day of Week and Hour")
            from helper import heatmap_data
            heatmap_df = heatmap_data(df)
            fig = px.imshow(
                heatmap_df,
                color_continuous_scale='Reds',
                aspect='auto',
                title='Activity Heatmap by Day of Week and Hour'
            )
            fig.update_layout(
                xaxis_title='Hour of Day',
                yaxis_title='Day of Week'
            )
            st.plotly_chart(fig, use_container_width=True)

        # ----------------------------------------
        # Word cloud analysis
        # ----------------------------------------
        if st.session_state.analysis_section == 'Word Cloud':
            st.header("Word Cloud of Messages")
            from helper import wordcloud_data
            wordcloud = wordcloud_data(df, selected_user)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

        # ----------------------------------------
        # Most common messages analysis
        # ----------------------------------------
        if st.session_state.analysis_section == 'Messages':
            st.header("Most Common Messages")
            from helper import most_common_messages
            common_messages_df = most_common_messages(df, selected_user)
            if common_messages_df.empty:
                st.write("No messages available.")
            else:
                fig = px.bar(
                    common_messages_df,
                    x='message',
                    y='count',
                    title='Most Common Messages',
                    color='count',
                    color_continuous_scale='Purples'
                )
                fig.update_layout(
                    xaxis_title='Message',
                    yaxis_title='Count',
                    coloraxis_showscale=False
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

        # ----------------------------------------
        # Emoji analysis
        # ----------------------------------------
        if st.session_state.analysis_section == 'Emojis':
            st.header("Most Common Emojis")
            from helper import emoji_analysis
            emoji_df = emoji_analysis(df, selected_user)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(emoji_df, use_container_width=True, hide_index=True)
            with col2:
                if emoji_df.empty:
                    st.write("No emojis found.")
                else:
                    fig = px.pie(
                        emoji_df,
                        names='emoji',
                        values='count',
                        title='Most Common Emojis'
                    )
                    st.plotly_chart(fig, use_container_width=True)