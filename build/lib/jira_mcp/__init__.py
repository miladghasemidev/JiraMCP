"""Jira MCP on-premises implementation."""

from jira_mcp.executor import JiraToolExecutor
from jira_mcp.inventory import Capability, Inventory

__all__ = ["Capability", "Inventory", "JiraToolExecutor"]
__version__ = "1.0.0"
