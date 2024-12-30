from flask import  Flask, request
from flask_restx import Api, Resource, fields
from config import DevelopmentConfig
from models import  Recipe
from exts import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# initialize SQLAlchemy
db.init_app(app)

api = Api(app, doc='/docs')

# model (serializer)
recipe_model = api.model('Recipe', {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
})

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {'message': 'Hello World!'}



@api.route('/recipes')
class RecipesResource(Resource):

    @api.marshal_list_with(recipe_model)  # helps convert the sqlalchemy object (recipe to a jason string)
    def get(self):
        """"Get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @api.marshal_with(recipe_model)
    def post(self):
        """Add a new recipe"""
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get('title'),
            description=data.get('description'),
        )

        new_recipe.save()
        return new_recipe, 201

@api.route('/recipes/<int:recipe_id>')
class RecipeResource(Resource):

    @api.marshal_with(recipe_model)
    def get(self, recipe_id):
        """Get a specific recipe"""
        recipe = Recipe.query.get_or_404(recipe_id)
        return recipe, 200

    @api.marshal_with(recipe_model)
    def put(self, recipe_id):
        """Update a recipe"""
        recipe_to_update = Recipe.query.get_or_404(recipe_id)
        data = request.get_json()
        recipe_to_update.update(data.get('title'), data.get('description'))
        return recipe_to_update, 200

    def delete(self, recipe_id):
        """Delete a recipe"""

        try:
            recipe = Recipe.query.get_or_404(recipe_id)
            recipe.delete()
        except Exception as e:
            return f"An error occurred while trying to delete recipe with id: {recipe_id}. Error: {str(e)}", 500

        return f"Recipe with id {recipe_id} has been deleted", 200




@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Recipe": Recipe
    }


if __name__ == '__main__':
    app.run(debug=True)

