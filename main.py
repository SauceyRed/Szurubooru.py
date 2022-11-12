import requests

from base64 import b64encode

API_URL: str = "https://gallery.keetydraws.com/api"
POSTS_ENDPOINT: str = "/posts"
TOKEN = b64encode(b"SauceyRed:a692dafe-f198-4b62-a831-8140fee082aa").decode("utf-8")

class Post:
	def __init__(self, version, id, creation_time, last_edit_time, safety, source, type, checksum, checksum_MD5, canvas_width, canvas_height,
				content_url, thumbnail_url, flags, tags, relations, notes, user, score, own_score, own_favorite, tag_count, favorite_count,
				comment_count, note_count, feature_count, relation_count, last_feature_time, favorited_by, has_custom_thumbnail, mime_type,
				comments, pools):
		self.version = version
		self.id = id
		self.creation_time = creation_time
		self.last_edit_time = last_edit_time
		self.safety = safety
		self.source = source
		self.type = type
		self.checksum = checksum
		self.checksum_MD5 = checksum_MD5
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.content_url = content_url
		self.thumbnail_url = thumbnail_url
		self.flags = flags
		self.tags = tags
		self.relations = relations
		self.notes = notes
		self.user = user
		self.score = score
		self.own_score = own_score
		self.own_favorite = own_favorite
		self.tag_count = tag_count
		self.favorite_count = favorite_count
		self.comment_count = comment_count
		self.note_count = note_count
		self.feature_count = feature_count
		self.relation_count = relation_count
		self.last_feature_time = last_feature_time
		self.favorited_by = favorited_by
		self.has_custom_thumbnail = has_custom_thumbnail
		self.mime_type = mime_type
		self.comments = comments
		self.pools = pools

def likeAllPosts():
	headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
	try:
		r: requests.Response = requests.get(API_URL + POSTS_ENDPOINT, headers=headers)
		r_json = r.json()
		if r.status_code != requests.codes.OK:
			exception_name = r_json["name"]
			exception_title = r_json["title"]
			exception_desc = r_json["description"]
			raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
	except Exception as e:
		print(f"An error occurred requesting all posts to attempt to like all posts:\n{str(e)}")
		exit()
	print("Total posts: " + str(r_json["total"]))
	print("Limit: " + str(r_json["limit"]))
	page_count = r_json["total"] / r_json["limit"]
	iter = 0
	while page_count > 0:
		print("Page count: " + str(page_count))
		offset = r_json["limit"] * iter
		try:
			r: requests.Response = requests.get(API_URL + POSTS_ENDPOINT + f"/?offset={offset}", headers=headers)
			r_json = r.json()
			if r.status_code != requests.codes.OK:
				exception_name = r_json["name"]
				exception_title = r_json["title"]
				exception_desc = r_json["description"]
				raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
		except Exception as e:
			print(f"An error occurred requesting all posts to attempt to like all posts:\n{str(e)}")
			exit()
		all_posts = r_json["results"]
		for post in all_posts:
			try:
				if post["ownScore"] == 1: print(f"Post with ID {post['id']} is already liked, skipping..."); continue
				post_r: requests.Response = requests.put(API_URL + f"/post/{post['id']}/score", json={"score": 1}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				print(f"Liked post with ID {post['id']}")
			except Exception as e:
				print(f"An error occurred while attempting to like all posts:\n{str(e)}")
				exit()
		page_count -= 1
		iter += 1
	print("Liked all posts!")

if __name__ == "__main__":
	likeAllPosts()
