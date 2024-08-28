# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
import hashlib
import json
from datetime import timedelta
from typing import Iterable, Callable, Union

import diskcache
import redis
import requests
from addict import Dict


class AdminApi(object):
    """
    慧享(绿城)科技 智慧社区全域服务平台 管理API Class
    """

    def __init__(
            self,
            base_url: str = "",
            username: str = "",
            password: str = "",
            disckcache_cache_instance: diskcache.Cache = None,
            redis_cache_instance: Union[redis.Redis, redis.StrictRedis] = None,
    ):
        """
        Admin Api Class 构造函数
        :param base_url: Admin Api Base URL
        :param username: Admin Api Username
        :param password: Admin Api Password
        :param disckcache_cache_instance: Admin Api Disk Cache Instance
        :param redis_cache_instance: Admin Api Redis Instance
        """
        self._base_url = base_url
        self._username = username
        self._password = password
        self._disckcache_cache_instance = disckcache_cache_instance
        self._redis_cache_instance = redis_cache_instance
        self._token_data = {}

    @property
    def base_url(self):
        """
        Admin Api Base URL
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        """
        Admin Api Base URL
        :param value:
        :return:
        """
        self._base_url = value

    @property
    def username(self):
        """
        Admin Api Username
        :return:
        """
        return self._username

    @username.setter
    def username(self, value):
        """
        Admin Api Username
        :param value:
        :return:
        """
        self._username = value

    @property
    def password(self):
        """
        Admin Api Password
        :return:
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Admin Api Password
        :param value:
        :return:
        """
        self._password = value

    @property
    def disckcache_cache_instance(self):
        """
        Admin Api Disk Cache Instance
        :return:
        """
        return self._disckcache_cache_instance

    @disckcache_cache_instance.setter
    def disckcache_cache_instance(self, value):
        """
        Admin Api Disk Cache Instance
        :param value:
        :return:
        """
        self._disckcache_cache_instance = value

    @property
    def redis_cache_instance(self):
        """
        Admin Api Redis Instance
        :return:
        """
        return self._redis_cache_instance

    @redis_cache_instance.setter
    def redis_cache_instance(self, value):
        """
        Admin Api Redis Instance
        :param value:
        :return:
        """
        self._redis_cache_instance = value

    @property
    def token_data(self):
        """
        Admin Api Token Data
        :return:
        """
        return self._token_data

    @token_data.setter
    def token_data(self, value):
        """
        Admin Api Token Data
        :param value:
        :return:
        """
        self._token_data = value

    def check_manage_login(
            self,
            path: str = "/old/serverUserAction!checkSession.action",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        check manage login
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return: bool,response.status_code,response.text
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        if not isinstance(self.token_data.get("token", ""), str) or not len(self.token_data.get("token", "")):
            return False, None, None
        if not isinstance(self.token_data.get("companyCode", ""), str) or not len(
                self.token_data.get("companyCode", "")):
            return False, None, None
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            return "null" in response.text.strip(), response.status_code, response.text
        return False, response.status_code, response.text

    def manage_login(
            self,
            path: str = "/manage/login",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        manage login
        :param path:
         requests.request.args
        :param requests_request_func_kwargs: requests.request.kwargs
        :param requests_response_callable: requests.response.callable
        :return: bool,response.status_code,response.json()
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.data = Dict({
            **{
                "username": self.username,
                "password": hashlib.md5(self.password.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            },
            **requests_request_func_kwargs.data,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(json_addict.get("status", -1)) == 100:
                if len(json_addict.get("data", {}).keys()):
                    self.token_data = json_addict.data.to_dict()
                    return True, response.status_code, json_addict
        return False, response.status_code, Dict({})

    def manage_login_with_diskcache(
            self,
            expire_time: float = timedelta(days=15).total_seconds(),
            check_manage_login_func_kwargs: dict = {},
            mange_login_func_kwargs: dict = {},
    ):
        if isinstance(self.disckcache_cache_instance, diskcache.Cache):
            cache_key = "_".join([
                "guolei_py3_wisharetec",
                "v1",
                "scaasp",
                "AdminApi",
                "diskcache",
                "token_data",
                f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
                f"{self.username}",
            ])
            self.token_data = self.disckcache_cache_instance.get(key=cache_key, default={})
            state, _, _ = self.check_manage_login(**check_manage_login_func_kwargs)
            if not state:
                state, _, _ = self.manage_login(**mange_login_func_kwargs)
                if state:
                    self.disckcache_cache_instance.set(key=cache_key, value=self.token_data, expire=expire_time)
        else:
            self.manage_login(**mange_login_func_kwargs)
        return self

    def manage_login_with_redis(
            self,
            expire_time: Union[int, timedelta] = timedelta(days=15),
            check_manage_login_func_kwargs: dict = {},
            mange_login_func_kwargs: dict = {},
    ):
        if isinstance(self.redis_cache_instance, (redis.Redis, redis.StrictRedis)):
            cache_key = "_".join([
                "guolei_py3_wisharetec",
                "v1",
                "scaasp",
                "AdminApi",
                "redis",
                "token_data",
                f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
                f"{self.username}",
            ])
            if isinstance(self.redis_cache_instance.get(name=cache_key), str) and len(
                    self.redis_cache_instance.get(name=cache_key)):
                self.token_data = json.loads(self.redis_cache_instance.get(name=cache_key))
                state, _, _ = self.check_manage_login(**check_manage_login_func_kwargs)
                if not state:
                    state, _, _ = self.manage_login(**mange_login_func_kwargs)
                    if state:
                        self.redis_cache_instance.setex(name=cache_key, value=self.token_data, time=expire_time)
        else:
            self.manage_login(**mange_login_func_kwargs)
        return self

    def manage_communityInfo_getAdminCommunityList(
            self,
            requests_request_func_kwargs_params: dict = {},
            path: str = "/manage/communityInfo/getAdminCommunityList",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>项目管理
        :param requests_request_func_kwargs_params:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **requests_request_func_kwargs_params,
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_communityRoom_listCommunityRoom(
            self,
            requests_request_func_kwargs_params: dict = {},
            path: str = "/manage/communityRoom/listCommunityRoom",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>房号管理=>有效房号
        :param requests_request_func_kwargs_params:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = {
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers
        }
        requests_request_func_kwargs.params = {
            **requests_request_func_kwargs_params,
            **requests_request_func_kwargs.params
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_communityRoom_getFullRoomInfo(
            self,
            id: Union[str, int] = "",
            path: str = "/manage/communityRoom/getFullRoomInfo",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>房号管理=>有效房号=>查看
        :param id:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        if isinstance(id, str) and not len(id):
            raise ValueError("id must be a string and not empty")
        if int(id) <= 0:
            raise ValueError("id must be a positive integer")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = {
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers
        }
        requests_request_func_kwargs.params = {
            **{
                "id": id,
            },
            **requests_request_func_kwargs.params
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_register_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            path: str = "/manage/user/register/list",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>用户管理=>注册用户管理
        :param requests_request_func_kwargs_params:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **requests_request_func_kwargs_params,
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_register_detail(
            self,
            id: str = "",
            path: str = "/manage/user/register/detail",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>用户管理=>注册用户管理=>查看
        :param id:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **{
                "id": id,
            },
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_register_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            path: str = "/manage/user/information/register/list",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>用户管理=>注册业主管理
        :param requests_request_func_kwargs_params:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **requests_request_func_kwargs_params,
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_register_detail(
            self,
            id: str = "",
            org_id: Union[str, int] = "",
            community_id: str = "",
            path: str = "manage/user/information/register/detail",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>用户管理=>注册业主管理=>查看
        :param community_id:
        :param org_id:
        :param id:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        if isinstance(org_id, str) and not len(org_id):
            raise TypeError("org_id must be a string and not empty")
        if int(org_id) <= 0:
            raise ValueError("org_id must be a positive integer")
        if not isinstance(community_id, str):
            raise TypeError("community_id must be a string")
        if not len(community_id):
            raise ValueError("community_id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **{
                "id": id,
                "orgId": org_id,
                "communityId": community_id,
            },
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_unregister_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            path: str = "/manage/user/information/unregister/list",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>用户管理=>未注册业主管理
        :param requests_request_func_kwargs_params:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **requests_request_func_kwargs_params,
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_unregister_detail(
            self,
            id: str = "",
            community_id: str = "",
            path: str = "manage/user/information/unregister/detail",
            requests_request_func_kwargs: dict = {},
            requests_response_callable: Callable = None
    ):
        """
        业户中心=>用户管理=>未注册业主管理=>查看
        :param community_id:
        :param org_id:
        :param id:
        :param path:
        :param requests_request_func_kwargs:
        :param requests_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.username, str):
            raise TypeError("self.username must be a string")
        if not len(self.username):
            raise ValueError("self.username must be a string and not empty")
        if not isinstance(self.password, str):
            raise TypeError("self.password must be a string")
        if not len(self.password):
            raise ValueError("self.password must be a string and not empty")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not len(path):
            raise ValueError("path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        if not isinstance(community_id, str):
            raise TypeError("community_id must be a string")
        if not len(community_id):
            raise ValueError("community_id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.params = Dict({
            **{
                "id": id,
                "communityId": community_id,
            },
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            if isinstance(requests_response_callable, Callable):
                return requests_response_callable(response=response)
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())
