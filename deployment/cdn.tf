resource "azurerm_cdn_profile" "default" {
  name                = "${local.prefix}-default"
  location            = azurerm_resource_group.northeurope.location
  resource_group_name = azurerm_resource_group.northeurope.name
  sku                 = "Standard_Microsoft"
  tags                = local.default_tags
}

resource "azurerm_cdn_endpoint" "default" {
  name                = "${local.prefix}-default"
  location            = azurerm_cdn_profile.default.location
  resource_group_name = azurerm_cdn_profile.default.resource_group_name
  profile_name        = azurerm_cdn_profile.default.name
  tags                = local.default_tags

  origin {
    name      = "${local.prefix}-ingress-load-balancer"
    host_name = local.cdn_origin_host_name
  }
  origin_host_header            = local.cdn_origin_host_name
  querystring_caching_behaviour = "BypassCaching"

  delivery_rule {
    name  = "EnforceHTTPS"
    order = 1
    request_scheme_condition {
      operator     = "Equal"
      match_values = ["HTTP"]
    }
    url_redirect_action {
      redirect_type = "Found"
      protocol      = "Https"
    }
  }
}

resource "azurerm_cdn_endpoint_custom_domain" "default" {
  count = local.cdn_hostname != "" ? 1 : 0

  name            = "default"
  cdn_endpoint_id = azurerm_cdn_endpoint.default.id
  host_name       = local.cdn_hostname

  cdn_managed_https {
    certificate_type = "Dedicated"
    protocol_type    = "ServerNameIndication"
    tls_version      = "TLS12"
  }
}
