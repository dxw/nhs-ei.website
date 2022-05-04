resource "kubernetes_namespace" "elasticsearch" {
  metadata {
    name = "elasticsearch"
  }
}

resource "helm_release" "elasticsearch" {
  name       = "${local.prefix}-elasticsearch"
  repository = "https://helm.elastic.co"
  chart      = "elasticsearch"
  namespace  = kubernetes_namespace.elasticsearch.metadata.0.name
  timeout    = 600

  set {
    name  = "antiAffinity"
    value = "soft"
  }

  set {
    name  = "esJavaOpts"
    value = "-Xmx128m -Xms128m"
  }

  set {
    name  = "resources.requests.cpu"
    value = "100m"
  }

  set {
    name  = "resources.requests.memory"
    value = "512M"
  }

  set {
    name  = "resources.limits.cpu"
    value = "1000m"
  }

  set {
    name  = "resources.limits.memory"
    value = "512M"
  }

  set {
    name  = "volumeClaimTemplate.accessModes[0]"
    value = "ReadWriteOnce"
  }

  set {
    name  = "volumeClaimTemplate.storageClassName"
    value = "default"
  }

  set {
    name  = "volumeClaimTemplate.resources.requests.storage"
    value = "50Gi"
  }
}

data "kubernetes_service" "elasticsearch" {
  metadata {
    name      = "elasticsearch-master"
    namespace = helm_release.elasticsearch.namespace
  }
  depends_on = [helm_release.elasticsearch]
}
