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
				fav_count=None, note_count=None, note_text=None, relation_count=None, feature_count=None, _type=None, content_checksum=None,
				file_size=None, image_width=None, image_height=None, image_area=None, image_aspect_ratio=None, creation_date=None, last_edit_date=None,
				comment_date=None, fav_date=None, feature_date=None, safety=None, verbose=False):
	_updateAuth()
	request_url = API_URL + "/posts/?"
	
	if amount: request_url += f"limit={amount}&"
	if id: request_url += f"id={id}&"
	if tag: request_url += f"tag={tag}&"
	if score: request_url += f"score={score}&"
	if uploader: request_url += f"uploader={uploader}&"
	if upload: request_url += f"upload={upload}&"
	if comment: request_url += f"comment={comment}&"
	if fav: request_url += f"fav={fav}&"
	if pool: request_url += f"pool={pool}&"
	if tag_count: request_url += f"tag-count={tag_count}&"
	if comment_count: request_url += f"comment-count={comment_count}&"
	if fav_count: request_url += f"fav-count={fav_count}&"
	if note_count: request_url += f"note-count={note_count}&"
	if note_text: request_url += f"note-text={note_text}&"
	if relation_count: request_url += f"relation-count={relation_count}&"
	if feature_count: request_url += f"feature-count={feature_count}&"
	if _type: request_url += f"type={_type}&"
	if content_checksum: request_url += f"content-checksum={content_checksum}&"
	if file_size: request_url += f"file-size={file_size}&"
	if image_width: request_url += f"image-width={image_width}&"
	if image_height: request_url += f"image-height={image_height}&"
	if image_area: request_url += f"image-area={image_area}&"
	if image_aspect_ratio: request_url += f"image-aspect-ratio={image_aspect_ratio}&"
	if creation_date: request_url += f"creation-date={creation_date}&"
	if last_edit_date: request_url += f"last-edit-date={last_edit_date}&"
	if comment_date: request_url += f"comment-date={comment_date}&"
	if fav_date: request_url += f"fav-date={fav_date}&"
	if feature_date: request_url += f"feature-date={feature_date}&"
	if safety: request_url += f"safety={safety}&"

	r = requests.get(request_url, headers=HEADERS)
	print(request_url)
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
			# if amount and len(all_posts) == amount: return all_posts
		page_count -= 1
		iter += 1
	if verbose: 
		print("Received all posts!")
		print("Total posts: " + str(len(all_posts)))
	return all_posts

def likeAllPosts(id=None, tag=None, score=None, uploader=None, upload=None, comment=None, fav=None, pool=None, tag_count=None, comment_count=None,
				fav_count=None, note_count=None, note_text=None, relation_count=None, feature_count=None, _type=None, content_checksum=None,
				file_size=None, image_width=None, image_height=None, image_area=None, image_aspect_ratio=None, creation_date=None, last_edit_date=None,
				comment_date=None, fav_date=None, feature_date=None, safety=None, verbose=False):

	_updateAuth()

	all_posts = listPosts(69, id, tag, score, uploader, upload, comment, fav, pool, tag_count, comment_count,
				fav_count, note_count, note_text, relation_count, feature_count, _type, content_checksum,
				file_size, image_width, image_height, image_area, image_aspect_ratio, creation_date, last_edit_date,
				comment_date, fav_date, feature_date, safety, verbose)

	for post in all_posts:
		if post.own_score == 1: print(f"Post with ID {post.id} is already liked, skipping..."); continue
		post_r = requests.put(API_URL + f"/post/{post.id}/score", json={"score": 1}, headers=HEADERS)
		post_r.raise_for_status()
		if verbose: print(f"Liked post with ID {post.id}")
	if verbose: print("Liked all posts!")
	return True
