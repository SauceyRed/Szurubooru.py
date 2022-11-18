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

from base64 import b64encode

_base_url, _api_endpoint, _api_base_url, _TOKEN, _headers = "", "", "", "", ""

def setAuth(base_url: str, api_endpoint: str, token: str):
	global _base_url, _api_endpoint, _api_base_url, _TOKEN, _headers
	_base_url = base_url
	_api_endpoint = api_endpoint
	_api_base_url = _base_url.strip("/") + "/" + _api_endpoint.strip("/")
	_TOKEN = b64encode(bytes(token, "utf-8")).decode("utf-8")
	_headers = {"Authorization": f"Token {_TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}

def getBaseUrl():
	return _base_url

def getApiEndpoint():
	return _api_endpoint

def getApiBaseUrl():
	return _api_base_url

def getHeaders():
	return _headers

def getToken():
	return _TOKEN

def getAuth():
	return _api_base_url, _headers
