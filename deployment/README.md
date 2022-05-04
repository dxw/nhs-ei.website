This documentation covers the deployment process and the creation of infrastructure.

## Deployment

## Azure infrastructure

The infrastructure is managed using [Terraform](https://www.terraform.io/).<br>
The state is stored remotely in encrypted Azure storage.<br>
[Terraform workspaces](https://www.terraform.io/docs/state/workspaces.html) are used to separate environments.

### Creating a new environment

When creating a new staging environment you may wish to build it in the same region as
the current live environment.

#### Configuring the storage backend

The Terraform state is stored remotely in Azure, this allows multiple team members to
make changes and means the state file is backed up. The state file contains
sensitive information so access to it should be restricted, and it should be stored
encrypted at rest.

##### Create a new storage backend

The [Azure tutorial](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage) outlines the steps to create a storage account and container for the state file. You will need:

- resource_group_name: The name of the resource group used for the Azure Storage account.
- storage_account_name: The name of the Azure Storage account.
- container_name: The name of the blob container.
- key: The name of the state store file to be created.

##### Create a backend configuration file

Create a new file named `backend.vars` with the following content:

```
resource_group_name  = [the name of the Azure resource group]
storage_account_name = [the name of the Azure Storage account]
container_name       = [the name of the blob container]
key                  = "terraform.tstate"
```

##### Log into azure with the Azure CLI

Install the azure cli:

```
$ brew install az
```

Log in to your account:

```
$ az login
```

Confirm which account you are currently using:

```
$ az account show
```

##### Initialise Terraform

Install the Terraform version manager `tfenv`:

```
$ brew install tfenv
```

Install the required terraform version:

```
$ tfenv install
```

Initialize Terraform to download the required Terraform modules and configure the remote state backend
to use the settings you specified in the previous step.

`$ terraform init -backend-config=backend.vars`

##### Create a Terraform variables file

Copy the `terraform.tfvars.example` to `terraform.tfvars` and modify the contents as required

If you do not wish to create the file, Terraform will ask you to provide the variables
when you run it.

##### Create the infrastructure

Now Terraform has been initialised you can create a workspace. The workspace name is
included in various resources such as the CDN, database, and load balancer.<br>
Do not use a <prefix>-<workspace> combination that already exists unless you know what
you are doing.

`$ terraform workspace new staging`

Switch to the new workspace<br>
`$ terraform workspace select staging`

Plan the changes<br>
`$ terraform plan`

Terraform will ask you to provide any variables not specified in an `*.auto.tfvars` file.
Now you can run:

`$ terraform apply`

If everything looks good, answer `yes` and wait for the new infrastructure to be created.

#### Connecting to the Kubernetes cluster

Install kubectl (The kubernetes cli):

```
$ brew install kubectl
```

Configure kubectl to connect to the Kubernetes cluster:

```
$ az aks get-credentials --resource-group <ResourceGroup> --name <AKSCluster>
```

You should be able to run `kubectl` commands normally, eg:

```
$ kubectl get pods -A
```

#### View the status of Scrapy

Scrapy isn't publically accessable, so we need to use kubectl to port-forward from our local machines to the running service

List the services to find the name of the scrapy service:

```
$ kubectl get services --namespace scrapy
```

Port forward to 8001:

```
$ kubectl port-forward --namespace scrapy service/<ScrapyServiceName> 8001:8001
```

Open http://localhost:8001 in your browser

#### Accessing containers

List the pods to find the one you wish to connect to:

```
$ kubectl list pods -A
```

or also specify the namespace to filter pods:

```
$ kubectl list pods --namespace web
```

Connect to one of the pods returned:

```
$ kubectl exec -ti --namespace web <PodName> -- /bin/bash
```

#### Accessing Postgres

The postgres database can be accessed via the web service or scrapy service.

Connect to one of the containers as described above.

To run a shell in postgres, run:

```
./manage.py dbshell
```

#### Viewing logs

The logs are accessable via the Azure portal

Log in, and navigate to the Kubernetes service console

Select the required kubernetes service

Select 'Services and ingresses'

Select either the web or scrapy service

Select 'Pods'

Select the Pod in the list

Select 'Live logs'

Select the pod from the drop down

You can also select the link 'View in Log Analytics' to view historical logs
