from sqlmodel import SQLModel, Field, create_engine

class FavoriteDog(SQLModel, table=True):
    __table_args__ = {"extend_existing": True} 
    id: int | None = Field(default=None, primary_key=True)
    url: str

engine = create_engine('sqlite:///dogs.db', echo=False)  # Disable SQL logging
# Create tables only if they don't exist
SQLModel.metadata.create_all(engine, checkfirst=True)
