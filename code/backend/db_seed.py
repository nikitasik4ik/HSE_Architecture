from faker import Faker

from backend.models import *
from backend.app import app, db


def seed():
    try:
        is_exist = Role.query.filter(Role.name == 'admin').one()

        if is_exist:
            print('Database already seeded')
            return

    except:
        print('Seeding database')

    fake = Faker()

    user_role = Role(name='user')
    admin_role = Role(name='admin')
    db.session.add(user_role)
    db.session.add(admin_role)

    for _ in range(10):
        user = User(username=fake.name(), email=fake.email(), password=fake.password(), role_id=1)
        db.session.add(user)
        db.session.commit()

    admin = User(username=fake.name(), email=fake.email(), password=fake.password(), role_id=2)
    db.session.add(admin)
    db.session.commit()

    # seed all tables
    found = Status(name='found')
    lost = Status(name='lost')
    db.session.add(found)
    db.session.add(lost)

    # seed breed
    dog_breed = BreedAnimal(name='labrador')
    cat_breed = BreedAnimal(name="persian")

    #seed CategoryAnimal
    dog = CategoryAnimal(name='dog', type_id=1)
    cat = CategoryAnimal(name='cat', type_id=2)


    db.session.add_all([dog, cat, dog_breed, cat_breed])
    db.session.commit()

    # seed found animals
    found_animal = FoundAnimal(name=fake.name(), description=fake.text(), category_id=1, user_id=1)
    #seed found animal correctly
    db.session.add(found_animal)
    db.session.commit()

    # seed lost animals
    lost_animal = MissingAnimal(name=fake.name(), description=fake.text(), status_id=1, category_id=2, user_id=1)
    db.session.add(lost_animal)
    db.session.commit()


    db.session.commit()

