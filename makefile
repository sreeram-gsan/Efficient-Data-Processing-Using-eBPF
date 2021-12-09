VERSION=v3

#build all the docker files in the local
docker_build:
	echo "docker build"
	docker build -f server/dockerfile -t project-server  server/.
	docker build -f extractor/dockerfile -t project-extractor extractor/.
	docker build -f processor/dockerfile -t project-processor processor/.
	docker build -f logs/dockerfile -t project-logs logs/.
	docker build -f reader/dockerfile -t project-reader reader/.
	docker pull rabbitmq
#deploy the whole setup into kubernetes local 
#to check which k8s cluster you are using; command: kubectl config view 
kube_deploy:
	echo "kube deployment"
	kubectl apply -f server/server-deployment.yaml
	kubectl apply -f server/server-service.yaml
	kubectl apply -f server/server-ingress.yaml

	kubectl apply -f extractor/extractor-deployment.yaml
	kubectl apply -f extractor/extractor-service.yaml

	kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
	kubectl apply -f rabbitmq/rabbitmq-service.yaml

	kubectl apply -f processor/processor-deployment.yaml
	kubectl apply -f processor/processor-service.yaml

	kubectl apply -f reader/reader-deployment.yaml

	kubectl apply -f logs/logs-deployment.yaml

#delete all the k8s services that are deployed by the project
kube_delete:
	echo "deleting all services in default"
	kubectl delete pods,ingress,service,deployment --all

#remove all the docker images created by the project
#do delete the k8s dependencies before removing the images; might throw the error that the image is in use
docker_clean:
	echo "clean docker images"
	docker rmi rabbitmq
	docker rmi project-processor
	docker rmi project-server
	docker rmi project-extractor
	docker rmi project-logs
	docker rmi project-reader

#clear docker cache; images are created a new than the from the previous build
docker_clear_cache:
	echo "clear docker cache"
	docker builder prune --all

#clean all the images under the project and clear the cache
docker_deep_clean:
	echo "deep clean docker"
	make docker_clean
	make docker_clear_cache
	
#create the setup of deployment
build:
	make docker_build
	make kube_deploy

#run integration tests
test:
	python3 test/run_test.py

clean:
	make kube_delete
	make docker_deep_clean