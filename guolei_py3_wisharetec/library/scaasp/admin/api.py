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
from jsonschema.validators import Draft202012Validator, validate


class ApiUrlSettings:
    """
    Url Settings Class
    """

    URL__QUERY_LOGIN_STATE: str = "/old/serverUserAction!checkSession.action"
    URL__LOGIN: str = "/manage/login"
    URL__QUERY_COMMUNITY_BY_PAGINATOR: str = "/manage/communityInfo/getAdminCommunityList"
    URL__QUERY_COMMUNITY_DETAIL: str = "/manage/communityInfo/getCommunityInfo"
    URL__QUERY_ROOM_BY_PAGINATOR: str = "/manage/communityRoom/listCommunityRoom"
    URL__QUERY_ROOM_DETAIL: str = "/manage/communityRoom/getFullRoomInfo"
    URL__QUERY_ROOM_EXPORT: str = "/manage/communityRoom/exportDelayCommunityRoomList"
    URL__QUERY_REGISTER_USER_BY_PAGINATOR: str = "/manage/user/register/list"
    URL__QUERY_REGISTER_USER_DETAIL: str = "/manage/user/register/detail"
    URL__QUERY_REGISTER_USER_EXPORT: str = "/manage/user/register/list/export"
    URL__QUERY_REGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/register/list"
    URL__QUERY_REGISTER_OWNER_DETAIL: str = "/manage/user/information/register/detail"
    URL__QUERY_REGISTER_OWNER_EXPORT: str = "/manage/user/information/register/list/export"
    URL__QUERY_UNREGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/unregister/list"
    URL__QUERY_UNREGISTER_OWNER_DETAIL: str = "/manage/user/information/unregister/detail"
    URL__QUERY_UNREGISTER_OWNER_EXPORT: str = "/manage/user/information/unregister/list/export"
    URL__QUERY_SHOP_GOODS_CATEGORY_BY_PAGINATOR: str = "/manage/productCategory/getProductCategoryList"
    URL__QUERY_SHOP_GOODS_BY_PAGINATOR: str = "/manage/shopGoods/getAdminShopGoods"
    URL__QUERY_SHOP_GOODS_DETAIL: str = "/manage/shopGoods/getShopGoodsDetail"
    URL__SAVE_SHOP_GOODS: str = "/manage/shopGoods/saveSysShopGoods"
    URL__UPDATE_SHOP_GOODS: str = "/manage/shopGoods/updateShopGoods"
    URL__QUERY_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/getGoodsStoreEdits"
    URL__SAVE_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/saveGoodsStoreEdits"
    URL__QUERY_STORE_PRODUCT_BY_PAGINATOR: str = "/manage/storeProduct/getAdminStoreProductList"
    URL__QUERY_STORE_PRODUCT_DETAIL: str = "/manage/storeProduct/getStoreProductInfo"
    URL__UPDATE_STORE_PRODUCT: str = "/manage/storeProduct/updateStoreProductInfo"
    URL__UPDATE_STORE_PRODUCT_STATUS: str = "/manage/storeProduct/updateProductStatus"
    URL__QUERY_BUSINESS_ORDER_BY_PAGINATOR: str = "/manage/businessOrderShu/list"
    URL__QUERY_BUSINESS_ORDER_DETAIL: str = "/manage/businessOrderShu/view"
    URL__QUERY_BUSINESS_ORDER_EXPORT_1: str = "/manage/businessOrder/exportToExcelByOrder"
    URL__QUERY_BUSINESS_ORDER_EXPORT_2: str = "/manage/businessOrder/exportToExcelByProduct"
    URL__QUERY_BUSINESS_ORDER_EXPORT_3: str = "/manage/businessOrder/exportToExcelByOrderAndProduct"
    URL__QUERY_WORK_ORDER_BY_PAGINATOR: str = "/old/orderAction!viewList.action"
    URL__QUERY_WORK_ORDER_DETAIL: str = "/old/orderAction!view.action"
    URL__QUERY_WORK_ORDER_EXPORT: str = "/manage/order/work/export"
    URL__QUERY_PARKING_AUTH_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/list"
    URL__QUERY_PARKING_AUTH_DETAIL: str = "/manage/carParkApplication/carParkCard"
    URL__UPDATE_PARKING_AUTH: str = "/manage/carParkApplication/carParkCard"
    URL__QUERY_PARKING_AUTH_AUDIT_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/parkingCardManagerByAudit"
    URL__QUERY_PARKING_AUTH_AUDIT_CHECK_BY_PAGINATOR: str = "/manage/carParkApplication/getParkingCheckList"
    URL__UPDATE_PARKING_AUTH_AUDIT_STATUS: str = "/manage/carParkApplication/completeTask"
    URL__QUERY_EXPORT_BY_PAGINATOR: str = "/manage/export/log"


