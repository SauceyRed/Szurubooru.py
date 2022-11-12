import requests

from base64 import b64encode
from json import load

API_URL: str = "https://gallery.keetydraws.com/api"
POSTS_ENDPOINT: str = "/posts"
with open("TOKEN.json") as f:
	f_json = load(f)
	TOKEN = b64encode(bytes(f_json["TOKEN"])).decode("utf-8")

class User:
	def __init__(self, version, name, email, rank, last_login_time, creation_time, avatar_style, avatar_url, comment_count, uploaded_post_count,
				liked_post_count, disliked_post_count, favorite_post_count):
		self.version = version
		self.name = name
		self.email = email
		self.rank = rank
		self.last_login_time = last_login_time
		self.creation_time = creation_time
		self.avatar_style = avatar_style
		self.avatar_url = avatar_url
		self.comment_count = comment_count
		self.uploaded_post_count = uploaded_post_count
		self.liked_post_count = liked_post_count
		self.disliked_post_count = disliked_post_count
		self.favorite_post_count = favorite_post_count

class MicroUser:
	def __init__(self, name, avatar_url):
		self.name = name
		self.avatar_url = avatar_url

class UserToken:
	def __init__(self, user, token, note, enabled, expiration_time, version, creation_time, last_edit_time, last_usage_time):
		self.user = user
		self.token = token
		self.note = note
		self.enabled = enabled
		self.expiration_time = expiration_time
		self.version = version
		self.creation_time = creation_time
		self.last_edit_time = last_edit_time
		self.last_usage_time = last_usage_time

class TagCategory:
	def __init__(self, version, name, color, usages, order, default):
		self.version = version
		self.name = name
		self.color = color
		self.usages = usages
		self.order = order
		self.default = default

class Tag:
	def __init__(self, version, names, category, implications, suggestions, creation_time, last_edit_time, usages, description):
		self.version = version
		self.names = names
		self.category = category
		self.implications = implications
		self.suggestions = suggestions
		self.creation_time = creation_time
		self.last_edit_time = last_edit_time
		self.usages = usages
		self.description = description

