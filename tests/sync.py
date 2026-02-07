from erome import Client

client = Client()

print("--- get_explore ---")
home = client.get_explore()
print(f"Found {len(home)} albums")

if home:
    album_url = home[0].id
    album_id = album_url.split("/")[-1]
    print(f"First album: {home[0].name} (ID: {album_id})")
else:
    album_id = "vGCHXU6e"

print(f"\n--- get_album ({album_id}) ---")
album = client.get_album(album_id)
print(f"Album Title: {album.title}")
# AlbumResponse has 'contents' which is a Dict[str, List[MediaItem]]
media_count = len(album.contents.get("videos", [])) + len(album.contents.get("images", []))
print(f"Media count: {media_count}")

print(f"\n--- get_related_albums ({album_id}) ---")
related = client.get_related_albums(album_id)
print(f"Found {len(related)} related albums")

print("\n--- get_search (query='milf') ---")
search_results = client.get_search("milf")
print(f"Found {len(search_results)} albums in search")

# Try to find a user from the explore page to test get_profile
# We'll use 'TheRealWolf' as a fallback if we can't find one, it's a common user
username = "TheRealWolf" 
print(f"\n--- get_profile ({username}) ---")
try:
    profile = client.get_profile(username)
    print(f"Profile: {profile.username}")
    print(f"Albums in profile: {len(profile.albums)}")
except Exception as e:
    print(f"Could not fetch profile for {username}: {e}")