class Api(object):
    """
    智慧社区全域服务平台 Admin API Class
    """

    def __init__(
            self,
            base_url: str = "https://sq.wisharetec.com/",
            username: str = None,
            password: str = None,
            cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None
    ):
        """
        Api 构造函数
        :param base_url: 基础url
        :param username: 用户名
        :param password: 密码
        :param cache_instance: 缓存实例
        """
        self._base_url = base_url
        self._username = username
        self._password = password
        self._cache_instance = cache_instance
        self._token_data = Dict()

    @property
    def base_url(self):
        """
        基础url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        """
        基础url
        :param base_url:
        :return:
        """
        self._base_url = base_url

    @property
    def username(self):
        """
        用户名
        :return:
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        用户名
        :param username:
        :return:
        """
        self._username = username

    @property
    def password(self):
        """
        密码
        :return:
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        密码
        :param password:
        :return:
        """
        self._password = password

    @property
    def cache_instance(self):
        """
        缓存实例
        :return:
        """
        return self._cache_instance

    @cache_instance.setter
    def cache_instance(self, cache_instance):
        """
        缓存实例
        :param cache_instance:
        :return:
        """
        self._cache_instance = cache_instance

    @property
    def token_data(self):
        """
        token 数据
        :return:
        """
        return Dict(self._token_data) if isinstance(self._token_data, dict) else Dict()

    @token_data.setter
    def token_data(self, token_data):
        """
        token 数据
        :param token_data:
        :return:
        """
        self._token_data = token_data

    def login(self, custom_callable: Callable = None):
        """
        登录
        :param custom_callable: 自定义回调 custom_callable(self) if isinstance(custom_callable, Callable)
        :return: custom_callable(self) if isinstance(custom_callable, Callable) else addict.Dict instance
        """
        if isinstance(custom_callable, Callable):
            return custom_callable(self)
        validate(instance=self.base_url, schema={"type": "string", "minLength": 1, "pattern": "^http"})
        validate(instance=self.username, schema={"type": "string", "minLength": 1})
        validate(instance=self.password, schema={"type": "string", "minLength": 1})
        # 缓存key
        cache_key = f"guolei_py3_wisharetec_token_data__{self._username}"
        # 使用缓存
        if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            if isinstance(self.cache_instance, diskcache.Cache):
                self.token_data = self.cache_instance.get(cache_key)
            if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                self.token_data = self.cache_instance.hgetall(cache_key)

        # 用户是否登录
        response = requests.get(
            url=f"{self.base_url}{ApiUrlSettings.URL__QUERY_LOGIN_STATE}",
            headers={
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            verify=False,
            timeout=(60, 60)
        )
        if response.status_code == 200:
            if response.text.lower().startswith("null"):
                return self
        response = requests.post(
            url=f"{self.base_url}{ApiUrlSettings.URL__LOGIN}",
            data={
                "username": self.username,
                "password": hashlib.md5(self.password.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            },
            verify=False,
            timeout=(60, 60)
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
                # 缓存处理
                if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
                    if isinstance(self.cache_instance, diskcache.Cache):
                        self.cache_instance.set(
                            key=cache_key,
                            value=self.token_data,
                            expire=timedelta(days=30).total_seconds()
                        )
                    if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                        self.cache_instance.hset(
                            name=cache_key,
                            mapping=self.token_data
                        )
                        self.cache_instance.expire(
                            name=cache_key,
                            time=timedelta(days=30)
                        )
        return self

    def get(
            self,
            url: str = "",
            params: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.get
        :param url: requests.get(url=url,params=params,**kwargs) url=base_url+url if not pattern ^http else url
        :param params: requests.get(url=url,params=params,**kwargs)
        :param kwargs: requests.get(url=url,params=params,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.get(
            url=f"{url}",
            params=params,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
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
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()

    def post(
            self,
            url: str = "",
            data: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.post
        :param url: requests.post(url=url,data=data,**kwargs) url=base_url+url if not pattern ^http else url
        :param data: requests.post(url=url,data=data,**kwargs)
        :param kwargs: requests.post(url=url,data=data,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.post(
            url=url,
            data=data,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
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
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()

    def put(
            self,
            url: str = "",
            data: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.put
        :param url: requests.put(url=url,params=params,**kwargs) url=base_url+url if not pattern ^http else url
        :param data: requests.put(url=url,data=data,**kwargs)
        :param kwargs: requests.put(url=url,data=data,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.put(
            url=url,
            data=data,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
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
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()

    def request(
            self,
            method: str = "GET",
            url: str = "",
            params: dict = None,
            data: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.request
        :param method: requests.request(method=method,url=url,data=data,params=params,**kwargs)
        :param url: requests.request(method=method,url=url,data=data,params=params,**kwargs) url=base_url+url if not pattern ^http else url
        :param params: requests.request(method=method,url=url,data=data,params=params,**kwargs)
        :param data: requests.request(method=method,url=url,data=data,params=params,**kwargs)
        :param kwargs: requests.request(method=method,url=url,data=data,params=params,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
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
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()
