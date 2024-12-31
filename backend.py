import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)
def get_apps_ids(_conn):
    with _conn:
        query = """SELECT apps_id FROM apps;"""
        df = pd.read_sql_query(query, _conn)
        return df['apps_id'].tolist()

@st.cache_data(ttl=600)
def get_apps_names(_conn):
    with _conn:
        query = """SELECT app_name FROM apps;"""
        df = pd.read_sql_query(query, _conn)
        return df['app_name'].tolist()

@st.cache_data(ttl=600)
def get_header_img(app_id, _conn):
    with _conn:
        query = f"""SELECT header_img_url FROM apps WHERE apps_id = {app_id}"""
        df = pd.read_sql_query(query, _conn)
        return df['header_img_url'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspects(app_id, _conn):
    with _conn:
        match app_id:
            case 1:
                query = """SELECT aspect_name FROM aspects LIMIT 50;"""
                df = pd.read_sql_query(query, _conn)
                return df['aspect_name'].tolist()
            case 2:
                query = """SELECT aspect_name FROM aspects LIMIT 50 OFFSET 50;"""
                df = pd.read_sql_query(query, _conn)
                return df['aspect_name'].tolist()
            case 3:
                query = """SELECT aspect_name FROM aspects LIMIT 50 OFFSET 100;"""
                df = pd.read_sql_query(query, _conn)
                return df['aspect_name'].tolist()
            case 4:
                query = """SELECT aspect_name FROM aspects LIMIT 50 OFFSET 150;"""
                df = pd.read_sql_query(query, _conn)
                return df['aspect_name'].tolist()
            case 5:
                query = """SELECT aspect_name FROM aspects LIMIT 50 OFFSET 200;"""
                df = pd.read_sql_query(query, _conn)
                return df['aspect_name'].tolist()
            case _:
                print("Error!")

@st.cache_data(ttl=600)
def get_number_of_reviews(app_id, _conn):
    with _conn:
        query = f"""SELECT COUNT(*) FROM reviews WHERE apps_id = {app_id} ;"""
        df = pd.read_sql_query(query, _conn)
        return df['COUNT(*)'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_one_star_reviews(app_id, _conn):
    with _conn:
        query = f"""SELECT COUNT(*) FROM reviews WHERE apps_id = {app_id} AND rating = 1;"""
        df = pd.read_sql_query(query, _conn)
        return df['COUNT(*)'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_two_star_reviews(app_id, _conn):
    with _conn:
        query = f"""SELECT COUNT(*) FROM reviews WHERE apps_id = {app_id} AND rating = 2;"""
        df = pd.read_sql_query(query, _conn)
        return df['COUNT(*)'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_three_star_reviews(app_id, _conn):
    with _conn:
        query = f"""SELECT COUNT(*) FROM reviews WHERE apps_id = {app_id} AND rating = 3;"""
        df = pd.read_sql_query(query, _conn)
        return df['COUNT(*)'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_four_star_reviews(app_id, _conn):
    with _conn:
        query = f"""SELECT COUNT(*) FROM reviews WHERE apps_id = {app_id} AND rating = 4;"""
        df = pd.read_sql_query(query, _conn)
        return df['COUNT(*)'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_five_star_reviews(app_id, _conn):
    with _conn:
        query = f"""SELECT COUNT(*) FROM reviews WHERE apps_id = {app_id} AND rating = 5;"""
        df = pd.read_sql_query(query, _conn)
        return df['COUNT(*)'].tolist()[0]

@st.cache_data(ttl=600)
def get_start_date(app_id, _conn):
    with _conn:
        query = f"""SELECT MIN(time) AS start_date FROM reviews WHERE apps_id = {app_id} ;"""
        df = pd.read_sql_query(query, _conn)
        return df['start_date'].tolist()[0]

@st.cache_data(ttl=600)
def get_end_date(app_id, _conn):
    with _conn:
        query = f"""SELECT MAX(time) AS end_date FROM reviews WHERE apps_id = {app_id} ;"""
        df = pd.read_sql_query(query, _conn)
        return df['end_date'].tolist()[0]

@st.cache_data(ttl=600)
def get_review_timestamps(app_id, _conn):
    with _conn:
        query = f"""SELECT time FROM reviews WHERE apps_id = {app_id} ;"""
        df = pd.read_sql_query(query, _conn)
        return df['time'].tolist()

@st.cache_data(ttl=600)
def get_number_of_positive_sentences(app_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.sent) AS sent
        FROM sents s
        JOIN reviews r ON s.review_id = r.review_id
        WHERE r.apps_id = {app_id} AND s.senti = 1 ;"""
        df = pd.read_sql_query(query, _conn)
        return df['sent'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_neutral_sentences(app_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.sent) AS sent
        FROM sents s
        JOIN reviews r ON s.review_id = r.review_id
        WHERE r.apps_id = {app_id} AND s.senti = 0 ;"""
        df = pd.read_sql_query(query, _conn)
        return df['sent'].tolist()[0]

@st.cache_data(ttl=600)
def get_number_of_negative_sentences(app_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.sent) AS sent
        FROM sents s
        JOIN reviews r ON s.review_id = r.review_id
        WHERE r.apps_id = {app_id} AND s.senti = -1 ;"""
        df = pd.read_sql_query(query, _conn)
        return df['sent'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_positive_sentiments(app_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.senti) as senti
        FROM sents s
        JOIN reviews r ON s.review_id = r.review_id
        JOIN apps a ON r.apps_id = a.apps_id
        WHERE a.apps_id = {app_id} AND s.senti = 1 ;
        """
        df = pd.read_sql_query(query, _conn)
        return df['senti'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_id(aspect_name, _conn):
    with _conn:
        query = f"""SELECT aspect_id FROM aspects WHERE aspect_name = '{aspect_name}' ;"""
        df = pd.read_sql_query(query, _conn)
        return df['aspect_id'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_senti_positive(aspect_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.senti) as senti
        FROM sents s
        JOIN kws_sents ks ON s.sent_id = ks.sent_id
        JOIN kws k on ks.kw_id = k.kw_id
        JOIN aspects a on k.aspect_id = a.aspect_id
        WHERE a.aspect_id = {aspect_id} AND s.senti = 1;"""
        df = pd.read_sql_query(query, _conn)
        return df['senti'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_senti_neutral(aspect_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.senti) as senti
        FROM sents s
        JOIN kws_sents ks ON s.sent_id = ks.sent_id
        JOIN kws k on ks.kw_id = k.kw_id
        JOIN aspects a on k.aspect_id = a.aspect_id
        WHERE a.aspect_id = {aspect_id} AND s.senti = 0;"""
        df = pd.read_sql_query(query, _conn)
        return df['senti'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_senti_negative(aspect_id, _conn):
    with _conn:
        query = f"""
        SELECT COUNT(s.senti) as senti
        FROM sents s
        JOIN kws_sents ks ON s.sent_id = ks.sent_id
        JOIN kws k on ks.kw_id = k.kw_id
        JOIN aspects a on k.aspect_id = a.aspect_id
        WHERE a.aspect_id = {aspect_id} AND s.senti = -1;"""
        df = pd.read_sql_query(query, _conn)
        return df['senti'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_sentence_summary(aspect_id, rank, _conn):
    with _conn:
        query = f"""
        SELECT s.sent as sent
        FROM sents s
        JOIN kws_sents ks ON s.sent_id = ks.sent_id
        JOIN kws k on ks.kw_id = k.kw_id
        JOIN aspects a on k.aspect_id = a.aspect_id
        WHERE a.aspect_id = {aspect_id} AND ks.rank = {rank};
        """
        df = pd.read_sql_query(query, _conn)
        if df['sent'].isnull().all():
            return None
        else:
            return df['sent'].tolist()[0]

@st.cache_data(ttl=600)
def get_aspect_name(aspect_id, _conn):
    with _conn:
        query = f"""SELECT aspect_name FROM aspects WHERE aspect_id = {aspect_id} ;"""
        df = pd.read_sql_query(query, _conn)
        return df['aspect_name'].tolist()[0]

