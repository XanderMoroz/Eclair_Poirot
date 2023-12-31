from sqlmodel import Session, select

from app.sweets.models import Sweet, Category, SweetCategory, Ingredient, SweetIngredient
from app.sweets.schemas import SweetCreate, CategoryCreate, IngredientCreate


def create_sweet(sweet: SweetCreate, session: Session, user):
    """
    Creates a new sweet.

    Args:
     - sweet (SweetCreate): Sweet creation data.
     - session (Session): SQLAlchemy database session.
     - user: User object.

    Returns: Newly created sweet object.
    """
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


def get_my_sweets(session: Session, user):
    """
    Retrieves a sweets of current user

    Args:
     - session (Session): SQLAlchemy database session.
     - user: User object.

    Returns: List of Sweets objects or None.
    """
    user = user[0]
    query = select(Sweet).where(Sweet.user_id == user.id)
    result = session.exec(query)
    sweets = result.all()
    print(sweets[0].categories)
    print(sweets[0].ingredients)
    return sweets


def get_sweet_by_id(sweet_id: int, session):
    """
    Retrieves a sweet by ID.

    Args:
     - sweet_id (int): ID of the sweet.
     - session (Session): SQLAlchemy database session.

    Returns: Sweet object or None if not found.
    """
    query = select(Sweet).where(Sweet.id == sweet_id)
    result = session.exec(query)
    sweet = result.one_or_none()
    return sweet


def get_deserts(page: int, session):
    """
    Retrieves a list of sweets with pagination.

    Args:
     - page (int): Page number.
     - session (Session): SQLAlchemy database session.

    Returns: List of Sweet objects.
    """
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    sweets = select(Sweet).offset(offset1).limit(max_per_page)
    results = session.exec(sweets)
    all_sweets = results.all()
    return all_sweets


def get_deserts_count(session):
    """
    Retrieves the count of sweets.

    Args:
     - session (Session): SQLAlchemy database session.

    Returns: Count of sweets.
    """
    sweets = select(Sweet)
    results = session.exec(sweets)
    sweets_result = results.all()
    sweets_count = len(sweets_result)
    return sweets_count


def update_sweet(sweet_id: int, payload: SweetCreate, session):
    """
    Deletes a sweet.

    Args:
     - sweet_id (int): ID of the sweet.
     - session (Session): SQLAlchemy database session.

    Returns: Deleted sweet object.
    """
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
    """
    Deletes a sweet.

    Args:
     - sweet_id (int): ID of the sweet.
     - session (Session): SQLAlchemy database session.

    Returns: Deleted sweet object.
    """
    query = select(Sweet).where(Sweet.id == sweet_id)
    results = session.exec(query)
    sweet = results.one()

    session.delete(sweet)
    session.commit()

    return sweet


def create_category(category: CategoryCreate, session):
    """
    Creates a new category of sweets.

    Args:
     - category (CategoryCreate): category creation data.
     - session (Session): SQLAlchemy database session.
     - user: User object.

    Returns: Newly created category object.
    """
    new_category = Category(
        title=category.title
    )
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category


def get_category_by_id(category_id: int, session):
    """
    Retrieves a category by ID.

    Args:
     - category_id (int): ID of the category.
     - session (Session): SQLAlchemy database session.

    Returns: Category object or None if not found.
    """
    query = select(Category).where(Category.id == category_id)
    result = session.exec(query)
    category = result.one_or_none()
    return category


def add_category_of_sweet(sweet_id: int, category_id: int, session):
    """
    Adds a category to a sweet.

    Args:
    - sweet_id (int): ID of the sweet.
    - category_id (int): ID of the category.
    - session (Session): SQLAlchemy database session.

    Returns: Newly created SweetCategory object.
    """
    new_sweet_category = SweetCategory(
        sweet_id=sweet_id,
        category_id=category_id
    )
    session.add(new_sweet_category)
    session.commit()
    session.refresh(new_sweet_category)
    return new_sweet_category


def remove_category_of_sweet(sweet_id: int, category_id: int, session):
    """
    Removes a category from a sweet.

    Args:
     - sweet_id (int): ID of the sweet.
     - category_id (int): ID of the category.
     - session (Session): SQLAlchemy database session.

    Returns: Removed SweetCategory object.
    """
    query = select(SweetCategory).where(SweetCategory.sweet_id == sweet_id, SweetCategory.category_id == category_id)
    results = session.exec(query)
    sweet_category = results.one()
    session.delete(sweet_category)
    session.commit()
    return sweet_category


def create_ingredient(ingredient: IngredientCreate, session):
    """
    Creates a new ingredient of sweets.

    Args:
     - ingredient (IngredientCreate): ingredient payload data.
     - session (Session): SQLAlchemy database session.
     - user: User object.

    Returns: Newly created ingredient object.
    """
    new_ingredient = Ingredient(
        title=ingredient.title
    )
    session.add(new_ingredient)
    session.commit()
    session.refresh(new_ingredient)

    return new_ingredient


def get_ingredient_by_id(ingredient_id: int, session):
    """
    Retrieves a ingredient by ID.

    Args:
     - ingredient_id (int): ID of the ingredient.
     - session (Session): SQLAlchemy database session.

    Returns: Ingredient object or None if not found.
    """
    print(ingredient_id)
    query = select(Ingredient).where(Ingredient.id == ingredient_id)
    result = session.exec(query)
    ingredient = result.one_or_none()
    print(ingredient)
    return ingredient


def add_ingredient_to_sweet(sweet_id: int, ingredient_id: int, session):
    """
    Adds a ingredient to a sweet.

    Args:
    - sweet_id (int): ID of the sweet.
    - ingredient_id (int): ID of the ingredient.
    - session (Session): SQLAlchemy database session.

    Returns: Newly created SweetIngredient object.
    """
    new_sweet_ingredient = SweetIngredient(
        sweet_id=sweet_id,
        ingredient_id=ingredient_id
    )
    session.add(new_sweet_ingredient)
    session.commit()
    session.refresh(new_sweet_ingredient)
    return new_sweet_ingredient


def remove_ingredient_of_sweet(sweet_id: int, ingredient_id: int, session):
    """
    Removes a ingredient from a sweet.

    Args:
     - sweet_id (int): ID of the sweet.
     - ingredient_id (int): ID of the ingredient.
     - session (Session): SQLAlchemy database session.

    Returns: Removed SweetIngredient object.
    """
    query = select(SweetIngredient).where(SweetIngredient.sweet_id == sweet_id,
                                          SweetIngredient.ingredient_id == ingredient_id)
    results = session.exec(query)
    sweet_ingredient = results.one()
    session.delete(sweet_ingredient)
    session.commit()
    return sweet_ingredient


def search_sweets(search_query: str, session: Session):
    """
    Searches for sweets based on a search query.

    Args:
     - search_query (str): Search query string.
     - session (Session): SQLAlchemy database session.

    Returns: List of Sweet objects matching the search query.
    """
    query = select(Sweet).where(Sweet.title.ilike('%' + search_query + '%'))
    results = session.exec(query)
    sweet = results.all()

    return sweet


def filter_sweets(min_price: int,
                  max_price: int,
                  session: Session):
    """
    Filters sweets based on price range.

    Args:
     - min_price (int): Minimum price value.
     - max_price (int): Maximum price value.
     - session (Session): SQLAlchemy database session.

    Returns: List of Sweet objects within the specified price range.
    """

    query = select(Sweet).where(Sweet.price >= min_price, Sweet.price <= max_price)
    results = session.exec(query)
    sweets = results.all()

    return sweets
