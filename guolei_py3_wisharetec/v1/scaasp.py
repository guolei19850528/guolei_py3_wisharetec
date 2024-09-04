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
            diskcache_instance: diskcache.Cache = None,
            redis_instance: Union[redis.Redis, redis.StrictRedis] = None,
    ):
        """
        Admin Api Class 构造函数
        :param base_url: Admin Api Base URL
        :param username: Admin Api Username
        :param password: Admin Api Password
        :param diskcache_instance: Admin Api Disk Cache Instance
        :param redis_instance: Admin Api Redis Instance
        """
        self._base_url = base_url
        self._username = username
        self._password = password
        self._diskcache_instance = diskcache_instance
        self._redis_instance = redis_instance
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
    def diskcache_instance(self):
        """
        Admin Api Disk Cache Instance
        :return:
        """
        return self._diskcache_instance

    @diskcache_instance.setter
    def diskcache_instance(self, value):
        """
        Admin Api Disk Cache Instance
        :param value:
        :return:
        """
        self._diskcache_instance = value

    @property
    def redis_instance(self):
        """
        Admin Api Redis Instance
        :return:
        """
        return self._redis_instance

    @redis_instance.setter
    def redis_instance(self, value):
        """
        Admin Api Redis Instance
        :param value:
        :return:
        """
        self._redis_instance = value

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
            requests_request_func_kwargs_url_path: str = "/old/serverUserAction!checkSession.action",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        check manage login
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return: bool,response.status_code,response.text
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        if not isinstance(self.token_data.get("token", ""), str) or not len(self.token_data.get("token", "")):
            return False, None, None
        if not isinstance(self.token_data.get("companyCode", ""), str) or not len(
                self.token_data.get("companyCode", "")):
            return False, None, None
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            return "null" in response.text.strip(), response.status_code, response.text
        return False, response.status_code, response.text

    def manage_login(
            self,
            requests_request_func_kwargs_url_path: str = "/manage/login",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        manage login
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs: requests.request.kwargs
        :param requests_request_func_response_callable: 
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(json_addict.get("status", -1)) == 100:
                if len(json_addict.get("data", {}).keys()):
                    self.token_data = json_addict.data.to_dict()
                    return True, response.status_code, json_addict
        return False, response.status_code, Dict(response.json())

    def manage_login_with_diskcache(
            self,
            expire_time: float = timedelta(days=15).total_seconds(),
            check_manage_login_func_kwargs: dict = {},
            mange_login_func_kwargs: dict = {},
    ):
        if isinstance(self.diskcache_instance, diskcache.Cache):
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
            self.token_data = self.diskcache_instance.get(key=cache_key, default={})
            state, _, _ = self.check_manage_login(**check_manage_login_func_kwargs)
            if not state:
                state, _, _ = self.manage_login(**mange_login_func_kwargs)
                if state:
                    self.diskcache_instance.set(key=cache_key, value=self.token_data, expire=expire_time)
        else:
            self.manage_login(**mange_login_func_kwargs)
        return self

    def manage_login_with_redis(
            self,
            expire_time: Union[int, timedelta] = timedelta(days=15),
            check_manage_login_func_kwargs: dict = {},
            mange_login_func_kwargs: dict = {},
    ):
        if isinstance(self.redis_instance, (redis.Redis, redis.StrictRedis)):
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
            if isinstance(self.redis_instance.get(name=cache_key), str) and len(
                    self.redis_instance.get(name=cache_key)):
                self.token_data = json.loads(self.redis_instance.get(name=cache_key))
                state, _, _ = self.check_manage_login(**check_manage_login_func_kwargs)
                if not state:
                    state, _, _ = self.manage_login(**mange_login_func_kwargs)
                    if state:
                        self.redis_instance.setex(name=cache_key, value=self.token_data, time=expire_time)
        else:
            self.manage_login(**mange_login_func_kwargs)
        return self

    def manage_communityInfo_getAdminCommunityList(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/communityInfo/getAdminCommunityList",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 项目管理
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_communityRoom_listCommunityRoom(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/communityRoom/listCommunityRoom",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 房号管理 > 有效房号
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_communityRoom_getFullRoomInfo(
            self,
            id: Union[str, int] = "",
            requests_request_func_kwargs_url_path: str = "/manage/communityRoom/getFullRoomInfo",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 房号管理 > 有效房号 > 查看
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if isinstance(id, str) and not len(id):
            raise ValueError("id must be a string and not empty")
        if int(id) <= 0:
            raise ValueError("id must be a positive integer")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_register_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/user/register/list",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册用户管理
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_register_detail(
            self,
            id: str = "",
            requests_request_func_kwargs_url_path: str = "/manage/user/register/detail",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册用户管理 > 查看
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_register_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/user/information/register/list",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册业主管理
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_register_detail(
            self,
            id: str = "",
            org_id: Union[str, int] = "",
            community_id: str = "",
            requests_request_func_kwargs_url_path: str = "/manage/user/information/register/detail",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 注册业主管理 > 查看
        :param community_id:
        :param org_id:
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
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
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_unregister_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/user/information/unregister/list",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 未注册业主管理
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_user_information_unregister_detail(
            self,
            id: str = "",
            community_id: str = "",
            requests_request_func_kwargs_url_path: str = "/manage/user/information/unregister/detail",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        业户中心 > 用户管理 > 未注册业主管理 > 查看
        :param community_id:
        :param org_id:
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
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
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_shopGoods_getAdminShopGoods(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/shopGoods/getAdminShopGoods",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_shopGoods_getShopGoodsDetail(
            self,
            id: str = "",
            requests_request_func_kwargs_url_path: str = "/manage/shopGoods/getShopGoodsDetail",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 查看
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_shopGoods_getGoodsStoreEdits(
            self,
            id: str = "",
            requests_request_func_kwargs_url_path: str = "/manage/shopGoods/getGoodsStoreEdits",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 商家产品 > 推送到门店商品
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_shopGoods_saveGoodsStoreEdits(
            self,
            requests_request_func_kwargs_json: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/shopGoods/saveGoodsStoreEdits",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品 > 保存
        :param requests_request_func_kwargs_json:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_json = Dict(requests_request_func_kwargs_json)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **requests_request_func_kwargs.headers,
        })
        requests_request_func_kwargs.json = Dict({
            **requests_request_func_kwargs_json,
            **requests_request_func_kwargs.json,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_storeProduct_getAdminStoreProductList(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/storeProduct/getAdminStoreProductList",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_storeProduct_getStoreProductInfo(
            self,
            id: str = "",
            requests_request_func_kwargs_url_path: str = "/manage/storeProduct/getStoreProductInfo",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 商品管理 > 门店商品 > 查看
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_businessOrderShu_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/businessOrderShu/list",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 订单管理 > 商业订单
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs_params.setdefault("subHandle", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_businessOrderShu_view(
            self,
            id: str = "",
            order_type: int = 1,
            requests_request_func_kwargs_url_path: str = "/manage/businessOrderShu/view",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        生活服务 > 订单管理 > 商业订单 > 查看
        :param id:
        :param order_type:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not len(id):
            raise ValueError("id must be a string and not empty")
        if not isinstance(order_type, int):
            order_type = 1
        order_type = int(order_type)
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
                "orderType": order_type,
            },
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_carParkApplication_carParkCard_list(
            self,
            requests_request_func_kwargs_params: dict = {},
            requests_request_func_kwargs_url_path: str = "/manage/carParkApplication/carParkCard/list",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权管理
        :param requests_request_func_kwargs_params:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs_params = Dict(requests_request_func_kwargs_params)
        requests_request_func_kwargs_params.setdefault("curPage", 1)
        requests_request_func_kwargs_params.setdefault("pageSize", 20)
        requests_request_func_kwargs_params.setdefault("executeSearch", 1)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())

    def manage_carParkApplication_carParkCard(
            self,
            id: Union[int, str] = "",
            requests_request_func_kwargs_url_path: str = "/manage/carParkApplication/carParkCard",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        智慧物联 > 车场管理 > 停车管理 > 停车授权管理 > 编辑
        :param id:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
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
        if not isinstance(requests_request_func_kwargs_url_path, str):
            raise TypeError("requests_request_func_kwargs_url_path must be a string")
        if not len(requests_request_func_kwargs_url_path):
            raise ValueError("requests_request_func_kwargs_url_path must be a string and not empty")
        if isinstance(id, str) and not len(id):
            raise ValueError("id must be a string and not empty")
        if int(id) <= 0:
            raise ValueError("id must be a positive integer")
        self.token_data = Dict(self.token_data).to_dict()
        self.token_data.setdefault("token", "")
        self.token_data.setdefault("companyCode", "")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
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
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if int(response.json().get("status", -1)) == 100:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict(response.json())
