import streamlit as st
import pandas as pd
from sqlmodel import Session, select
from client.api import DogImage, Breed
from models import FavoriteDog, engine


def show_random_tab():
    """
    Displays the Random Dog tab: fetch and save random or breed-specific dogs.
    """
    st.header("🎲 Random Dog")

    # Fetch a new random dog
    if st.button("Show random dog", key="btn_random"):
        st.session_state.random_dog = DogImage.random()
        st.session_state.breed_dog = None  # Clear breed-specific

    if st.session_state.random_dog:
        dog = st.session_state.random_dog
        caption = f"Random {dog.breed}" + (f" ({dog.sub_breed})" if dog.sub_breed else "")
        st.image(dog.url, caption=caption, use_container_width=True)

        if st.button("Save to favorites", key="save_random"):
            save_favorite(dog.url)
            st.success("Random dog saved to favorites!")
            st.session_state.random_dog = None

    # Breed-specific section
    st.subheader("Or choose by breed")
    breeds_dict = Breed.get_breeds()
    breed_list = sorted(breeds_dict.keys())
    selected_breed = st.selectbox("Select breed", breed_list, key="select_breed")

    if st.button("Show dog by breed", key="btn_breed"):
        st.session_state.breed_dog = DogImage.random(breed=selected_breed)
        st.session_state.random_dog = None  # Clear random

    if st.session_state.breed_dog:
        dog = st.session_state.breed_dog
        caption = dog.breed + (f" ({dog.sub_breed})" if dog.sub_breed else "")
        st.image(dog.url, caption=caption, use_container_width=True)

        if st.button("Save to favorites", key="save_breed"):
            save_favorite(dog.url)
            st.success("Breed dog saved to favorites!")
            st.session_state.breed_dog = None


def show_favorites_tab():
    """
    Displays the Favorites tab: list, and remove favorite dogs.
    """
    st.header("🐾 Your Favorite Dogs")
    with Session(engine) as session:
        favorites = session.exec(select(FavoriteDog)).all()

    if not favorites:
        st.write("No favorites yet. Save some cute dogs! 🐕")
        return

    cols = st.columns(3)
    for idx, fav in enumerate(favorites):
        with cols[idx % 3]:
            st.image(fav.url, use_container_width=True)
            if st.button("Remove", key=f"del{fav.id}"):
                remove_favorite(fav.id)


def show_stats_tab():
    """
    Displays the Stats tab: distribution of favorite breeds.
    """
    st.header("📊 Favorite Breeds Distribution")
    with Session(engine) as session:
        favorites = session.exec(select(FavoriteDog)).all()

    if not favorites:
        st.write("No data to display. Add favorites first.")
        return

    # Extract breeds
    def extract_breed(url: str) -> str:
        slug = url.split("/breeds/")[1].split("/")[0]
        return slug.split('-', 1)[0]

    breeds = [extract_breed(f.url) for f in favorites]
    df = pd.DataFrame({"breed": breeds})
    counts = df["breed"].value_counts().rename_axis("breed").reset_index(name="count")
    st.bar_chart(counts.set_index("breed"))


def save_favorite(url: str):
    """
    Helper to save a favorite dog URL.
    """
    with Session(engine) as session:
        session.add(FavoriteDog(url=url))
        session.commit()


def remove_favorite(fav_id: int):
    """
    Helper to remove a favorite by its ID.
    """
    with Session(engine) as session:
        obj = session.get(FavoriteDog, fav_id)
        if obj:
            session.delete(obj)
            session.commit()


def main():
    st.set_page_config(page_title="🐶 BarkBoard")

    # Initialize session state
    if "random_dog" not in st.session_state:
        st.session_state.random_dog = None
    if "breed_dog" not in st.session_state:
        st.session_state.breed_dog = None

    # Tabs
    tab_random, tab_fav, tab_stats = st.tabs([
        "🎲 Random Dog", "🐾 Favorites", "📊 Stats"
    ])

    with tab_random:
        show_random_tab()
    with tab_fav:
        show_favorites_tab()
    with tab_stats:
        show_stats_tab()


if __name__ == "__main__":
    main()
