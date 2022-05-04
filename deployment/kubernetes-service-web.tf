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
    name  = "ingress.hostnames[0]"
    value = "${local.prefix}-ingress.${local.azure_region}.cloudapp.azure.com"
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
    name  = "environment.database_url"
    value = local.default_postgres_web_db_url
  }

  set {
    name  = "environment.wagtailsearch_urls"
    value = "http://${data.kubernetes_service.elasticsearch.spec.0.cluster_ip}:9200"
  }

  set {
    name  = "environment.scrapy_endpoint"
    value = "http://${data.kubernetes_service.scrapy.spec.0.cluster_ip}:8001/"
  }

  dynamic "set" {
    for_each = local.web_environment_variables
    content {
      name  = "environment.${set.key}"
      value = set.value
    }
  }
}
