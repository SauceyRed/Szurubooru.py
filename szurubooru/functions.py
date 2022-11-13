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

from classes import *
from base64 import b64encode
from json import load

with open("config.json") as f:
	f_json = load(f)
	API_URL = f_json["API_URL"]
	TOKEN = b64encode(bytes(f_json["TOKEN"], "utf-8")).decode("utf-8")

headers: dict = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}

def getPost(id, verbatim=False):
	r = requests.get(API_URL + f"/post/{id}", headers=headers)
	r_json = r.json()
	r.raise_for_status()
	return Post.from_json(r_json)

def getAllPosts(id=None, tag=None, score=None, uploader=None, upload=None, comment=None, fav=None, pool=None, tag_count=None, comment_count=None,
				fav_count=None, note_count=None, note_text=None, relation_count=None, feature_count=None, type=None, content_checksum=None,
				file_size=None, image_width=None, image_height=None, image_area=None, image_aspect_ratio=None, creation_date=None, last_edit_date=None,
				comment_date=None, fav_date=None, feature_date=None, safety=None, verbatim=False):
	r = requests.get(API_URL + "/posts", headers=headers)
	r_json = r.json()
	r.raise_for_status()
	if verbatim:
		print("Total posts: " + str(r_json["total"]))
		print("Limit: " + str(r_json["limit"]))
	page_count = r_json["total"] / r_json["limit"]
	iter = 0
	all_posts = []
	while page_count > 0:
		if verbatim: print("Page count: " + str(page_count))
		offset = r_json["limit"] * iter
		if verbatim: print("Offset: " + str(offset))
		r = requests.get(API_URL + "/posts" + f"/?offset={offset}", headers=headers)
		r_json = r.json()
		r.raise_for_status()
		all_posts_json = r_json["results"]
		for post in all_posts_json:
			all_posts.append(Post.from_json(post))
			if verbatim: print(f"Got post with ID {post['id']}")
		page_count -= 1
		iter += 1
	if verbatim: 
		print("Received all posts!")
		print("Total posts: " + str(len(all_posts)))
	return all_posts

def likeAllPosts(id=None, tag=None, score=None, uploader=None, upload=None, comment=None, fav=None, pool=None, tag_count=None, comment_count=None,
				fav_count=None, note_count=None, note_text=None, relation_count=None, feature_count=None, type=None, content_checksum=None,
				file_size=None, image_width=None, image_height=None, image_area=None, image_aspect_ratio=None, creation_date=None, last_edit_date=None,
				comment_date=None, fav_date=None, feature_date=None, safety=None, verbatim=False):
	all_posts = getAllPosts(id, tag, score, uploader, upload, comment, fav, pool, tag_count, comment_count,
				fav_count, note_count, note_text, relation_count, feature_count, type, content_checksum,
				file_size, image_width, image_height, image_area, image_aspect_ratio, creation_date, last_edit_date,
				comment_date, fav_date, feature_date, safety, verbatim)

	for post in all_posts:
		if post.own_score == 1: print(f"Post with ID {post.id} is already liked, skipping..."); continue
		post_r = requests.put(API_URL + f"/post/{post.id}/score", json={"score": 1}, headers=headers)
		post_r.raise_for_status()
		if verbatim: print(f"Liked post with ID {post.id}")
	if verbatim: print("Liked all posts!")
	return True
