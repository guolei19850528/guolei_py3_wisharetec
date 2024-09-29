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
from typing import Union, Callable, Iterator, Any

import diskcache
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator, validate

from guolei_py3_requests.library import (
    request,
    ResponseCallable
)
from requests import Response


class ResponseCallable(ResponseCallable):
    """
    Response Callable Class
    """

    @staticmethod
    def text__start_with_null(response: Response = None, status_code: int = 200):
        text = ResponseCallable.text(response=response, status_code=status_code)
        return isinstance(text, str) and text.startswith("null")

    @staticmethod
    def json_addict__status_is_100__data(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallable.json_addict(response=response, status_code=status_code)
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


class UrlsSetting:
    """
    Urls Settings Class
    """

    QUERY_LOGIN_STATE: str = "/old/serverUserAction!checkSession.action"
    LOGIN: str = "/manage/login"
    QUERY_COMMUNITY_BY_PAGINATOR: str = "/manage/communityInfo/getAdminCommunityList"
    QUERY_COMMUNITY_DETAIL: str = "/manage/communityInfo/getCommunityInfo"
    QUERY_ROOM_BY_PAGINATOR: str = "/manage/communityRoom/listCommunityRoom"
    QUERY_ROOM_DETAIL: str = "/manage/communityRoom/getFullRoomInfo"
    QUERY_ROOM_EXPORT: str = "/manage/communityRoom/exportDelayCommunityRoomList"
    QUERY_REGISTER_USER_BY_PAGINATOR: str = "/manage/user/register/list"
    QUERY_REGISTER_USER_DETAIL: str = "/manage/user/register/detail"
    QUERY_REGISTER_USER_EXPORT: str = "/manage/user/register/list/export"
    QUERY_REGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/register/list"
    QUERY_REGISTER_OWNER_DETAIL: str = "/manage/user/information/register/detail"
    QUERY_REGISTER_OWNER_EXPORT: str = "/manage/user/information/register/list/export"
    QUERY_UNREGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/unregister/list"
    QUERY_UNREGISTER_OWNER_DETAIL: str = "/manage/user/information/unregister/detail"
    QUERY_UNREGISTER_OWNER_EXPORT: str = "/manage/user/information/unregister/list/export"
    QUERY_SHOP_GOODS_CATEGORY_BY_PAGINATOR: str = "/manage/productCategory/getProductCategoryList"
    QUERY_SHOP_GOODS_BY_PAGINATOR: str = "/manage/shopGoods/getAdminShopGoods"
    QUERY_SHOP_GOODS_DETAIL: str = "/manage/shopGoods/getShopGoodsDetail"
    SAVE_SHOP_GOODS: str = "/manage/shopGoods/saveSysShopGoods"
    UPDATE_SHOP_GOODS: str = "/manage/shopGoods/updateShopGoods"
    QUERY_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/getGoodsStoreEdits"
    SAVE_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/saveGoodsStoreEdits"
    QUERY_STORE_PRODUCT_BY_PAGINATOR: str = "/manage/storeProduct/getAdminStoreProductList"
    QUERY_STORE_PRODUCT_DETAIL: str = "/manage/storeProduct/getStoreProductInfo"
    UPDATE_STORE_PRODUCT: str = "/manage/storeProduct/updateStoreProductInfo"
    UPDATE_STORE_PRODUCT_STATUS: str = "/manage/storeProduct/updateProductStatus"
    QUERY_BUSINESS_ORDER_BY_PAGINATOR: str = "/manage/businessOrderShu/list"
    QUERY_BUSINESS_ORDER_DETAIL: str = "/manage/businessOrderShu/view"
    QUERY_BUSINESS_ORDER_EXPORT_1: str = "/manage/businessOrder/exportToExcelByOrder"
    QUERY_BUSINESS_ORDER_EXPORT_2: str = "/manage/businessOrder/exportToExcelByProduct"
    QUERY_BUSINESS_ORDER_EXPORT_3: str = "/manage/businessOrder/exportToExcelByOrderAndProduct"
    QUERY_WORK_ORDER_BY_PAGINATOR: str = "/old/orderAction!viewList.action"
    QUERY_WORK_ORDER_DETAIL: str = "/old/orderAction!view.action"
    QUERY_WORK_ORDER_EXPORT: str = "/manage/order/work/export"
    QUERY_PARKING_AUTH_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/list"
    QUERY_PARKING_AUTH_DETAIL: str = "/manage/carParkApplication/carParkCard"
    UPDATE_PARKING_AUTH: str = "/manage/carParkApplication/carParkCard"
    QUERY_PARKING_AUTH_AUDIT_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/parkingCardManagerByAudit"
    QUERY_PARKING_AUTH_AUDIT_CHECK_BY_PAGINATOR: str = "/manage/carParkApplication/getParkingCheckList"
    UPDATE_PARKING_AUTH_AUDIT_STATUS: str = "/manage/carParkApplication/completeTask"
    QUERY_EXPORT_BY_PAGINATOR: str = "/manage/export/log"


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

    def headers(self, headers: dict = None, is_with_token: bool = True):
        headers = Dict(headers) if headers else Dict()
        if is_with_token:
            headers.setdefault("Token", self.token_data.get("token", ""))
            headers.setdefault("Companycode", self.token_data.get("companyCode", ""))
        return headers.to_dict()

    def login(self, login_callable: Callable = None):
        """
        登录
        :param login_callable: 自定义回调 custom_callable(self) if isinstance(custom_callable, Callable)
        :return: custom_callable(self) if isinstance(custom_callable, Callable) else self
        """
        if isinstance(login_callable, Callable):
            return login_callable(self)
        validate(instance=self.base_url, schema={"type": "string", "minLength": 1, "pattern": "^http"})
        validate(instance=self.username, schema={"type": "string", "minLength": 1})
        validate(instance=self.password, schema={"type": "string", "minLength": 1})
        # 缓存key
        cache_key = f"guolei_py3_wisharetec_token_data__{self.username}"
        # 使用缓存
        if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            if isinstance(self.cache_instance, diskcache.Cache):
                self.token_data = self.cache_instance.get(cache_key)
            if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                self.token_data = self.cache_instance.hgetall(cache_key)

        # 用户是否登录
        result = self.get(
            response_callable=ResponseCallable.text__start_with_null,
            url=f"{UrlsSetting.QUERY_LOGIN_STATE}",
            verify=False,
            timeout=(60, 60)
        )
        if result:
            return self
        result = self.post(
            response_callable=ResponseCallable.json_addict__status_is_100__data,
            url=f"{UrlsSetting.LOGIN}",
            data={
                "username": self.username,
                "password": hashlib.md5(self.password.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            },
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "token": {"type": "string", "minLength": 1},
                "companyCode": {"type": "string", "minLength": 1},
            },
            "required": ["token", "companyCode"],
        }).is_valid(result):
            self.token_data = result
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
            is_with_token=True,
            response_callable: Callable = ResponseCallable.json_addict__status_is_100__data,
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            response_callable=response_callable,
            method="GET",
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )

    def post(
            self,
            response_callable: Callable = ResponseCallable.json_addict__status_is_100__data,
            url: str = None,
            params: Any = None,
            data: Any = None,
            json: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            response_callable=response_callable,
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

    def put(
            self,
            response_callable: Callable = ResponseCallable.json_addict__status_is_100__data,
            url: str = None,
            params: Any = None,
            data: Any = None,
            json: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            response_callable=response_callable,
            method="PUT",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

    def request(
            self,
            response_callable: Callable = ResponseCallable.json_addict__status_is_100__data,
            method: str = "GET",
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        headers = self.headers(headers=headers)
        return request(
            response_callable=response_callable,
            method=method,
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )
