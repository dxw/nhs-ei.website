resource "azurerm_log_analytics_workspace" "oms" {
  name                = "${local.project}-oms"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.default_tags
}

resource "azurerm_log_analytics_solution" "containers" {
  solution_name         = "Containers"
  workspace_resource_id = azurerm_log_analytics_workspace.oms.id
  workspace_name        = azurerm_log_analytics_workspace.oms.name
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/Containers"
  }
}
