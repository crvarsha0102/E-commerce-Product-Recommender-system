import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
import numpy as np

def load_clean_data():
    return pd.read_csv("clean_data.csv")

# Modified content-based recommendation logic
def content_based_recommendation(search_query, train_data, top_n=5):
    train_data['combined_text'] = (
        train_data['Name'].fillna('') + ' ' +
        train_data['Description'].fillna('') + ' ' +
        train_data['Tags'].fillna('')
    )

    # Initialize the TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the combined text
    tfidf_matrix = tfidf_vectorizer.fit_transform(train_data['combined_text'])

    # Transform the search query
    query_vector = tfidf_vectorizer.transform([search_query])

    # Compute cosine similarity between the query and all items
    cosine_similarities = linear_kernel(query_vector, tfidf_matrix).flatten()

    # Get indices of top N most similar items
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]

    # Get the names of the top recommended products
    return train_data.iloc[top_indices]['Name'].tolist()

# Collaborative Filtering Recommendation System
def collaborative_filtering_recommendation(train_data, target_user_ID, top_n=10):
    # Create a user-item matrix where rows are users and columns are products
    user_item_matrix = train_data.pivot_table(index='ID', columns='ProdID', values='Rating', aggfunc='mean').fillna(0)

    # Calculate user similarity using cosine similarity
    user_similarity = cosine_similarity(user_item_matrix)

    # Get the target user's index
    target_user_index = user_item_matrix.index.get_loc(target_user_ID)

    # Get similarities of the target user to all other users
    user_similarities = user_similarity[target_user_index]

    # Get indices of the most similar users (excluding the target user)
    similar_users_indices = user_similarities.argsort()[::-1][1:]

    recommended_items = []
    for user_index in similar_users_indices:
        # Get the items rated by the similar user that the target user hasn't rated yet
        rated_by_similar_user = user_item_matrix.iloc[user_index]
        not_rated_by_target_user = (rated_by_similar_user > 0) & (user_item_matrix.iloc[target_user_index] == 0)
        recommended_items.extend(user_item_matrix.columns[not_rated_by_target_user][:top_n])

    # Get product details for the recommended items
    recommended_items_details = train_data[train_data['ProdID'].isin(recommended_items)][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    return recommended_items_details.head(top_n)

# Hybrid Recommendation System
def hybrid_recommendations(train_data, target_user_id, item_name, top_n=10):
    # Combine content-based and collaborative filtering recommendations
    content_based_rec = content_based_recommendation(train_data, item_name, top_n)
    collaborative_filtering_rec = collaborative_filtering_recommendation(train_data, target_user_id, top_n)

    # Combine recommendations and remove duplicates
    hybrid_rec = pd.concat([content_based_rec, collaborative_filtering_rec]).drop_duplicates()

    return hybrid_rec.head(top_n)
