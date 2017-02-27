class CreateRecipes < ActiveRecord::Migration[5.0]
  def change
    create_table :recipes do |t|
      t.column :name, :string
      t.column :image_url, :string
      t.column :url, :string
      t.timestamps
    end
  end
end
