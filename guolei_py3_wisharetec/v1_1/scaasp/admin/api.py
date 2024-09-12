#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
作者：[郭磊]
手机：[5210720528]
Email：[174000902@qq.com]
=================================================
"""

import hashlib
import json
from typing import Union, Callable

import diskcache
import redis
import requests
from addict import Dict
from jsonschema import validate
from jsonschema.validators import Draft202012Validator


class Api(object):
    """
    慧享(绿城)科技 智慧社区全域服务平台 管理 API Class
    """

    def __init__(
            self,
            base_url: str = None,
            username: str = None,
            password: str = None,
            diskcache_cache: diskcache.Cache = None,
            redis_cache: Union[redis.Redis, redis.StrictRedis] = None
    ):
        """
        构造函数
        :param base_url: base url
        :param username: 用户名
        :param password: 密码
        :param diskcache_cache: diskcache.Cache instance
        :param redis_cache: redis.Redis instance or redis.StrictRedis instance
        """
        validate(instance=base_url, schema={"type": "string", "minLength": 1, "format": "uri", })
        validate(instance=username, schema={"type": "string", "minLength": 1, })
        validate(instance=password, schema={"type": "string", "minLength": 1, })
        self._base_url = base_url
        self._username = username
        self._password = password
        self._diskcache_cache = diskcache_cache
        self._redis_cache = redis_cache
        self._token_data = Dict()

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def diskcache_cache(self):
        return self._diskcache_cache

    @diskcache_cache.setter
    def diskcache_cache(self, diskcache_cache):
        self._diskcache_cache = diskcache_cache

    @property
    def redis_cache(self):
        return self._redis_cache

    @redis_cache.setter
    def redis_cache(self, redis_cache):
        self._redis_cache = redis_cache

    @property
    def token_data(self):
        return self._token_data

    @token_data.setter
    def token_data(self, token_data):
        self._token_data = token_data

    def is_login(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        是否登录
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not isinstance(request_func_kwargs, dict):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/old/serverUserAction!checkSession.action")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("headers", {
            "Token": self.token_data.get("token", ""),
            "Companycode": self.token_data.get("companyCode", ""),
        })
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                instance=isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                    isinstance(response.json(), dict)):
                return "null" in response.text.lower().strip()
        return False

    def login(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        登录
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/login")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("data", {
            "username": self.username,
            "password": hashlib.md5(self.password.encode("utf-8")).hexdigest(),
            "mode": "PASSWORD",
        })
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                instance=isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                self.token_data = Dict(response.json()).data
                return True
        return False

    def login_with_diskcache_cache(
            self,
            diskcache_cache_key: str = None,
            diskcache_cache_expire: float = None,
            is_login_func_kwargs: dict = {},
            login_func_kwargs: dict = {},
    ):
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.diskcache_cache, diskcache.Cache)):
            if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                    isinstance(is_login_func_kwargs, dict)):
                is_login_func_kwargs = {}
            if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                    isinstance(login_func_kwargs, dict)):
                login_func_kwargs = {}
            is_login_func_kwargs = Dict(is_login_func_kwargs)
            login_func_kwargs = Dict(login_func_kwargs)
            if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(diskcache_cache_key):
                diskcache_cache_key = "_".join([
                    "guolei_py3_wisharetec_v1_scaasp_admin_api_diskcache_cache",
                    "token",
                    hashlib.md5(self.base_url.encode("utf-8")).hexdigest(),
                    hashlib.md5(self.username.encode("utf-8")).hexdigest(),
                ])
            self.token_data = Dict(self.diskcache_cache.get(key=diskcache_cache_key, default={}))
        if not self.is_login(**is_login_func_kwargs):
            if self.login(**login_func_kwargs):
                self.diskcache_cache.set(
                    key=diskcache_cache_key,
                    value=self.token_data.to_dict(),
                    expire=diskcache_cache_expire
                )
        return self

    def login_with_redis_cache(
            self,
            redis_cache_key: str = None,
            redis_cache_expire: float = None,
            is_login_func_kwargs: dict = {},
            login_func_kwargs: dict = {},
    ):
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.redis_cache, (redis.Redis, redis.StrictRedis))):
            if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                    isinstance(is_login_func_kwargs, dict)):
                is_login_func_kwargs = {}
            if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                    isinstance(login_func_kwargs, dict)):
                login_func_kwargs = {}
            is_login_func_kwargs = Dict(is_login_func_kwargs)
            login_func_kwargs = Dict(login_func_kwargs)
            if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(redis_cache_key):
                diskcache_cache_key = "_".join([
                    "guolei_py3_wisharetec_v1_scaasp_admin_api_redis_cache",
                    "token",
                    hashlib.md5(self.base_url.encode("utf-8")).hexdigest(),
                    hashlib.md5(self.username.encode("utf-8")).hexdigest(),
                ])
            if isinstance(self.redis_cache.get(key=redis_cache_key), str):
                self.token_data = Dict(json.loads(self.redis_cache.get(key=redis_cache_key)))
            else:
                self.token_data = Dict()
        if not self.is_login(**is_login_func_kwargs):
            if self.login(**login_func_kwargs):
                self.diskcache_cache.set(
                    key=diskcache_cache_key,
                    value=self.token_data.to_dict(),
                    expire=redis_cache_expire
                )
        return self

    def login_with_cache(
            self,
            cache_type: str = None,
            cache_key: str = None,
            cache_expire: float = None,
            is_login_func_kwargs: dict = {},
            login_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(cache_type):
            cache_type = "diskcache_cache"
        if cache_type.lower() not in ["diskcache_cache", "redis_cache"]:
            cache_type = "diskcache_cache"
        if cache_type.lower() == "diskcache_cache":
            return self.login_with_diskcache_cache(
                diskcache_cache_key=cache_key,
                diskcache_cache_expire=cache_expire,
                is_login_func_kwargs=is_login_func_kwargs,
                login_func_kwargs=login_func_kwargs
            )
        if cache_type.lower() == "redis_cache":
            return self.login_with_redis_cache(
                redis_cache_key=cache_key,
                redis_cache_expire=cache_expire,
                is_login_func_kwargs=is_login_func_kwargs,
                login_func_kwargs=login_func_kwargs
            )
        raise ValueError("Cache type must be 'diskcache_cache' or 'redis_cache'")

    def query_community_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 项目管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/communityInfo/getAdminCommunityList")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_community_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 项目管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/communityInfo/getCommunityInfo")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_room_no_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 房号管理 > 有效房号
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/communityRoom/listCommunityRoom")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_room_no_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 房号管理 > 有效房号 > 编辑
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/communityRoom/getFullRoomInfo")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_register_user_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册用户管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/user/register/list")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_register_user_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册用户管理 > 详情
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/user/register/detail")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_register_owner_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册业主管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/user/information/register/list")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_register_owner_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册业主管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/user/information/register/detail")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_unregister_owner_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 未注册业主管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/user/information/unregister/list")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_unregister_owner_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 未注册业主管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/user/information/unregister/detail")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_shop_goods_category_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 自定义分类
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/productCategory/getProductCategoryList")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_shop_goods_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/shopGoods/getAdminShopGoods")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_shop_goods_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 编辑
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/shopGoods/getShopGoodsDetail")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def save_shop_goods(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 编辑 > 保存
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/shopGoods/saveSysShopGoods")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("json", {})
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        if Draft202012Validator({"type": "str", "minLebgth": 1}).is_valid(request_func_kwargs.id):
            request_func_kwargs.setdefault("url", f"{self.base_url}/manage/shopGoods/updateShopGoods")
            request_func_kwargs.setdefault("method", f"PUT")
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_shop_goods_push_to_store(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 推送到门店商品
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/shopGoods/getGoodsStoreEdits")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def save_shop_goods_push_to_store(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 推送到门店商品 > 保存
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/shopGoods/saveGoodsStoreEdits")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("json", {})
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_store_product_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/storeProduct/getAdminStoreProductList")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_store_product_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品 > 编辑
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/storeProduct/getStoreProductInfo")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def update_store_product(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品 > 编辑 > 保存
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/storeProduct/updateStoreProductInfo")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("json", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def update_store_product_status(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品 > 上下架
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/storeProduct/updateProductStatus")
        request_func_kwargs.setdefault("method", f"PUT")
        request_func_kwargs.setdefault("data", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_business_order_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 订单管理 > 商业订单
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/businessOrderShu/list")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_business_order_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品 > 编辑
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/businessOrderShu/view")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_parking_auth_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权管理
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/carParkApplication/carParkCard/list")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_parking_auth_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权管理 > 编辑
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/carParkApplication/carParkCard")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def update_parking_auth(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权管理 > 编辑 > 保存
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/manage/carParkApplication/carParkCard")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("json", {})
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_parking_auth_audit_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权审核
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url",
                                       f"{self.base_url}/manage/carParkApplication/carParkCard/parkingCardManagerByAudit")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_parking_auth_audit_check_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权审核 > 审核进程
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url",
                                       f"{self.base_url}/manage/carParkApplication/getParkingCheckList")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def update_parking_auth_audit_status(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权审核 > 更新审核状态
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url",
                                       f"{self.base_url}/manage/carParkApplication/completeTask")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("json", {})
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_export_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        数据服务 > 数据中心
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url",
                                       f"{self.base_url}/manage/export/log")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("curPage", 1)
        request_func_kwargs.params.setdefault("pageSize", 20)
        request_func_kwargs.setdefault("headers", {})
        request_func_kwargs.headers.setdefault("Token", self.token_data.get("token", ""))
        request_func_kwargs.headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 100},
                            {"type": "string", "const": "100"},
                        ],
                    },
                    "data": {"type": "object"}
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()
