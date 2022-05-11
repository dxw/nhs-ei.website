resource "kubernetes_namespace" "web" {
  metadata {
    name = "web"
  }
}

resource "azurerm_role_assignment" "default_aks_to_web_acr" {
  scope                = data.azurerm_container_registry.web.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.default.kubelet_identity[0].object_id
}

resource "helm_release" "web" {
  name      = "${local.prefix}-web"
  chart     = "./helm/nhsei-website"
  namespace = kubernetes_namespace.web.metadata.0.name

  set {
    name  = "replicaCount"
    value = local.web_replica_count
  }

  set {
    name  = "ingress.hostnames[0]"
    value = local.ingress_hostname
  }

  dynamic "set" {
    for_each = local.custom_apex_domain == "" ? [] : [0]
    content {
      name  = "ingress.hostnames[1]"
      value = "${local.project}-ingress.${terraform.workspace}.${local.custom_apex_domain}"
    }
  }

  dynamic "set" {
    for_each = local.custom_apex_domain == "" ? [] : [0]
    content {
      name  = "ingress.tlshosts[0]"
      value = "${local.project}-ingress.${terraform.workspace}.${local.custom_apex_domain}"
    }
  }

  set {
    name  = "imageCredentials.registry"
    value = data.azurerm_container_registry.web.login_server
  }

  set {
    name  = "image.tag"
    value = local.web_image_tag
  }

  set {
    name  = "environment.DATABASE_URL"
    value = local.default_postgres_web_db_url
  }

  set {
    name  = "environment.WAGTAILSEARCH_URLS"
    value = "http://${data.kubernetes_service.elasticsearch.spec.0.cluster_ip}:9200"
  }

  set {
    name  = "environment.SCRAPY_ENDPOINT"
    value = "http://${data.kubernetes_service.scrapy.spec.0.cluster_ip}:8001/"
  }

  set {
    name  = "environment.AZURE_CONNECTION_STRING"
    value = "DefaultEndpointsProtocol=https;AccountName=${azurerm_storage_account.default.name};AccountKey=${azurerm_storage_account.default.primary_access_key};EndpointSuffix=core.windows.net"
  }

  set {
    name  = "environment.AZURE_CONTAINER"
    value = azurerm_storage_container.web_media.name
  }

  dynamic "set" {
    for_each = local.web_environment_variables
    content {
      name  = "environment.${set.key}"
      value = set.value
    }
  }
}
