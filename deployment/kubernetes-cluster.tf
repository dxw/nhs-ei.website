resource "azurerm_kubernetes_cluster" "default" {
  name                = "${local.prefix}-default"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name

  kubernetes_version = local.aks_version
  dns_prefix         = "${local.prefix}-default"

  role_based_access_control_enabled = true

  default_node_pool {
    name                = "default"
    node_count          = local.aks_node_counts["count"]
    min_count           = local.aks_node_counts["min"]
    max_count           = local.aks_node_counts["max"]
    vm_size             = local.aks_vm_size
    type                = "VirtualMachineScaleSets"
    enable_auto_scaling = true
    zones               = local.aks_availability_zones
    vnet_subnet_id      = azurerm_subnet.default_aks_nodes.id
  }

  identity {
    type = "SystemAssigned"
  }

  aci_connector_linux {
    subnet_name = azurerm_subnet.default_aks_nodes.name
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.default_aks_oms_agent.id
  }

  azure_policy_enabled             = false
  http_application_routing_enabled = false

  network_profile {
    network_plugin     = "azure"
    network_policy     = "calico"
    network_mode       = "transparent"
    outbound_type      = "loadBalancer"
    load_balancer_sku  = "standard"
    service_cidr       = cidrsubnet(local.virtual_network_address_space, 8, 0)
    dns_service_ip     = cidrhost(cidrsubnet(local.virtual_network_address_space, 8, 0), 10)
    docker_bridge_cidr = "172.17.0.0/16"
  }

  api_server_authorized_ip_ranges = local.aks_api_authorized_ip_ranges

  lifecycle {
    ignore_changes = [
      default_node_pool.0.node_count,
    ]
  }

  tags = local.default_tags
}
