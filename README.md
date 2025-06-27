# BarkBoard 🐶

**BarkBoard** is like **Pinterest for dogs**—discover and collect adorable dog photos in a visually rich, interactive gallery. Powered by **Streamlit** for fast UI, **Sensei** for API client generation, and **SQLModel** for seamless persistence.

## 🚀 Features

1. **Random & Breed-Specific Dogs**: Get surprise pups or choose your favorite breed.
2. **Pin to Favorites**: Save photos to your own gallery for later viewing.
3. **Gallery View**: Scroll through saved dogs in a clean, grid-based interface.
4. **Stats Dashboard**: See which breeds you love most with real-time charts.

## Screenshots

### Main Page

<img src="https://raw.githubusercontent.com/blnkoff/barkboard/main/img/random_dog.png" alt="Main Page" width="400px">

### Favorites View

<img src="https://raw.githubusercontent.com/blnkoff/barkboard/main/img/favorite.png" alt="Favorites View" width="400px">

### Stats Dashboard

<img src="https://raw.githubusercontent.com/blnkoff/barkboard/main/img/stats.png" alt="Stats Dashboard" width="400px">

## 🛠️ Tech Stack

* **[Streamlit](https://docs.streamlit.io/)** — Build data apps with pure Python, no frontend needed. ([docs.streamlit.io][1])
* **[Sensei](https://github.com/CrocoFactory/sensei)** — Generate type-safe API wrappers using decorators and Pydantic models. ([github.com][2])
* **[SQLModel](https://sqlmodel.tiangolo.com/)** — Define Python classes that serve as both Pydantic models and SQLAlchemy ORM tables. ([sqlmodel.tiangolo.com][3])
* **[Dog CEO API](https://dog.ceo/dog-api/)** — Source of 20,000+ open-source dog images. ([dog.ceo][4])

## 📦 Installation

```bash
# 1. Clone repository
git clone https://github.com/your_username/barkboard.git
cd barkboard

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install poetry
poetry install
```

## ▶️ Running the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` to view the app.

## 📂 Project Structure

```
streampaws/
├── app.py               # Streamlit UI script
├── client/              # Sensei API wrapper module
│   └── api.py           # DogImage model & get_random_dog endpoint
├── models.py            # SQLModel ORM definitions and DB init
├── LICENSE              # License file
├── dogs.db              # Database with featured dogs
├── pyproject.toml       # Pinned dependencies
└── README.md            # This file
```

## 📄 License

Released under the [MIT License](https://opensource.org/licenses/MIT).

[1]: https://docs.streamlit.io/?utm_source=chatgpt.com
[2]: https://github.com/CrocoFactory/sensei?utm_source=chatgpt.com
[3]: https://sqlmodel.tiangolo.com/?utm_source=chatgpt.com
[4]: https://dog.ceo/dog-api/documentation/?utm_source=chatgpt.com
