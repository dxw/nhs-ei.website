resource "kubernetes_namespace" "ingress_nginx" {
  metadata {
    name = "ingress-nginx"
  }
}

resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx/"
  chart      = "ingress-nginx"
  namespace  = kubernetes_namespace.ingress_nginx.metadata.0.name

  set {
    name  = "controller.service.externalTrafficPolicy"
    value = "Local"
  }

  set {
    name  = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/azure-dns-label-name"
    value = "${local.prefix}-ingress"
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

data "kubernetes_service" "ingress_nginx_load_balancer" {
  metadata {
    name      = "${helm_release.ingress_nginx.name}-controller"
    namespace = helm_release.ingress_nginx.namespace
  }
  depends_on = [helm_release.ingress_nginx]
}

resource "helm_release" "cert_manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  namespace  = kubernetes_namespace.ingress_nginx.metadata.0.name

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

data "template_file" "kubectl_manifest_letsencrypt_cluster_issuer" {
  template = file("./kubectl-manifests/letsencrypt-cluster-issuer.yml.tpl")

  vars = {
    acme_email  = local.letsencrypt_email
    acme_server = local.letsencrypt_server
  }
}

resource "kubectl_manifest" "letsencrypt_cluster_issuer" {
  count = local.letsencrypt_email != "" && local.letsencrypt_server != "" ? 1 : 0

  validate_schema = true
  yaml_body       = data.template_file.kubectl_manifest_letsencrypt_cluster_issuer.rendered

  depends_on = [
    helm_release.cert_manager
  ]
}
