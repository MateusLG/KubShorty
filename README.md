# Kube-Shorty: Encurtador de URLs com FastAPI e Kubernetes

Kube-Shorty é um serviço de encurtamento de URLs (similar ao bit.ly) construído como um sistema de microsserviços. O objetivo principal deste projeto é demonstrar como desenvolver, containerizar e orquestrar uma aplicação web moderna usando FastAPI, PostgreSQL, Redis e Kubernetes.

## Tecnologias Utilizadas

Este projeto utiliza um stack de tecnologias moderno, focado em performance e escalabilidade.

| Tecnologia | Função | Porquê? |
| :--- | :--- | :--- |
| **FastAPI** | Backend (API) | Framework Python de alta performance, ideal para I/O (rede, DB). Fornece validação de dados nativa (com Pydantic) e documentação automática (`/docs`). |
| **PostgreSQL** | Banco de Dados | A nossa fonte de verdade. Usado para o armazenamento persistente e relacional da URL original com o seu respetivo código curto. |
| **Redis** | Cache (In-Memory DB) | Essencial para a performance. Guarda os códigos curtos mais acedidos na memória para um redirecionamento quase instantâneo, evitando consultas desnecessárias ao PostgreSQL. |
| **Docker / Docker Compose** | Ambiente de Dev | Usado para criar um ambiente de desenvolvimento local idêntico e reprodutível. O `docker-compose.yml` orquestra a API, o DB e o Cache na sua máquina. |
| **Kubernetes (K8s)** | Orquestração | Simula o ambiente de produção. O Kubernetes gere o ciclo de vida dos nossos containers, garantindo que estão sempre no ar, permitindo escalar a API e gerindo a rede interna (Service Discovery). |

## Como Rodar o Projeto

Existem duas formas de executar a aplicação: localmente com Docker Compose (para desenvolvimento) ou num cluster Kubernetes (simulando produção).

### Pré-requisitos

* [Git](https://git-scm.com/downloads)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
    * Certifique-se de que tanto o **Docker Compose** como o **Kubernetes** estão ativados nas configurações do Docker Desktop.

### 1. Instalação

Primeiro, clone o repositório e entre na pasta do projeto:

```bash
git clone (https://github.com/seu-usuario/kube-shorty.git)
cd kube-shorty
```
#### Opção A: Rodar com Docker Compose (Desenvolvimento)
Este modo é o mais simples para testar e desenvolver localmente.
    ```bash
    docker-compose up --build
    # Documentação da API: http://localhost:8000/docs
    ```

#### Opção B: Rodar com Kubernetes (Simulação de Produção)
Este modo utiliza o cluster Kubernetes incluído no Docker Desktop.
Parar o Docker Compose (se estiver a ser executado) Certifique-se de que os containers do docker-compose estão parados para evitar conflitos de porta.

```bash
docker-compose down
# Construir a Imagem Local O Kubernetes do Docker Desktop usa o repositório de imagens local.

docker build -t kube-shorty-api:v1 .
# Aplicar os Manifestos K8s

kubectl apply -f k8s/
# Verificar o Status Irá demorar cerca de um minuto para tudo ficar online. Pode monitorizar o status:

kubectl get pods --watch
# Aguarde até que os 4 pods estejam com o status Running.
```


## Testar a Aplicação
O ficheiro k8s/api-service.yaml cria um Service do tipo LoadBalancer. No Docker Desktop, isto é exposto automaticamente no localhost na porta 80.
- Opção Ideal: Tente aceder no seu navegador: http://localhost/docs (note a ausência da porta :8000)
- Solução (Se o localhost falhar): É comum a rede do LoadBalancer do Docker Desktop falhar. A forma garantida de testar é usar port-forward para se conectar diretamente a um dos Pods da API.
```bash
# 1. Obtenha o nome de um dos seus pods da API
kubectl get pods

# (Copie um dos nomes, ex: api-deployment-6d9f8c47f-abc12)

# 2. Inicie o port-forward (substitua pelo nome do seu pod)
kubectl port-forward <nome-do-pod-da-api> 8080:8000

# Agora, acesse no navegador: http://localhost:8080/docs
```

## Endpoints da API
POST /encurtar Cria uma nova URL encurtada. Corpo (JSON):
```JSON
{
  "url_original": "[https://www.google.com](https://www.google.com)"
}
```
- GET /{codigo_curto} Redireciona para a URL original correspondente. Exemplo: GET /aBcD12
