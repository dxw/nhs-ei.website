resource "kubernetes_namespace" "scrapy" {
  metadata {
    name = "scrapy"
  }
}

resource "helm_release" "scrapy" {
  name      = "${local.prefix}-scrapy"
  chart     = "./helm/nhsei-scrapy"
  namespace = kubernetes_namespace.scrapy.metadata.0.name

  set {
    name  = "imageCredentials.registry"
    value = data.azurerm_container_registry.web.login_server
  }

  set {
    name  = "image.tag"
    value = local.scrapy_image_tag
  }

  set {
    name  = "environment.DATABASE_URL"
    value = local.default_postgres_scrapy_db_url
  }

  dynamic "set" {
    for_each = local.scrapy_environment_variables
    content {
      name  = "environment.${set.key}"
      value = set.value
    }
  }
}

data "kubernetes_service" "scrapy" {
  metadata {
    name      = "${helm_release.scrapy.name}-nhsei-scrapy"
    namespace = helm_release.scrapy.namespace
  }
  depends_on = [helm_release.scrapy]
}
