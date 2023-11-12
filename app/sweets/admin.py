from sqladmin import ModelView

from app.sweets.models import Sweet, Category, SweetCategory, Ingredient, SweetIngredient


class SweetAdmin(ModelView, model=Sweet):
    column_list = [Sweet.id,
                   Sweet.user_id,
                   Sweet.title,
                   Sweet.description,
                   Sweet.price,
                   Sweet.in_stock,
                   Sweet.created_at,
                   Sweet.edited_at,
                   Sweet.categories,
                   Sweet.ingredients,]

    async def insert_model(self, request, data):
        data["user_id"] = request.session["user_id"]
        return await super().insert_model(request, data)


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id,
                   Category.title,]


class SweetCategoryAdmin(ModelView, model=SweetCategory):
    column_list = [SweetCategory.sweet_id,
                   SweetCategory.category_id]


class IngredientAdmin(ModelView, model=Ingredient):
    column_list = [Ingredient.id,
                   Ingredient.title]


class SweetIngredientAdmin(ModelView, model=SweetIngredient):
    column_list = [SweetIngredient.sweet_id,
                   SweetIngredient.ingredient_id]
