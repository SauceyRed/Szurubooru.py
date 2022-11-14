"""
Copyright (C) 2022-present  SauceyRed

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import requests

from functions import API_URL, TOKEN, headers

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

	@classmethod
	def from_json(cls, json):
		return Post(json["version"], json["id"], json["creationTime"], json["lastEditTime"], json["safety"], json["source"],
					json["type"], json["checksum"], json["checksumMD5"], json["canvasWidth"], json["canvasHeight"], json["contentUrl"],
					json["thumbnailUrl"], json["flags"], json["tags"], json["relations"], json["notes"], json["user"], json["score"],
					json["ownScore"], json["ownFavorite"], json["tagCount"], json["favoriteCount"], json["commentCount"], json["noteCount"],
					json["featureCount"], json["relationCount"], json["lastFeatureTime"], json["favoritedBy"], json["hasCustomThumbnail"],
					json["mimeType"], json["comments"], json["pools"])

	@classmethod
	def to_json(self):
		return {
			"version": self.version, "id": self.id, "creationTime": self.creation_time, "lastEditTime": self.last_edit_time,
			"safety": self.safety, "source": self.source, "type": self.type, "checksum": self.checksum, "checksumMD5": self.checksum_MD5,
			"canvasWidth": self.canvas_width, "canvasHeight": self.canvas_height, "contentUrl": self.content_url, "thumbnailUrl": self.thumbnail_url,
			"flags": self.flags, "tags": self.tags, "relations": self.relations, "notes": self.notes, "user": self.user, "score": self.score,
			"ownScore": self.own_score, "ownFavorite": self.own_favorite, "tagCount": self.tag_count, "favoriteCount": self.favorite_count,
			"commentCount": self.comment_count, "noteCount": self.note_count, "featureCount": self.feature_count, "relationCount": self.relation_count,
			"lastFeatureTime": self.last_feature_time, "favoritedBy": self.favorited_by, "hasCustomThumbnail": self.has_custom_thumbnail,
			"mimeType": self.mime_type, "comments": self.comments, "pools": self.pools
		}

	def create(self, anonymous=False):
		post_r = requests.post(API_URL + f"/posts/", json={"tags": self.tags, "safety": self.safety, "source": self.source,
														"relations": self.relations, "notes": self.notes, "flags": self.flags,
														"anonymous": anonymous}, headers=headers)
		post_r_json = post_r.json()
		post_r.raise_for_status()
		return print(f"Created post with ID {post_r_json['id']}")
	
	def update(self):
		post_r = requests.put(API_URL + f"/posts/", json={"version": self.version, "tags": self.tags,
														"safety": self.safety, "source": self.source, "relations": self.relations,
														"notes": self.notes, "flags": self.flags}, headers=headers)
		post_r_json = post_r.json()
		post_r.raise_for_status()
		return print(f"Created post with ID {post_r_json['id']}")

	def getPreviousPost(self):
		post_r = requests.get(API_URL + f"/post/{self.id}/around", headers=headers)
		post_r_json = post_r.json()
		post_r.raise_for_status()
		prev_post = post_r_json["prev"]
		return prev_post

	def getNextPost(self):
		post_r = requests.get(API_URL + f"/post/{self.id}/around", headers=headers)
		post_r_json = post_r.json()
		post_r.raise_for_status()
		next_post = post_r_json["next"]
		return next_post

	def delete(self):
		post_r = requests.delete(API_URL + f"/post/{self.id}", json={"version": self.version}, headers=headers)
		post_r_json = post_r.json()
		post_r.raise_for_status()
		return print(f"Created post with ID {post_r_json['id']}")

	def merge(self, target_post, replace_content):
		post_r = requests.post(API_URL + f"/post-merge/", json={"removeVersion": self.version, "remove": self.id,
																"mergeToVersion": target_post.version, "mergeTo": target_post.id,
																"replaceContent": replace_content}, headers=headers)
		post_r.raise_for_status()
		return print(f"Merged posts with IDs {self.id} and {target_post.id}")

	def like(self):
		if self.own_score == 1: return print(f"Post with ID {self.id} is already liked!")
		post_r = requests.put(API_URL + f"/post/{self.id}/score", json={"score": 1}, headers=headers)
		post_r.raise_for_status()
		return print(f"Liked post with ID {self.id}")
	
	def dislike(self):
		if self.own_score == 1: return print(f"Post with ID {self.id} is already disliked!")
		post_r = requests.put(API_URL + f"/post/{self.id}/score", json={"score": -1}, headers=headers)
		post_r.raise_for_status()
		return print(f"Disliked post with ID {self.id}")
	
	def reset_rating(self):
		if self.own_score == 1: return print(f"Post with ID {self.id} has not been liked or disliked by you!")
		post_r = requests.put(API_URL + f"/post/{self.id}/score", json={"score": 0}, headers=headers)
		post_r.raise_for_status()
		return print(f"Reset rating on post with ID {self.id}")
	
	def favorite(self):
		if self.own_favorite: return print(f"Post with ID {self.id} is already favorited!")
		post_r = requests.post(API_URL + f"/post/{self.id}/favorite", headers=headers)
		post_r.raise_for_status()
		return print(f"Favorited post with ID {self.id}")

	def unfavorite(self):
		if self.own_favorite: return print(f"Post with ID {self.id} is not favorited!")
		post_r = requests.delete(API_URL + f"/post/{self.id}/favorite", headers=headers)
		post_r.raise_for_status()
		return print(f"Unfavorited post with ID {self.id}")

	def feature(self):
		post_r = requests.post(API_URL + f"/featured-post", json={"id": self.id}, headers=headers)
		post_r.raise_for_status()
		return print(f"Featured post with ID {self.id}")

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