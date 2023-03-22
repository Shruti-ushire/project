
import streamlit_authenticator as stauth
import streamlit as st  # 🎈 data web app development
import pandas as pd # read csv, df manipulation
import numpy as np # np mean, np random
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express  as px  # interactive charts
import time  # to simulate a real time data, time loop
from wordcloud import WordCloud,STOPWORDS


        


st.title("Sentiment Analysis of Tweets about US Airlines")

def login():
    names = ['Shruti Ushire','Yash Jadhav']
    usernames = ['shruti','yash']
    passwords = ['admin','coadmin']
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login('Login', 'main')
        
    if st.session_state["authentication_status"]:
        test=authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*')
        # creating a sidebar widget
        st.sidebar.title("Customizations")
        st.sidebar.markdown("Additional filters and customizations...")

        st.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets...")

        DATA_URL = "tweets.csv"

        st.set_option('deprecation.showPyplotGlobalUse', False)


        # Load data
        @st.cache_data(persist=True)  # caching data to avoid run the function on each app re-run if the passed args not changed
        def load_data(data_url):
            data = pd.read_csv(data_url)
            data['tweet_created'] = pd.to_datetime(data['tweet_created'])
            return data


        data = load_data(DATA_URL)

        # passing data to st dashboard
        # st.write(data)

        # adding widgets to sidebar
        st.sidebar.subheader("Show random tweets")
        random_tweet = st.sidebar.radio('Sentiment Type', ('positive', 'neutral', 'negative'), key="1")

        # Query dataframe for random tweets (will show one at a time on sidebar)
        st.subheader("1) Some Random Tweets...")

        st.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])

        # data visualizations
        st.subheader("2) Visualizations:")

        st.sidebar.markdown("### Number of tweets by sentiment")
        # select box widget
        select = st.sidebar.selectbox("Visualization Type:", ['Histogram', 'Pie Chart'], key='2')

        sentiment_count = data['airline_sentiment'].value_counts()
        # st.write(sentiment_count)

        sentiment_count_df = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

        # show/hide plots
        if not st.sidebar.checkbox("Hide Visualizations", True):
            st.markdown("### Number of tweets by sentiment")
            if select == "Histogram":
                fig = px.bar(sentiment_count_df, x='Sentiment', y='Tweets', color='Tweets', height=500)
                st.plotly_chart(fig)
            else:
                fig = px.pie(sentiment_count_df, values='Tweets', names='Sentiment')
                st.plotly_chart(fig)

        # create a map visualization
        st.sidebar.subheader("When and Where users are tweeting from?")
        # hour = st.sidebar.number_input("Hour of Day", min_value=1, max_value=23)
        hour = st.sidebar.slider("Hour of Day", 0, 23)
        modified_data = data[data['tweet_created'].dt.hour == hour]

        # show/hide map plot
        if not st.sidebar.checkbox("Hide Tweets Map", True, key='3'):
            st.markdown("### Tweet locations based on the time of day")
            st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
            st.map(modified_data)
            if st.sidebar.checkbox("Show raw data table", False):
                st.write(modified_data)

        # Breakdown airlines  by sentiment (multi choice selector)
        st.sidebar.subheader("breakdown airline tweets by sentiment")
        choice = st.sidebar.multiselect('Pick airlines',
                                        ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin america'), key="4")

        if len(choice) > 0:
            choice_data = data[data.airline.isin(choice)]
            fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count',
                                    color='airline_sentiment',
                                    facet_col='airline_sentiment', labels={'airline_sentiment': 'tweets'}, height=600,
                                    width=800)
            st.plotly_chart(fig_choice)

        # creating word cloud visualizations
        st.sidebar.header("Word Cloud")
        word_sentiment = st.sidebar.radio('Display WordCloud for sentiment:', ('positive', 'neutral', 'negative'), key='5')

        if not st.sidebar.checkbox("Hide WordCloud", True, key='6'):
            st.subheader('Word cloud for %s sentiment' % word_sentiment)
            df = data[data['airline_sentiment'] == word_sentiment]
            words = ' '.join(df['text'])
            # remove unnecessary stop words and characters
            processed_words = ' '.join(
                [word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
            wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(
                processed_words)
            wordcloud_fig = plt.imshow(wordcloud)
            plt.xticks([])
            plt.yticks([])
            st.pyplot()
        
def main():
    login()

if __name__ == "__main__":
    main()





