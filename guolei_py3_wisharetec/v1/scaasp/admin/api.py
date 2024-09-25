#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者:[郭磊]
手机:[5210720528]
email:[174000902@qq.com]
github:[https://github.com/guolei19850528/guolei_py3_wisharetec]
=================================================
"""
import hashlib
import pathlib
from datetime import timedelta
from typing import Union, Callable, Iterator

import diskcache
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response
from retrying import retry, RetryError

# api urls addict
api_urls_addict = Dict()
# 是否登录
api_urls_addict.is_login = "/old/serverUserAction!checkSession.action"
# 登录
api_urls_addict.login = "/manage/login"

api_urls_addict.query_community_with_paginator = "/manage/communityInfo/getAdminCommunityList"
api_urls_addict.query_community_detail = "/manage/communityInfo/getCommunityInfo"
api_urls_addict.query_room_no_with_paginator = "/manage/communityRoom/listCommunityRoo"
api_urls_addict.query_room_no_detail = "/manage/communityRoom/getFullRoomInfo"
api_urls_addict.room_no_export = "/manage/communityRoom/exportDelayCommunityRoomList"
api_urls_addict.query_register_user_with_paginator = "/manage/user/register/list"
api_urls_addict.query_register_user_detail = "/manage/user/register/detail"
api_urls_addict.register_user_export = "/manage/user/register/list/export"
api_urls_addict.query_register_owner_with_paginator = "/manage/user/information/register/list"
api_urls_addict.query_register_owner_detail = "/manage/user/information/register/detail"
api_urls_addict.register_owner_export = "/manage/user/information/register/list/export"
api_urls_addict.query_unregister_owner_with_paginator = "/manage/user/information/unregister/list"
api_urls_addict.query_unregister_owner_detail = "/manage/user/information/unregister/detail"
api_urls_addict.unregister_owner_export = "/manage/user/information/unregister/list/export"
api_urls_addict.query_shop_goods_category_with_paginator = "/manage/productCategory/getProductCategoryList"
api_urls_addict.query_shop_goods_with_paginator = "/manage/shopGoods/getAdminShopGoods"
api_urls_addict.query_shop_goods_detail = "/manage/shopGoods/getShopGoodsDetail"
api_urls_addict.add_shop_goods = "/manage/shopGoods/saveSysShopGoods"
api_urls_addict.update_shop_goods = "/manage/shopGoods/updateShopGoods"
api_urls_addict.query_shop_goods_push_to_store = "/manage/shopGoods/getGoodsStoreEdits"
api_urls_addict.save_shop_goods_push_to_store = "/manage/shopGoods/saveGoodsStoreEdits"
api_urls_addict.query_store_product_with_paginator = "/manage/storeProduct/getAdminStoreProductList"
api_urls_addict.query_store_product_detail = "/manage/storeProduct/getStoreProductInfo"
api_urls_addict.update_store_product = "/manage/storeProduct/updateStoreProductInfo"
api_urls_addict.update_store_product_status = "/manage/storeProduct/updateProductStatus"
api_urls_addict.query_business_order_with_paginator = "/manage/businessOrderShu/list"
api_urls_addict.query_business_order_detail = "/manage/businessOrderShu/view"
api_urls_addict.business_order_export_1 = "/manage/businessOrder/exportToExcelByOrder"
api_urls_addict.business_order_export_1 = "/manage/businessOrder/exportToExcelByProduct"
api_urls_addict.business_order_export_1 = "/manage/businessOrder/exportToExcelByOrderAndProduct"
api_urls_addict.query_work_order_with_paginator = "/old/orderAction!viewList.action"
api_urls_addict.query_work_order_detail = "/old/orderAction!view.action"
api_urls_addict.work_order_export = "/manage/order/work/export"
api_urls_addict.query_parking_auth_with_paginator = "/manage/carParkApplication/carParkCard/list"
api_urls_addict.query_parking_auth_detail = "/manage/carParkApplication/carParkCard"
api_urls_addict.update_parking_auth = "/manage/carParkApplication/carParkCard"
api_urls_addict.query_parking_auth_audit_with_paginator = "/manage/carParkApplication/carParkCard/parkingCardManagerByAudit"
api_urls_addict.query_parking_auth_audit_check_with_paginator = "/manage/carParkApplication/getParkingCheckList"
api_urls_addict.update_parking_auth_audit_status = "/manage/carParkApplication/completeTask"
api_urls_addict.query_export_with_paginator = "/manage/export/log"


class Api(object):
    """
    智慧社区全域服务平台 Admin API Class
    """

    def __init__(
            self,
            base_url: str = "https://sq.wisharetec.com/",
            username: str = None,
            password: str = None,
            diskcache_instance: diskcache.Cache = None,
            redis_instance: Union[redis.Redis, redis.StrictRedis] = None
    ):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._diskcache_instance = diskcache_instance
        self._redis_instance = redis_instance
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
    def diskcache_instance(self):
        return self._diskcache_instance

    @diskcache_instance.setter
    def diskcache_instance(self, diskcache_instance):
        self._diskcache_instance = diskcache_instance

    @property
    def redis_instance(self):
        return self._redis_instance

    @redis_instance.setter
    def redis_instance(self, redis_instance):
        self._redis_instance = redis_instance

    @property
    def token_data(self):
        return Dict(self._token_data) if isinstance(self._token_data, dict) else Dict()

    @token_data.setter
    def token_data(self, token_data):
        self._token_data = token_data

    def request(
            self,
            request_func_kwargs_url_path: str = None,
            request_func_kwargs=None,
            request_func_response_callable: Callable = None,
    ):
        """
        call request.request()
        :param request_func_kwargs_url_path: request_func_kwargs.url=f"{self.base_url}{request_func_kwargs_url_path}"
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: return request_func_response_callable(response,request_func_kwargs) if isinstance(request_func_response_callable, Callable)
        :return:
        """
        request_func_kwargs = Dict(request_func_kwargs) if isinstance(request_func_kwargs, dict) else Dict()
        request_func_kwargs.setdefault("url", f"{self.base_url}{request_func_kwargs_url_path}")
        request_func_kwargs.setdefault("method", f"GET")
        response = requests.request(**request_func_kwargs.to_dict())
        if isinstance(request_func_response_callable, Callable):
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
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def request_with_token(
            self,
            request_func_kwargs_url_path: str = None,
            request_func_kwargs: dict = None,
            request_func_response_callable: Callable = None,
    ):
        """
        call self.request() with token

        usage:
            >>> from guolei_py3_wisharetec.v1.scaasp.admin.api import Api as AdminApi
            >>> admin_api=AdminApi()
            >>> admin_api.login().request_with_token()
            >>> admin_api.login_with_diskcache().request_with_token()
        :param request_func_kwargs_url_path: request_func_kwargs.url=f"{self.base_url}{request_func_kwargs_url_path}"
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: return request_func_response_callable(response,request_func_kwargs) if isinstance(request_func_response_callable, Callable)
        :return:
        """
        request_func_kwargs = Dict(request_func_kwargs) if isinstance(request_func_kwargs, dict) else Dict()
        request_func_kwargs.headers = Dict(
            {
                **{
                    "Token": self.token_data.get("token", ""),
                    "Companycode": self.token_data.get("companyCode", ""),
                },
                **request_func_kwargs.headers,
            }
        )
        return self.request(
            request_func_kwargs_url_path=request_func_kwargs_url_path,
            request_func_kwargs=request_func_kwargs,
            request_func_response_callable=request_func_response_callable
        )

    def is_login(
            self,
            request_func_kwargs_url_path: str = api_urls_addict.is_login,
            request_func_kwargs: dict = None,
            request_func_response_callable: Callable = None
    ):
        """
        是登录
        :param request_func_kwargs_url_path: request_func_kwargs.url=f"{self.base_url}{request_func_kwargs_url_path}"
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: return request_func_response_callable(response,request_func_kwargs) if isinstance(request_func_response_callable, Callable)
        :return:
        """
        if not isinstance(request_func_response_callable, Callable):
            request_func_response_callable = lambda x, y: x.text.lower().startswith("null")
        return self.request_with_token(
            request_func_kwargs_url_path=request_func_kwargs_url_path,
            request_func_kwargs=request_func_kwargs,
            request_func_response_callable=request_func_response_callable
        )

    def login(
            self,
            request_func_kwargs_url_path: str = api_urls_addict.login,
            request_func_kwargs: dict = None,
            request_func_response_callable: Callable = None
    ):
        """
        登录
        :param request_func_kwargs_url_path: request_func_kwargs.url=f"{self.base_url}{request_func_kwargs_url_path}"
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: return request_func_response_callable(response,request_func_kwargs) if isinstance(request_func_response_callable, Callable)
        :return:
        """
        request_func_kwargs = Dict(request_func_kwargs) if isinstance(request_func_kwargs, dict) else Dict()
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.data = Dict({
            **{
                "username": self.username,
                "password": hashlib.md5(self.password.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            },
            **request_func_kwargs.data,
        })
        if not isinstance(request_func_response_callable, Callable):
            request_func_response_callable = lambda x, y: x
        response: Response = self.request(
            request_func_kwargs_url_path=request_func_kwargs_url_path,
            request_func_kwargs=request_func_kwargs,
            request_func_response_callable=request_func_response_callable
        )
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
                    "data": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string", "minLength": 1},
                            "companyCode": {"type": "string", "minLength": 1},
                        },
                        "required": ["token", "companyCode"],
                    }
                },
                "required": ["status", "data"]
            }).is_valid(response.json()):
                self.token_data = Dict(response.json()).data
        return self

    def login_with_diskcache(
            self,
            key: str = None,
            expire: float = None,
            is_login_func_kwargs: dict = None,
            login_func_kwargs: dict = None
    ):
        """
        使用diskcache登录
        :param key: 缓存key
        :param expire: 过期时间
        :param is_login_func_kwargs: self.is_login(**is_login_func_kwargs)
        :param login_func_kwargs: self.login(**login_func_kwargs)
        :return:
        """
        is_login_func_kwargs = Dict(is_login_func_kwargs) if is_login_func_kwargs else Dict()
        login_func_kwargs = Dict(login_func_kwargs) if is_login_func_kwargs else Dict()
        if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(key):
            key = "_".join(["guolei_py3_wisharetec_scaasp_admin_api_diskcache_token_data_", self.username])
        if isinstance(self.diskcache_instance, diskcache.Cache):
            self.token_data = self.diskcache_instance.get(key=key, default=Dict())
            if not self.is_login(**is_login_func_kwargs):
                self.login(**login_func_kwargs)
                self.diskcache_instance.set(key=key, value=self.token_data, expire=expire)
        return self

    def login_with_redis(
            self,
            key: str = None,
            expire: Union[int, timedelta] = None,
            is_login_func_kwargs: dict = None,
            login_func_kwargs: dict = None
    ):
        """
        使用redis登录
        :param key: 缓存key
        :param expire: 过期时间
        :param is_login_func_kwargs: self.is_login(**is_login_func_kwargs)
        :param login_func_kwargs: self.login(**login_func_kwargs)
        :return:
        """
        is_login_func_kwargs = Dict(is_login_func_kwargs) if is_login_func_kwargs else Dict()
        login_func_kwargs = Dict(login_func_kwargs) if is_login_func_kwargs else Dict()
        if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(key):
            key = "_".join(["guolei_py3_wisharetec_scaasp_admin_api_redis_token_data_", self.username])
        if isinstance(self.redis_instance, (redis.Redis, redis.StrictRedis)):
            self.token_data = self.redis_instance.hgetall(name=key)
            if not self.is_login(**is_login_func_kwargs):
                self.login(**login_func_kwargs)
                self.redis_instance.hset(name=key, mapping=self.token_data)
                self.redis_instance.expire(name=key, time=expire)

        return self

    def login_with_cache(
            self,
            types: str = "diskcache",
            login_with_cache_func_kwargs: dict = None,
    ):
        """
        使用缓存登录
        :param types: 类型 diskcache || redis
        :param login_with_cache_func_kwargs: self.login_with_redis(**login_with_cache_func_kwargs) || self.login_with_diskcache(**login_with_cache_func_kwargs)
        :return:
        """
        login_with_cache_func_kwargs = Dict(login_with_cache_func_kwargs) if login_with_cache_func_kwargs else Dict()
        if types.lower() == "redis":
            return self.login_with_redis(
                **login_with_cache_func_kwargs
            )
        return self.login_with_diskcache(
            **login_with_cache_func_kwargs
        )

    def download_export_with_id(
            self,
            export_id: Union[str, int] = 0,
            download_path: str = None,
            query_export_with_paginator_func_kwargs: dict = None,
            login_with_cache_func_kwargs: dict = None,
            retry_func_kwargs: dict = None
    ):
        """
        使用 ID 下载导出
        :param export_id: 导出ID
        :param download_path: 下载路径
        :param query_export_with_paginator_func_kwargs: 分页查询导出数据参数
        :param login_with_cache_func_kwargs: 缓存登录参数
        :param retry_func_kwargs: 重试参数
        :return:
        """
        login_with_cache_func_kwargs = Dict(
            login_with_cache_func_kwargs) if login_with_cache_func_kwargs else Dict()
        query_export_with_paginator_func_kwargs = Dict(
            query_export_with_paginator_func_kwargs) if query_export_with_paginator_func_kwargs else Dict()
        query_export_with_paginator_func_kwargs.setdefault(
            "request_func_kwargs_url_path",
            api_urls_addict.query_export_with_paginator
        )
        query_export_with_paginator_func_kwargs.setdefault("request_func_kwargs", Dict())
        query_export_with_paginator_func_kwargs.request_func_kwargs.setdefault("method", "GET")
        query_export_with_paginator_func_kwargs.request_func_kwargs.setdefault("verify", False)
        query_export_with_paginator_func_kwargs.request_func_kwargs.setdefault("timeout", (60, 60))
        query_export_with_paginator_func_kwargs.request_func_kwargs.params = Dict({
            **{
                "executeSearch": 1,
                "curPage": 1,
                "pageSize": 50,
            },
            **query_export_with_paginator_func_kwargs.request_func_kwargs.params,
        })
        retry_func_kwargs = Dict(retry_func_kwargs) if retry_func_kwargs else Dict()
        retry_func_kwargs.setdefault("stop_max_attempt_number", timedelta(minutes=60).seconds)
        retry_func_kwargs.setdefault("wait_fixed", timedelta(seconds=10).seconds * 1000)

        @retry(**retry_func_kwargs)
        def _retry_func(
                export_id: Union[str, int] = 0,
                download_path: str = None,
                query_export_with_paginator_func_kwargs: dict = None,
                login_with_cache_func_kwargs: dict = None,
        ):
            export_with_paginator = self.login_with_cache(
                **login_with_cache_func_kwargs
            ).request_with_token(
                **query_export_with_paginator_func_kwargs
            )
            if Draft202012Validator({
                "type": "object",
                "properties": {"resultList": {"type": "array", "minItems": 1}},
                "required": ["resultList"]
            }).is_valid(export_with_paginator):
                for i in export_with_paginator.resultList:
                    if Draft202012Validator({
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "const": export_id},
                            "status": {"type": "integer", "const": 2},
                            "filePath": {"type": "string", "minLength": 1},
                        }
                    }).is_valid(i):
                        if "".join(pathlib.Path(i.filePath).suffixes).lower() not in "".join(
                                pathlib.Path(download_path).suffixes).lower():
                            download_path = f"{download_path}{''.join(pathlib.Path(i.filePath).suffixes)}"
                        response = requests.get(i.filePath)
                        with open(download_path, "wb") as f:
                            f.write(response.content)
                        return download_path
                    raise RetryError("download_export_with_id func error")
            raise RetryError("download_export_with_id func error")

        return _retry_func(
            export_id=export_id,
            download_path=download_path,
            query_export_with_paginator_func_kwargs=query_export_with_paginator_func_kwargs,
            login_with_cache_func_kwargs=login_with_cache_func_kwargs
        )
