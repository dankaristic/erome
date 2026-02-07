import asyncio
from erome import AsyncClient

async def main():
    ac = AsyncClient()

    print("--- get_explore ---")
    home = await ac.get_explore()
    print(f"Found {len(home)} albums")

    if home:
        album_url = home[0].id
        album_id = album_url.split("/")[-1]
        print(f"First album: {home[0].name} (ID: {album_id})")
    else:
        album_id = "vGCHXU6e"

    print(f"\n--- get_album ({album_id}) ---")
    album = await ac.get_album(album_id)
    print(f"Album Title: {album.title}")
    media_count = len(album.contents.get("videos", [])) + len(album.contents.get("images", []))
    print(f"Media count: {media_count}")

    print(f"\n--- get_related_albums ({album_id}) ---")
    related = await ac.get_related_albums(album_id)
    print(f"Found {len(related)} related albums")

    print("\n--- get_search (query='milf') ---")
    search_results = await ac.get_search("milf")
    print(f"Found {len(search_results)} albums in search")

    username = "TheRealWolf"
    print(f"\n--- get_profile ({username}) ---")
    try:
        profile = await ac.get_profile(username)
        print(f"Profile: {profile.username}")
        print(f"Albums in profile: {len(profile.albums)}")
    except Exception as e:
        print(f"Could not fetch profile for {username}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
