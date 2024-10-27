from fastapi import FastAPI, HTTPException
from models import Blog, UpdateBlog
from database import blog_collection
from bson import ObjectId
from pydantic import BaseModel

app = FastAPI()

# Helper function to format MongoDB document to JSON
def blog_helper(blog) -> dict:
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "content": blog["content"],
        "author": blog["author"],
        "views": blog["views"],
    }

# Create a blog
@app.post("/blog/", response_model=Blog)
async def create_blog(blog: Blog):
    new_blog = await blog_collection.insert_one(blog.dict())
    created_blog = await blog_collection.find_one({"_id": new_blog.inserted_id})
    return blog_helper(created_blog)

# Get all blogs
@app.get("/blogs/")
async def get_blogs():
    blogs = []
    async for blog in blog_collection.find():
        blogs.append(blog_helper(blog))
    return blogs

# Get a single blog by ID
@app.get("/blog/{id}", response_model=Blog)
async def get_blog(id: str):
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        return blog_helper(blog)
    raise HTTPException(status_code=404, detail="Blog not found")

# Update a blog by ID
@app.put("/blog/{id}")
async def update_blog(id: str, blog: UpdateBlog):
    update_result = await blog_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": blog.dict(exclude_unset=True)}
    )
    if update_result.modified_count == 1:
        updated_blog = await blog_collection.find_one({"_id": ObjectId(id)})
        return blog_helper(updated_blog)
    raise HTTPException(status_code=404, detail="Blog not found")

# Delete a blog by ID
@app.delete("/blog/{id}")
async def delete_blog(id: str):
    delete_result = await blog_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")