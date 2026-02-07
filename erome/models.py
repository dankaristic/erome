from pydantic import BaseModel
from typing import Optional, List, Dict

class MediaItem(BaseModel):
    link: str
    caption: Optional[str] = None
    duration: Optional[str] = None


class AlbumCard(BaseModel):
    id: str
    thumb: Optional[str] = None
    name: str
    views: str
    images: Optional[str] = None
    videos: Optional[str] = None


class AlbumResponse(BaseModel):
    title: str
    album_id: str
    username: str
    icon: Optional[str] = None
    total_images: str
    total_videos: str
    contents: Dict[str, List[MediaItem]]
    success: bool
    message: Optional[str] = None

class ProfileResponse(BaseModel):
    username: str
    icon: Optional[str] = None
    metadata: Dict[str, str]  # albums, views, followers, following
    albums: List[AlbumCard]
    page: int
    success: bool = True