class MicroTag:
	def __init__(self, names, category, usages):
		self.names = names
		self.category = category
		self.usages = usages

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
	
		def create(anonymous: bool = False):
			try:
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.post(API_URL + f"/posts/", json={"tags": self.tags, "safety": self.safety,
																					"source": self.source, "relations": self.relations,
																					"notes": self.notes, "flags": self.flags,
																					"anonymous": anonymous}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Created post with ID {post_r_json['id']}")
			except Exception as e:
				return print(f"An error occurred while attempting to favorite a post:\n{str(e)}")
		
		def update():
			try:
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.put(API_URL + f"/posts/", json={"version": self.version, "tags": self.tags,
																					"safety": self.safety, "source": self.source,
																					"relations": self.relations, "notes": self.notes,
																					"flags": self.flags}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Created post with ID {post_r_json['id']}")
			except Exception as e:
				return print(f"An error occurred while attempting to favorite a post:\n{str(e)}")

		def around():
			try:
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.get(API_URL + f"/post/{self.id}/around", headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
			except Exception as e:
				return print(f"An error occurred while attempting to favorite a post:\n{str(e)}")
			prev_post = post_r_json["prev"]
			next_post = post_r_json["next"]
			return prev_post, next_post

		def delete():
			try:
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.delete(API_URL + f"/post/{self.id}", json={"version": self.version}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Created post with ID {post_r_json['id']}")
			except Exception as e:
				return print(f"An error occurred while attempting to favorite a post:\n{str(e)}")

		def merge(target_post, replace_content):
			try:
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.post(API_URL + f"/post-merge/", json={"removeVersion": self.version, "remove": self.id,
																					"mergeToVersion": target_post.version, "mergeTo": target_post.id,
																					"replaceContent": replace_content}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Merged posts with IDs {self.id} and {target_post.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to merge posts:\n{str(e)}")

		def like():
			try:
				if self.own_score == 1: return print(f"Post with ID {self.id} is already liked!")
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.put(API_URL + f"/post/{self.id}/score", json={"score": 1}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Liked post with ID {self.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to like a post:\n{str(e)}")
		
		def dislike():
			try:
				if self.own_score == 1: return print(f"Post with ID {self.id} is already disliked!")
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.put(API_URL + f"/post/{self.id}/score", json={"score": -1}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Disliked post with ID {self.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to dislike a post:\n{str(e)}")
		
		def reset_rating():
			try:
				if self.own_score == 1: return print(f"Post with ID {self.id} has not been liked or disliked by you!")
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.put(API_URL + f"/post/{self.id}/score", json={"score": 0}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Reset rating on post with ID {self.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to reset the rating of a post:\n{str(e)}")
		
		def favorite():
			try:
				if self.own_favorite: return print(f"Post with ID {self.id} is already favorited!")
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.post(API_URL + f"/post/{self.id}/favorite", headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Favorited post with ID {self.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to favorite a post:\n{str(e)}")

		def unfavorite():
			try:
				if self.own_favorite: return print(f"Post with ID {self.id} is not favorited!")
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.delete(API_URL + f"/post/{self.id}/favorite", headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Unfavorited post with ID {self.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to unfavorite a post:\n{str(e)}")

		def feature():
			try:
				headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
				post_r: requests.Response = requests.post(API_URL + f"/featured-post", json={"id": self.id}, headers=headers)
				post_r_json = post_r.json()
				if post_r.status_code != requests.codes.OK:
					exception_name = post_r_json["name"]
					exception_title = post_r_json["title"]
					exception_desc = post_r_json["description"]
					raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
				return print(f"Featured post with ID {self.id}")
			except Exception as e:
				return print(f"An error occurred while attempting to favorite a post:\n{str(e)}")

class MicroPost:
	def __init__(self, name, thumbnail_url):
		self.name = name
		self.thumbnail_url = thumbnail_url

class Note:
	def __init__(self, polygon, text):
		self.polygon = polygon
		self.text = text

class PoolCategory:
	def __init__(self, version, name, color, usages, default):
		self.version = version
		self.name = name
		self.color = color
		self.usages = usages
		self.default = default

class Pool:
	def __init__(self, version, id, names, category, posts, creation_time, last_edit_time, post_count, description):
		self.version = version
		self.id = id
		self.names = names
		self.category = category
		self.posts = posts
		self.creation_time = creation_time
		self.last_edit_time = last_edit_time
		self.post_count = post_count
		self.description = description

class MicroPool:
	def __init__(self, id, names, category, description, post_count):
		self.id = id
		self.names = names
		self.category = category
		self.description = description
		self.post_count = post_count

class Comment:
	def __init__(self, version, id, post_id, user, text, creation_time, last_edit_time, score, own_score):
		self.version = version
		self.id = id
		self.post_id = post_id
		self.user = user
		self.text = text
		self.creation_time = creation_time
		self.last_edit_time = last_edit_time
		self.score = score
		self.own_score = own_score

class Snapshot:
	def __init__(self, operation, type, id, user, data, time):
		self.operation = operation
		self.type = type
		self.id = id
		self.user = user
		self.data = data
		self.time = time

class UnpagedSearchResult:
	def __init__(self, results):
		self.results = results

class PagedSearchResult:
	def __init__(self, query, offset, limit, total, results):
		self.query = query
		self.offset = offset
		self.limit = limit
		self.total = total
		self.results = results

class ImageSearchResult:
	def __init__(self, exact_post, similar_posts):
		self.exact_post = exact_post
		self.similar_posts = similar_posts
	class SimilarPost:
		def __init__(self, distance, post):
			self.distance = distance
			self.post = post

def getPost(id: int):
	headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}
	try:
		r: requests.Response = requests.get(API_URL + f"/post/{id}", headers=headers)
		r_json = r.json()
		if r.status_code != requests.codes.OK:
			exception_name = r_json["name"]
			exception_title = r_json["title"]
			exception_desc = r_json["description"]
			raise Exception(f"{exception_name}: {exception_title}: {exception_desc}")
	except Exception as e:
		print(f"An error occurred requesting all posts to attempt to like all posts:\n{str(e)}")
		exit()
	
	return r_json

	# return Post(r_json["version"], r_json["id"], r_json["creationTime"], r_json["lastEditTime"], r_json["safety"], r_json["source"],
	# 			r_json["type"], r_json["checksum"], r_json["checksumMD5"], r_json["canvasWidth"], r_json["canvasHeight"], r_json["contentUrl"],
	# 			r_json["thumbnailUrl"], r_json["flags"], r_json["tags"], r_json["relations"], r_json["notes"], r_json["user"], r_json["score"],
	# 			r_json["ownScore"], r_json["ownFavorite"], r_json["tagCount"], r_json["favoriteCount"], r_json["commentCount"], r_json["noteCount"],
	# 			r_json["featureCount"], r_json["relationCount"], r_json["lastFeatureTime"], r_json["favoritedBy"], r_json["hasCustomThumbnail"],
	# 			r_json["mimeType"], r_json["comments"], r_json["pools"])

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
