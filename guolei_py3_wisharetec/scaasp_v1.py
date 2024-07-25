#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
慧享(绿城)科技 智慧社区全域服务平台类库
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
=================================================
"""
import hashlib
import json
from datetime import timedelta
from typing import Iterable, Callable

import redis
from addict import Dict
from diskcache import Cache
import guolei_py3_requests
from requests import Response


class RequestsResponseCallable(guolei_py3_requests.RequestsResponseCallable):
    """
    guolei_py3_wisharetec scaasp_v1 Admin Api RequestsResponseCallable

    you can extend this class to add custom function
    """

    @staticmethod
    def status_code_200_text_is_str_null(response: Response = None):
        return RequestsResponseCallable.status_code_200_text(response=response).strip() == "null"

    @staticmethod
    def status_code_200_json_addict_status_100(response: Response = None):
        json_addict = RequestsResponseCallable.status_code_200_json_addict(response=response)
        return json_addict.status == 100 or json_addict.status == "100"

    @staticmethod
    def status_code_200_json_addict_status_100_data(response: Response = None):
        if RequestsResponseCallable.status_code_200_json_addict_status_100(response=response):
            return RequestsResponseCallable.status_code_200_json_addict(response=response).data
        return Dict({})

    @staticmethod
    def status_code_200_json_addict_status_100_data_result_list(response: Response = None):
        if RequestsResponseCallable.status_code_200_json_addict_status_100(response=response):
            return RequestsResponseCallable.status_code_200_json_addict(response=response).data.resultList
        return Dict({})


class AdminApi(object):
    """
    guolei_py3_wisharetec scaasp_v1 Admin Api

    you can extend this class to add custom function
    """

    def __init__(
            self,
            base_url: str = "",
            uid: str = "",
            pwd: str = "",
            cache_diskcache_instance: Cache = None,
            cache_strict_redis_instance: redis.StrictRedis = None
    ):
        """
        guolei_py3_wisharetec scaasp_v1 Admin Api constructor

        :param base_url: base url
        :param uid: phone number or username
        :param pwd: password
        :param cache_diskcache_instance: diskcache.Cache instance
        :param cache_strict_redis_instance: redis.StrictRedis instance
        """
        self._base_url = base_url
        self._uid = uid
        self._pwd = pwd
        self._token_data = {}
        self._cache_diskcache_instance = cache_diskcache_instance
        self._cache_strict_redis_instance = cache_strict_redis_instance
        self._is_use_token = False

    @property
    def base_url(self) -> str:
        """
        base url if end with "/" then remove end "/"
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value: str):
        """
        base url
        :param value:
        :return:
        """
        self._base_url = value

    @property
    def uid(self) -> str:
        """
        phone number or username
        :return:
        """
        return self._uid

    @uid.setter
    def uid(self, value: str):
        """
        phone number or username
        :param value:
        :return:
        """
        self._uid = value

    @property
    def pwd(self) -> str:
        """
        password
        :return:
        """
        return self._pwd

    @pwd.setter
    def pwd(self, value: str):
        """
        password
        :param value:
        :return:
        """
        self._pwd = value

    @property
    def token_data(self) -> dict:
        """
        token data
        :return:
        """
        return self._token_data

    @token_data.setter
    def token_data(self, value: dict):
        """
        token data
        :param value:
        :return:
        """
        self._token_data = value

    @property
    def cache_diskcache_instance(self) -> Cache:
        """
        diskcache.Cache instance
        :return:
        """
        return self._cache_diskcache_instance

    @cache_diskcache_instance.setter
    def cache_diskcache_instance(self, value: Cache):
        """
        diskcache.Cache instance
        :param value:
        :return:
        """
        self._cache_diskcache_instance = value

    @property
    def cache_strict_redis_instance(self) -> redis.StrictRedis:
        """
        redis.StrictRedis instance
        :return:
        """
        return self._cache_strict_redis_instance

    @cache_strict_redis_instance.setter
    def cache_strict_redis_instance(self, value: redis.StrictRedis):
        """
        redis.StrictRedis instance
        :param value:
        :return:
        """
        self._cache_strict_redis_instance = value

    def requests_request(
            self,
            path: str = "",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ):
        """
        call guolei_py3_requests.requests_request
        :param path: path
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return: return guolei_py3_requests.requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs.setdefault("method", "GET")
        requests_request_kwargs.setdefault("url", f"{self.base_url}{path}")
        if self._is_use_token:
            token_data = Dict(self.token_data)
            token_data.setdefault("token", "")
            token_data.setdefault("Companycode", "")
            requests_request_kwargs.headers = {
                **requests_request_kwargs.headers,
                "Token": token_data.token,
                "Companycode": token_data.companyCode,
            }
        return guolei_py3_requests.requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs.to_dict(),
        )

    def check_login(
            self,
            path: str = "/old/serverUserAction!checkSession.action",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_text_is_str_null,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ):
        """
        check login
        :param path: path
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return: bool if is login return True else return False
        """
        token_data = Dict(self.token_data)
        token_data.setdefault("token", "")
        token_data.setdefault("Companycode", "")
        if not len(token_data.keys()):
            return False
        if not isinstance(token_data.token, str):
            return False
        if not len(token_data.token):
            return False
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "method": "GET",
            "headers": {
                "Token": token_data.token,
                "Companycode": token_data.companyCode,
            },
            **requests_request_kwargs,
        })
        return self.requests_request(
            path=path,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def login(
            self,
            path: str = "/manage/login",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ):
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "method": "POST",
            "data": {
                "username": self.uid,
                "password": hashlib.md5(self.pwd.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            },
            **requests_request_kwargs,
        })
        token_data = self.requests_request(
            path=path,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
        token_data = Dict(token_data)
        if not len(token_data.keys()):
            return False
        token_data.setdefault("token", "")
        token_data.setdefault("Companycode", "")
        if not len(token_data.token):
            return False
        self.token_data = token_data
        return True

    def login_with_strict_redis(
            self,
            cache_strict_redis_instance: redis.StrictRedis = None,
            cache_expire=timedelta(days=90),
            check_login_path: str = "/old/serverUserAction!checkSession.action",
            check_login_requests_response_callable: Callable = RequestsResponseCallable.status_code_200_text_is_str_null,
            check_login_requests_request_args: Iterable = (),
            check_login_requests_request_kwargs: dict = {},
            login_path: str = "/manage/login",
            login_requests_response_callable: Callable = RequestsResponseCallable.status_code_200_text_is_str_null,
            login_requests_request_args: Iterable = (),
            login_requests_request_kwargs: dict = {}
    ):
        cache_key = "_".join([
            f"guolei_py3_wisharetec",
            f"scaasp_v1",
            f"AdminApi",
            f"redis",
            f"token_data",
            f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
            f"{self.uid}",
        ])
        if cache_strict_redis_instance is None or not isinstance(cache_strict_redis_instance, redis.StrictRedis):
            cache_strict_redis_instance = self.cache_strict_redis_instance
        if isinstance(cache_strict_redis_instance, redis.StrictRedis):
            self.token_data = Dict(json.loads(cache_strict_redis_instance.get(cache_key)))
        if not self.check_login(
                path=check_login_path,
                requests_response_callable=check_login_requests_response_callable,
                requests_request_args=check_login_requests_request_args,
                requests_request_kwargs=check_login_requests_request_kwargs
        ):
            if self.login(
                    path=login_path,
                    requests_response_callable=login_requests_response_callable,
                    requests_request_args=login_requests_request_args,
                    requests_request_kwargs=login_requests_request_kwargs
            ):
                if isinstance(cache_strict_redis_instance, redis.StrictRedis):
                    cache_strict_redis_instance.setex(
                        name=cache_key,
                        value=json.dumps(self.token_data),
                        time=cache_expire
                    )
        self._is_use_token = True
        return self

    def login_with_diskcache(
            self,
            cache_diskcache_instance: Cache = None,
            cache_expire=timedelta(days=90).total_seconds(),
            check_login_path: str = "/old/serverUserAction!checkSession.action",
            check_login_requests_response_callable: Callable = RequestsResponseCallable.status_code_200_text_is_str_null,
            check_login_requests_request_args: Iterable = (),
            check_login_requests_request_kwargs: dict = {},
            login_path: str = "/manage/login",
            login_requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            login_requests_request_args: Iterable = (),
            login_requests_request_kwargs: dict = {}
    ):
        cache_key = "_".join([
            f"guolei_py3_wisharetec",
            f"scaasp_v1",
            f"AdminApi",
            f"diskcache",
            f"token_data",
            f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
            f"{self.uid}",
        ])

        if cache_diskcache_instance is None or not isinstance(cache_diskcache_instance, Cache):
            cache_diskcache_instance = self.cache_diskcache_instance
        if isinstance(cache_diskcache_instance, Cache):
            self.token_data = cache_diskcache_instance.get(cache_key, {})
        if not self.check_login(
                path=check_login_path,
                requests_response_callable=check_login_requests_response_callable,
                requests_request_args=check_login_requests_request_args,
                requests_request_kwargs=check_login_requests_request_kwargs
        ):
            if self.login(
                    path=login_path,
                    requests_response_callable=login_requests_response_callable,
                    requests_request_args=login_requests_request_args,
                    requests_request_kwargs=login_requests_request_kwargs
            ):
                if isinstance(cache_diskcache_instance, Cache):
                    cache_diskcache_instance.set(
                        key=cache_key,
                        value=self.token_data,
                        expire=cache_expire
                    )
        self._is_use_token = True
        return self

    def login_with_cache(
            self,
            cache_type: str = "diskcache",
            cache_instance=None,
            cache_expire=timedelta(days=90).total_seconds(),
            check_login_path: str = "/old/serverUserAction!checkSession.action",
            check_login_requests_response_callable: Callable = RequestsResponseCallable.status_code_200_text_is_str_null,
            check_login_requests_request_args: Iterable = (),
            check_login_requests_request_kwargs: dict = {},
            login_path: str = "/manage/login",
            login_requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            login_requests_request_args: Iterable = (),
            login_requests_request_kwargs: dict = {}
    ):
        if not isinstance(cache_type, str):
            cache_type = "diskcache"
        if not len(cache_type):
            cache_type = "diskcache"
        if "diskcache" in cache_type.lower():
            return self.login_with_diskcache(
                cache_diskcache_instance=cache_instance,
                cache_expire=cache_expire,
                check_login_path=check_login_path,
                check_login_requests_response_callable=check_login_requests_response_callable,
                check_login_requests_request_args=check_login_requests_request_args,
                check_login_requests_request_kwargs=check_login_requests_request_kwargs,
                login_path=login_path,
                login_requests_response_callable=login_requests_response_callable,
                login_requests_request_args=login_requests_request_args,
                login_requests_request_kwargs=login_requests_request_kwargs
            )
        if "strict_redis" in cache_type.lower():
            return self.login_with_strict_redis(
                cache_strict_redis_instance=cache_instance,
                cache_expire=cache_expire,
                check_login_path=check_login_path,
                check_login_requests_response_callable=check_login_requests_response_callable,
                check_login_requests_request_args=check_login_requests_request_args,
                check_login_requests_request_kwargs=check_login_requests_request_kwargs,
                login_path=login_path,
                login_requests_response_callable=login_requests_response_callable,
                login_requests_request_args=login_requests_request_args,
                login_requests_request_kwargs=login_requests_request_kwargs
            )
        self.login()
        self._is_use_token = True
        return self
