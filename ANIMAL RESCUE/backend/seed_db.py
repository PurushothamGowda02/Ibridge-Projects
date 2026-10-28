from database import SessionLocal, engine
import models, auth

def seed():
    db = SessionLocal()
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)

    # Check if we already have animals
    if db.query(models.Animal).count() == 0:
        print("Seeding Animals...")
        animals = [
            models.Animal(
                name="Buddy",
                species="Dog",
                breed="Golden Retriever",
                age="Puppy",
                gender="Male",
                description="Buddy is a playful and loving puppy who loves to play fetch and cuddle.",
                image_url="http://localhost:5173/hero.png",
                status="available"
            ),
            models.Animal(
                name="Luna",
                species="Cat",
                breed="Calico",
                age="Adult",
                gender="Female",
                description="Luna is a calm and elegant cat who enjoys quiet afternoons and sunbathing.",
                image_url="http://localhost:5173/hero.png",
                status="available"
            ),
            models.Animal(
                name="Max",
                species="Dog",
                breed="German Shepherd",
                age="Adult",
                gender="Male",
                description="Max is highly trained, loyal, and looking for a house with a big yard.",
                image_url="http://localhost:5173/hero.png",
                status="available"
            ),
             models.Animal(
                name="Bella",
                species="Cat",
                breed="Persian",
                age="Kitten",
                gender="Female",
                description="Bella is a fluffy white kitten who loves to purr and sit on laps.",
                image_url="http://localhost:5173/hero.png",
                status="available"
            )
        ]
        db.add_all(animals)
        db.commit()
        print("Added 4 animals.")
    else:
        print("Animals already exist in database.")

    db.close()

if __name__ == "__main__":
    seed()
