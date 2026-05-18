from pydantic import BaseModel
from typing import Optional, List, Dict

class ModelItem(BaseModel):
    name: str
    slug: str

class ChannelItem(ModelItem):
    pass

class CategoryItem(ModelItem):
    pass

class TagItem(ModelItem):
    pass

class GalleryImage(BaseModel):
    thumbnail: str
    image: str


class GalleryItem(BaseModel):
    gallery_id: str
    slug: str
    title: str
    images: List[GalleryImage]
    models: Optional[List[ModelItem]]
    channels: Optional[List[ChannelItem]]
    tags: Optional[List[TagItem]]
    categories: Optional[List[CategoryItem]]
    rating: Optional[str] = None
    views: Optional[str] = None