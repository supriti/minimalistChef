class RecipesController < ApplicationController
    def index
        @recipes = Recipe.all
    end

    def show
        @recipe = Recipe.find(params[:id])
        @ingredients = []
        RecipeIngredient.where("recipe_id=?", params[:id]).find_each do |ri|
            @ingredients.append(Ingredient.find(ri.ingredient_id))
        end
    end
  
    def new
        
    end

    def create

    end
    
    def edit
        @recipe = Recipe.find(params[:id])
    end
    
    def update
       
    end
    
    def delete
       Recipe.find(params[:id]).destroy
       redirect_to :action => 'list'
    end
end
