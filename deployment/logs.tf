resource "azurerm_log_analytics_workspace" "default_aks_oms_agent" {
  name                = "${local.project}-default-aks-oms-agent"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.default_tags
}
