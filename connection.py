'''
Weaviate connection with streamlit
'''
from typing import Optional, Dict, Any

import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
from streamlit.errors import StreamlitAPIException
import weaviate
from weaviate.data import DataObject
from weaviate.gql import Query
from weaviate.schema import Schema


CONSISTENCY_LEVEL = weaviate.data.replication.ConsistencyLevel.ALL


class WeaviateConnection(ExperimentalBaseConnection[weaviate.Client]):
    '''
    Weaviate Connection
    '''

    def _connect(self, **kwargs) -> weaviate.Client:
        url = self._get_param('url')
        if not url:
            raise StreamlitAPIException(
                "Missing Weaviate connection param: url")

        # Get auth mode
        # API
        auth_type = self._get_param("auth_type")
        if auth_type == 'API_KEY':
            api_key = self._get_param("api_key")
            if not api_key:
                raise StreamlitAPIException(
                    "Missing Weaviate connection param: api_key")
            auth_config = weaviate.AuthApiKey(api_key=api_key)
        elif auth_type == 'OIDC_OWNER':
            username = self._get_param("username")
            password = self._get_param("password")
            scope = self._get_param("scope")
            if not username:
                raise StreamlitAPIException(
                    "Missing Weaviate connection param: username")
            if not password:
                raise StreamlitAPIException(
                    "Missing Weaviate connection param: password")
            auth_config = weaviate.AuthClientPassword(
                username=username,
                password=password,
                scope=scope
            )
        elif auth_type == 'OIDC_CLIENT':
            client_secret = self._get_param("client_secret")
            scope = self._get_param("scope")
            if not client_secret:
                raise StreamlitAPIException(
                    "Missing Weaviate connection param: client_secret")
            auth_config = weaviate.AuthClientCredentials(
                client_secret=client_secret,
                scope=scope
            )
        elif auth_type == 'OIDC_TOKEN':
            access_token = self._get_param("access_token")
            expires_in = self._get_param("expires_in")
            refresh_token = self._get_param("refresh_token")
            if not access_token:
                raise StreamlitAPIException(
                    "Missing Weaviate connection param: access_token")
            if not expires_in:
                expires_in = 60
            auth_config = weaviate.AuthBearerToken(
                access_token=access_token,
                expires_in=expires_in,
                refresh_token=refresh_token
            )
        else:
            auth_config = None

        if auth_config:
            return weaviate.Client(url=url, auth_client_secret=auth_config, **kwargs)
        return weaviate.Client(url=url, **kwargs)

    def client(self) -> weaviate.Client:
        '''
        Get weaviate client
        '''
        return self._instance

    def query(self) -> Query:
        '''
        Get Query object
        '''
        return self._instance.query

    def is_ready(self):
        """
        Ping Weaviate's ready state

        Returns
        -------
        bool
            True if Weaviate is ready to accept requests,
            False otherwise.
        """
        return self._instance.is_ready()

    def schema(self) -> Schema:
        """
        Get Weaviate's schema

        Returns
        -------
        Schema
        """
        return self._instance.schema

    def data_object(self) -> DataObject:
        """
        Get Weaviate's DataObject

        Returns
        -------
        DataObject
        """
        return self._instance.data_object

    @st.cache_data(ttl=30)
    def get_all(_self, class_name: str) -> Optional[Dict[str, Any]]:
        """
        Gets all objects from Weaviate for class, the maximum number of objects returned is 100.

        Parameters
        ----------
        class_name: str
            The class name of the objects.

        Returns
        -------
        list of dicts
            A list of all objects. If no objects where found the list is empty.
        """
        print(f"Getting all for class {class_name}")
        data_object = _self._instance.data_object
        return data_object.get(class_name=class_name)

    def create(self, data_obj: Dict, class_name: str) -> str:
        """
        Takes a dict describing the object and adds it to Weaviate.

        Parameters
        ----------
        data_object : dict or str
            Object to be added.
            If type is str it should be either a URL or a file.
        class_name : str
            Class name associated with the object given.

        Returns
        -------
        str
            Returns the UUID of the created object if successful.

        """
        data_object = self._instance.data_object
        return data_object.create(data_object=data_obj,
                                  class_name=class_name,
                                  consistency_level=CONSISTENCY_LEVEL
                                  )

    def _get_param(self, key: str, **kwargs) -> str:
        if key in kwargs:
            param = kwargs.pop(key)
        else:
            try:
                param = self._secrets[key]
            except KeyError:
                param = None
        return param
