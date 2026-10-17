from typing import Dict, Any, List, Optional
from meilisearch import Client
from dataclasses import dataclass


@dataclass
class SearchSettings:
    displayedAttributes: Optional[List[str]] = None
    searchableAttributes: Optional[List[str]] = None
    filterableAttributes: Optional[List[str]] = None
    sortableAttributes: Optional[List[str]] = None
    rankingRules: Optional[List[str]] = None
    stopWords: Optional[List[str]] = None
    synonyms: Optional[Dict[str, List[str]]] = None
    distinctAttribute: Optional[str] = None
    typoTolerance: Optional[Dict[str, Any]] = None
    faceting: Optional[Dict[str, Any]] = None
    pagination: Optional[Dict[str, Any]] = None


class SettingsManager:
    """Manage Meilisearch index settings"""

    def __init__(self, client: Client):
        self.client = client

    def get_settings(self, index_uid: str) -> Dict[str, Any]:
        """Get all settings for an index"""
        try:
            index = self.client.index(index_uid)
            return index.get_settings()
        except Exception as e:
            raise Exception(f"Failed to get settings: {str(e)}")

    def update_settings(
        self, index_uid: str, settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update settings for an index"""
        try:
            index = self.client.index(index_uid)
            return index.update_settings(settings)
        except Exception as e:
            raise Exception(f"Failed to update settings: {str(e)}")

    def reset_settings(self, index_uid: str) -> Dict[str, Any]:
        """Reset settings to default values"""
        try:
            index = self.client.index(index_uid)
            return index.reset_settings()
        except Exception as e:
            raise Exception(f"Failed to reset settings: {str(e)}")

    def get_embedders(self, index_uid: str) -> Dict[str, Any]:
        """Get the embedder configuration for an index"""
        try:
            index = self.client.index(index_uid)
            return index.get_embedders()
        except Exception as e:
            raise Exception(f"Failed to get embedders: {str(e)}")

    def update_embedders(
        self, index_uid: str, embedders: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the embedder configuration for an index"""
        try:
            index = self.client.index(index_uid)
            return index.update_embedders(embedders)
        except Exception as e:
            raise Exception(f"Failed to update embedders: {str(e)}")

    def reset_embedders(self, index_uid: str) -> Dict[str, Any]:
        """Reset/remove the embedder configuration for an index"""
        try:
            index = self.client.index(index_uid)
            return index.reset_embedders()
        except Exception as e:
            raise Exception(f"Failed to reset embedders: {str(e)}")
