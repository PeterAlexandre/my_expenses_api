from sqlalchemy.orm import Session

from app.models.transaction_category import TransactionCategory
from app.models.user import User
from app.schemas.category import CategoryBulkItem, CategoryBulkRequest, CategoryCreate, CategoryUpdate


def create_category(session: Session, user: User, data: CategoryCreate) -> TransactionCategory:
    category = TransactionCategory(**data.model_dump(), user_id=user.id)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def get_category(session: Session, user: User, category_id: int) -> TransactionCategory | None:
    return (
        session.query(TransactionCategory)
        .filter(
            TransactionCategory.category_id == category_id,
            TransactionCategory.user_id == user.id,
        )
        .first()
    )


def list_categories(session: Session, user: User) -> list[TransactionCategory]:
    return (
        session.query(TransactionCategory)
        .filter(TransactionCategory.user_id == user.id)
        .order_by(TransactionCategory.name)
        .all()
    )


def update_category(session: Session, category: TransactionCategory, data: CategoryUpdate) -> TransactionCategory:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    session.commit()
    session.refresh(category)
    return category


def delete_category(session: Session, category: TransactionCategory) -> None:
    session.delete(category)
    session.commit()


def bulk_update_categories(
    session: Session, user: User, data: CategoryBulkRequest
) -> list[TransactionCategory]:
    incoming_ids = {item.category_id for item in data.categories if item.category_id is not None}

    existing = (
        session.query(TransactionCategory)
        .filter(TransactionCategory.user_id == user.id)
        .all()
    )
    existing_by_id = {c.category_id: c for c in existing}

    # Delete categories absent from payload
    for category in existing:
        if category.category_id not in incoming_ids:
            session.delete(category)

    result = []
    for item in data.categories:
        if item.category_id is not None:
            category = existing_by_id.get(item.category_id)
            if category is None:
                raise ValueError(f"Category {item.category_id} not found or does not belong to user.")
            category.name = item.name
            category.pattern = item.pattern
            result.append(category)
        else:
            new_category = TransactionCategory(
                name=item.name,
                pattern=item.pattern,
                user_id=user.id,
            )
            session.add(new_category)
            result.append(new_category)

    session.commit()
    for category in result:
        session.refresh(category)

    return sorted(result, key=lambda c: c.name)


def match_category(session: Session, user: User, description: str) -> int | None:
    categories = (
        session.query(TransactionCategory)
        .filter(
            TransactionCategory.user_id == user.id,
            TransactionCategory.pattern.isnot(None),
        )
        .order_by(TransactionCategory.category_id.asc())
        .all()
    )
    description_lower = description.lower()
    for category in categories:
        if category.pattern:
            patterns = [p.strip() for p in category.pattern.split(";") if p.strip()]
            if any(p.lower() in description_lower for p in patterns):
                return category.category_id
    return None
