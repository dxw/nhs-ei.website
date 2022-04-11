resource "kubernetes_namespace" "ingress-nginx" {
  metadata {
    name = "ingress-nginx"
    labels = {
      "cert-manager.io/disable-validation" = true
    }
  }
}

resource "helm_release" "ingress-nginx" {
  name       = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx/"
  chart      = "ingress-nginx"
  namespace  = kubernetes_namespace.ingress-nginx.metadata.0.name

  set {
    name  = "controller.service.externalTrafficPolicy"
    value = "Local"
  }

  set {
    name  = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/azure-dns-label-name"
    value = local.project
  }

  set {
    name  = "controller.nodeSelector.beta\\.kubernetes\\.io/os"
    value = "linux"
    type  = "string"
  }

  set {
    name  = "defaultBackend.nodeSelector.beta\\.kubernetes\\.io/os"
    value = "linux"
    type  = "string"
  }
}

resource "helm_release" "cert-manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  namespace  = kubernetes_namespace.ingress-nginx.metadata.0.name

  set {
    name  = "controller.nodeSelector.beta\\.kubernetes\\.io/os"
    value = "linux"
    type  = "string"
  }

  set {
    name  = "installCRDs"
    value = true
  }
}

data "kubernetes_service" "ingress-load-balancer" {
  metadata {
    name      = "${helm_release.ingress-nginx.name}-controller"
    namespace = helm_release.ingress-nginx.namespace
  }
  depends_on = [helm_release.ingress-nginx]
}
