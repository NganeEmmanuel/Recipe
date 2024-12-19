from urllib import request

from flask import  Flask
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
    def get(self):
        """"Get all recipes"""
        recipes = Recipe.query.all()
        return {'recipes': recipes}

    def post(self):
        """Add a new recipe"""
        data = request.get_json()
        recipe = Recipe(**data)
        db.session.add(recipe)
        db.session.commit()
        return {'message': 'Recipe added!'}, 201

@api.route('/recipes/<int:recipe_id>')
class RecipeResource(Resource):
    def get(self, recipe_id):
        """Get a specific recipe"""
        recipe = Recipe.query.get(recipe_id)
        return {'recipe': recipe}

    def put(self, recipe_id):
        """Update a recipe"""
        pass

    def delete(self, recipe_id):
        """Delete a recipe"""
        pass




@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Recipe": Recipe
    }


if __name__ == '__main__':
    app.run(debug=True)

