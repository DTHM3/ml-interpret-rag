# Makefile for deploying the RAG backend application

# Commands:
# make all		Build everything and deploy to Kubernetes (default)
# make deploy		Build everything and deploy to Kubernetes
# make build		Build just the Docker image
# make frontend		Build just the React frontend
# make docker		Build frontend + Docker image
# make k8s		Apply K8s secrets, deployment, and service
# make restart		Restart backend deployment pod only

APP_NAME=rag-backend
DOCKER_IMAGE=$(APP_NAME):latest

# Default target
.PHONY: all
all: deploy

# Step 1: Build frontend assets
.PHONY: frontend
frontend:
	cd frontend && npm install && npm run build

# Step 2: Build Docker image (with --no-cache)
.PHONY: docker
docker: frontend
	docker build --no-cache -t $(DOCKER_IMAGE) .

# Step 3: Apply k8s manifests
.PHONY: k8s
k8s:
	kubectl apply -f k8s/secret.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml

# Step 4: Restart deployment
.PHONY: restart
restart:
	kubectl rollout restart deployment/$(APP_NAME)

# Combined: make deploy → full dev pipeline
.PHONY: deploy
deploy: docker k8s restart
