class IngredientsController < ApplicationController
    def index
        @ingredients = Ingredient.all
    end

    def show
        @ingredient = Ingredient.find(params[:id])
    end
  
    def new
        
    end

    def create

    end
    
    def edit
        @ingredient = Ingredient.find(params[:id])
    end
    
    def update
       
    end
    
    def delete
       Ingredient.find(params[:id]).destroy
       redirect_to :action => 'list'
    end
end
