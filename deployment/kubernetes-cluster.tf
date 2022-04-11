resource "azurerm_kubernetes_cluster" "cluster" {
  name                = "${local.project}-k8s"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${local.project}-k8s"
  tags                = local.default_tags

  lifecycle {
    ignore_changes = [
      default_node_pool.0.node_count,
    ]
  }

  default_node_pool {
    name                = "default"
    node_count          = 2
    vm_size             = "Standard_DS2_v2"
    type                = "VirtualMachineScaleSets"
    enable_auto_scaling = true
    availability_zones  = [1, 2, 3]
    min_count           = 1
    max_count           = 4
  }

  identity {
    type = "SystemAssigned"
  }

  addon_profile {
    aci_connector_linux {
      enabled = false
    }

    azure_policy {
      enabled = false
    }

    http_application_routing {
      enabled = false
    }

    kube_dashboard {
      enabled = false
    }

    oms_agent {
      enabled                    = true
      log_analytics_workspace_id = azurerm_log_analytics_workspace.oms.id
    }
  }
}
