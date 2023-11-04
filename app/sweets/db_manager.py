from sqlmodel import Session, select

from app.sweets.models import Sweet, SweetCreate


def create_sweet(sweet: SweetCreate, session: Session, user):
    print("sweet.price")
    print(sweet.price)
    type(sweet.price)

    new_sweet = Sweet(
        title=sweet.title,
        description=sweet.description,
        price=int(sweet.price),
        user_id=user[0].id,

    )
    session.add(new_sweet)
    session.commit()
    session.refresh(new_sweet)

    return new_sweet


def get_sweet_by_id(sweet_id: int, session):
    query = select(Sweet).where(Sweet.id == sweet_id)
    result = session.exec(query)
    sweet = result.one_or_none()
    return sweet
#
#
def get_deserts(page: int, session):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    sweets = select(Sweet).offset(offset1).limit(max_per_page)
    results = session.exec(sweets)
    all_sweets = results.all()
    return all_sweets


def get_deserts_count(session):
    sweets = select(Sweet)
    results = session.exec(sweets)
    sweets_result = results.all()
    sweets_count = len(sweets_result)
    return sweets_count


def update_sweet(sweet_id: int, payload: SweetCreate, session):
    statement = select(Sweet).where(Sweet.id == sweet_id)
    results = session.exec(statement)
    sweet = results.one()

    # Update
    sweet.title = payload.title
    sweet.description = payload.description
    sweet.price = payload.price
    session.add(sweet)
    session.commit()
    session.refresh(sweet)

    return sweet

def delete_sweet(sweet_id: int, session):
    query = select(Sweet).where(Sweet.id == sweet_id)
    results = session.exec(query)
    sweet = results.one()

    session.delete(sweet)
    session.commit()

    return sweet