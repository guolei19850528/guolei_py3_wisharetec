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
from pendulum import instance
from requests import Response
from retrying import retry, RetryError

"""
URL__请求方法__说明
"""
URL__GET__LOGIN_STATE: str = "/old/serverUserAction!checkSession.action"
URL__POST__LOGIN: str = "/manage/login"
URL__GET__COMMUNITY_BY_PAGINATOR: str = "/manage/communityInfo/getAdminCommunityList"
URL__GET__COMMUNITY_DETAIL: str = "/manage/communityInfo/getCommunityInfo"
URL__GET__ROOM_BY_PAGINATOR: str = "/manage/communityRoom/listCommunityRoom"
URL__GET__ROOM_DETAIL: str = "/manage/communityRoom/getFullRoomInfo"
URL__GET__ROOM_EXPORT: str = "/manage/communityRoom/exportDelayCommunityRoomList"
URL__GET__REGISTER_USER_BY_PAGINATOR: str = "/manage/user/register/list"
URL__GET__REGISTER_USER_DETAIL: str = "/manage/user/register/detail"
URL__GET__REGISTER_USER_EXPORT: str = "/manage/user/register/list/export"
URL__GET__REGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/register/list"
URL__GET__REGISTER_OWNER_DETAIL: str = "/manage/user/information/register/detail"
URL__GET__REGISTER_OWNER_EXPORT: str = "/manage/user/information/register/list/export"
URL__GET__UNREGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/unregister/list"
URL__GET__UNREGISTER_OWNER_DETAIL: str = "/manage/user/information/unregister/detail"
URL__GET__UNREGISTER_OWNER_EXPORT: str = "/manage/user/information/unregister/list/export"
URL__GET__SHOP_GOODS_CATEGORY_BY_PAGINATOR: str = "/manage/productCategory/getProductCategoryList"
URL__GET__SHOP_GOODS_BY_PAGINATOR: str = "/manage/shopGoods/getAdminShopGoods"
URL__GET__SHOP_GOODS_DETAIL: str = "/manage/shopGoods/getShopGoodsDetail"
URL__POST__ADD_SHOP_GOODS: str = "/manage/shopGoods/saveSysShopGoods"
URL__POST__UPDATE_SHOP_GOODS: str = "/manage/shopGoods/updateShopGoods"
URL__GET__SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/getGoodsStoreEdits"
URL__POST__SAVE_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/saveGoodsStoreEdits"
URL__GET__STORE_PRODUCT_BY_PAGINATOR: str = "/manage/storeProduct/getAdminStoreProductList"
URL__GET__STORE_PRODUCT_DETAIL: str = "/manage/storeProduct/getStoreProductInfo"
URL__POST__UPDATE_STORE_PRODUCT: str = "/manage/storeProduct/updateStoreProductInfo"
URL__POST__UPDATE_STORE_PRODUCT_STATUS: str = "/manage/storeProduct/updateProductStatus"
URL__GET__BUSINESS_ORDER_BY_PAGINATOR: str = "/manage/businessOrderShu/list"
URL__GET__BUSINESS_ORDER_DETAIL: str = "/manage/businessOrderShu/view"
URL__GET__BUSINESS_ORDER_EXPORT_1: str = "/manage/businessOrder/exportToExcelByOrder"
URL__GET__BUSINESS_ORDER_EXPORT_2: str = "/manage/businessOrder/exportToExcelByProduct"
URL__GET__BUSINESS_ORDER_EXPORT_3: str = "/manage/businessOrder/exportToExcelByOrderAndProduct"
URL__GET__WORK_ORDER_BY_PAGINATOR: str = "/old/orderAction!viewList.action"
URL__GET__WORK_ORDER_DETAIL: str = "/old/orderAction!view.action"
URL__GET__WORK_ORDER_EXPORT: str = "/manage/order/work/export"
URL__GET__PARKING_AUTH_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/list"
URL__GET__PARKING_AUTH_DETAIL: str = "/manage/carParkApplication/carParkCard"
URL__POST__UPDATE_PARKING_AUTH: str = "/manage/carParkApplication/carParkCard"
URL__GET__PARKING_AUTH_AUDIT_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/parkingCardManagerByAudit"
URL__GET__PARKING_AUTH_AUDIT_CHECK_BY_PAGINATOR: str = "/manage/carParkApplication/getParkingCheckList"
URL__UPDATE_PARKING_AUTH_AUDIT_STATUS: str = "/manage/carParkApplication/completeTask"
URL__GET__EXPORT_BY_PAGINATOR: str = "/manage/export/log"


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
        self._base_url = base_url
        self._username = username
        self._password = password
        self._cache_instance = cache_instance
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
    def cache_instance(self):
        return self._cache_instance

    @cache_instance.setter
    def cache_instance(self, cache_instance):
        self._cache_instance = cache_instance

    @property
    def token_data(self):
        return Dict(self._token_data) if isinstance(self._token_data, dict) else Dict()

    @token_data.setter
    def token_data(self, token_data):
        self._token_data = token_data

    def login(self):
        """
        执行登录

        if isinstance(self.cache_instance, diskcache.Cache):usage diskcache

        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):usage redis

        :return:
        """
        # 缓存key
        cache_key = f"guolei_py3_wisharetec_token_data__{self._username}"

        # 判断是否使用缓存
        if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            if isinstance(self.cache_instance, diskcache.Cache):
                self.token_data = self.cache_instance.get(cache_key)
            if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                self.token_data = self.cache_instance.hgetall(cache_key)

        # 检测用户是否登录
        response = requests.get(
            url=f"{self.base_url}{URL__GET__LOGIN_STATE}",
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
            url=f"{self.base_url}{URL__POST__LOGIN}",
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
            response_callable: Callable = None
    ):
        validate(instance=url, schema={"type": "string", "minLength": 1})
        validate(
            instance=self.token_data,
            schema={
                "type": "object",
                "properties": {
                    "token": {"type": "string", "minLength": 1},
                    "companyCode": {"type": "string", "minLength": 1},
                },
                "required": ["token", "companyCode"]})
        url = f"/{url}" if not url.startswith("/") else url
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.get(
            url=f"{self.base_url}{url}",
            params=params,
            **kwargs
        )
        if isinstance(response_callable, Callable):
            return response_callable(response)
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

    def post(
            self,
            url: str = "",
            data: dict = None,
            json: dict = None,
            kwargs: dict = None,
            response_callable: Callable = None
    ):
        validate(instance=url, schema={"type": "string", "minLength": 1})
        validate(
            instance=self.token_data,
            schema={
                "type": "object",
                "properties": {
                    "token": {"type": "string", "minLength": 1},
                    "companyCode": {"type": "string", "minLength": 1},
                },
                "required": ["token", "companyCode"]})
        url = f"/{url}" if not url.startswith("/") else url
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.post(
            url=f"{self.base_url}{url}",
            data=data,
            json=json,
            **kwargs
        )
        if isinstance(response_callable, Callable):
            return response_callable(response)
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

    def put(
            self,
            url: str = "",
            data: dict = None,
            json: dict = None,
            kwargs: dict = None,
            response_callable: Callable = None
    ):
        validate(instance=url, schema={"type": "string", "minLength": 1})
        validate(
            instance=self.token_data,
            schema={
                "type": "object",
                "properties": {
                    "token": {"type": "string", "minLength": 1},
                    "companyCode": {"type": "string", "minLength": 1},
                },
                "required": ["token", "companyCode"]})
        url = f"/{url}" if not url.startswith("/") else url
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", ""),
            },
            **kwargs.headers
        })
        response = requests.put(
            url=f"{self.base_url}{url}",
            data=data,
            json=json,
            **kwargs
        )
        if isinstance(response_callable, Callable):
            return response_callable(response)
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
