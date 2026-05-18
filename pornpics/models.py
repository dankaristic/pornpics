from pydantic import BaseModel
from typing import Optional, List, Dict

class PornstarItem(BaseModel):
    name: str
    slug: str

class GalleryModel(BaseModel):
    gid: int
    slug: str
    thumbnail: str
    title: str

class ChannelItem(PornstarItem):
    pass

class CategoryItem(PornstarItem):
    pass

class TagItem(PornstarItem):
    pass

class GalleryImage(BaseModel):
    thumbnail: str
    image: str


class GalleryResponse(BaseModel):
    gallery_id: str
    slug: str
    title: str
    images: List[GalleryImage]
    models: Optional[List[PornstarItem]]
    channels: Optional[List[ChannelItem]]
    tags: Optional[List[TagItem]]
    categories: Optional[List[CategoryItem]]
    rating: Optional[str] = None
    views: Optional[str] = None

class CategoryResponse(BaseModel):
    slug: Optional[str]
    title: Optional[str]
    tags: Optional[List[TagItem]]
    categories: Optional[List[CategoryItem]]
    galleries: List[GalleryModel]