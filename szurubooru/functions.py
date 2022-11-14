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

from .classes import *
from .auth import *

def _updateAuth():
	global API_URL, HEADERS
	API_URL, HEADERS = getAuth()

def listTagCategories(amount=10):
	_updateAuth()
	r = requests.get(API_URL + "/tag-categories", headers=HEADERS)
	r_json = r.json()
	r.raise_for_status()
	all_tag_categories = []
	for tag_category in r_json["results"]:
		all_tag_categories.append(TagCategory.from_json(tag_category))
		if amount and len(all_tag_categories) == amount: return all_tag_categories
	return all_tag_categories

def createTagCategory(name, color, order):
	_updateAuth()
	r = requests.post(API_URL + "/tag-categories", json={"name": name, "color": color, "order": order}, headers=HEADERS)
	r_json = r.json()
	r.raise_for_status()
	return Post.from_json(r_json)

def createPost(tags, safety, source, relations, notes, flags, anonymous=False):
	_updateAuth()
	r = requests.post(API_URL + f"/posts/", json={"tags": tags, "safety": safety, "source": source,
													"relations": relations, "notes": notes, "flags": flags,
													"anonymous": anonymous}, headers=HEADERS)
	r_json = r.json()
	r.raise_for_status()
	return print(f"Created post with ID {r_json['id']}")

def getPost(id, verbose=False):
	_updateAuth()
	r = requests.get(API_URL + f"/post/{id}", headers=HEADERS)
	r_json = r.json()
	r.raise_for_status()
	return Post.from_json(r_json)

def getFeaturedPost(verbose=False):
	_updateAuth()
	r = requests.get(API_URL + "/featured-post", headers=HEADERS)
	r_json = r.json()
	r.raise_for_status()
	return Post.from_json(r_json)

def listPosts(amount=10, id=None, tag=None, score=None, uploader=None, upload=None, comment=None, fav=None, pool=None, tag_count=None, comment_count=None,
				fav_count=None, note_count=None, note_text=None, relation_count=None, feature_count=None, type=None, content_checksum=None,
				file_size=None, image_width=None, image_height=None, image_area=None, image_aspect_ratio=None, creation_date=None, last_edit_date=None,
				comment_date=None, fav_date=None, feature_date=None, safety=None, verbose=False):
	_updateAuth()
	r = requests.get(API_URL + "/posts", headers=HEADERS)
	r_json = r.json()
	r.raise_for_status()
	if verbose:
		print("Total posts: " + str(r_json["total"]))
		print("Limit: " + str(r_json["limit"]))
	page_count = r_json["total"] / r_json["limit"]
	iter = 0
	all_posts = []
	while page_count > 0:
		if verbose: print("Page count: " + str(page_count))
		offset = r_json["limit"] * iter
		if verbose: print("Offset: " + str(offset))
		r = requests.get(API_URL + "/posts" + f"/?offset={offset}", headers=HEADERS)
		r_json = r.json()
		r.raise_for_status()
		all_posts_json = r_json["results"]
		for post in all_posts_json:
			all_posts.append(Post.from_json(post))
			if verbose: print(f"Got post with ID {post['id']}")
			if amount and len(all_posts) == amount: return all_posts
		page_count -= 1
		iter += 1
	if verbose: 
		print("Received all posts!")
		print("Total posts: " + str(len(all_posts)))
	return all_posts

def likeAllPosts(id=None, tag=None, score=None, uploader=None, upload=None, comment=None, fav=None, pool=None, tag_count=None, comment_count=None,
				fav_count=None, note_count=None, note_text=None, relation_count=None, feature_count=None, type=None, content_checksum=None,
				file_size=None, image_width=None, image_height=None, image_area=None, image_aspect_ratio=None, creation_date=None, last_edit_date=None,
				comment_date=None, fav_date=None, feature_date=None, safety=None, verbose=False):

	_updateAuth()

	all_posts = listPosts(id, tag, score, uploader, upload, comment, fav, pool, tag_count, comment_count,
				fav_count, note_count, note_text, relation_count, feature_count, type, content_checksum,
				file_size, image_width, image_height, image_area, image_aspect_ratio, creation_date, last_edit_date,
				comment_date, fav_date, feature_date, safety, verbose)

	for post in all_posts:
		if post.own_score == 1: print(f"Post with ID {post.id} is already liked, skipping..."); continue
		post_r = requests.put(API_URL + f"/post/{post.id}/score", json={"score": 1}, headers=HEADERS)
		post_r.raise_for_status()
		if verbose: print(f"Liked post with ID {post.id}")
	if verbose: print("Liked all posts!")
	return True
