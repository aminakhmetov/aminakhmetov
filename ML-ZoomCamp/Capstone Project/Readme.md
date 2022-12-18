## Machine Learning Zoomcamp 2022 Capstone Project

### General description
This are all materials for the Capstone Project in the context of [Machine Learning Zoomcamp](http://mlzoomcamp.com) 2022 edition.

We use the dataset from [Kitchenware classification](https://www.kaggle.com/competitions/kitchenware-classification) competition on Kaggle that proposes to train a classifier to classify photos of сutlery (kitchenware/kitchen instruments). It is required to register for competition to obtain the dataset.

One can imagine the use of such classifer in online auctions of antiquites/second-hand market/online shops when user downloads its photos to the website and it gives to it an estimate of price and defines correctly the category where one shold sell such cutlery.

### Video-demonstration of the service use in kubernetes cluster
[![Demonstration of how to run proposed service](https://img.youtube.com/vi/Ly-a4dacRjg/0.jpg)](https://youtu.be/Ly-a4dacRjg)

### Instruction on how to build the solution for image recognition classifier:

#### Setting the envorenment
1. Install conda package: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
2. Create conda environment: conda create --name ml-zoomcamp-capstone-project
3. Activate conda environment: conda activate ml-zoomcamp-capstone-project
4. Install python version 3.9.13: conda install -c anaconda python=3.9.13
5. Install python package requirements with pip: pip install -r requirements.txt

#### Download dataset:
1. Register for [Kitchenware classification](https://www.kaggle.com/competitions/kitchenware-classification) competition.
2. Download data to 'kitchenware-classification' folder from the website.

#### Running Jupyter Notebook:
It is highly encouraged to run the jupyter notebook from the server or PC with GPU, as all the analysis takes about 2h on a [server with GPU](https://github.com/DataTalksClub/kitchenware-competition-starter), and takes about 24h to run it on a PC.

#### Training the final classifier:
1. Download data to 'kitchenware-classification' folder.
2. Run the training script (takes about 45 min to run on a PC): python train.py
3. Model will be saved in *.tflite format in 'deployment' directory.

#### Creating Docker Image:
As the model trained we can start preparation for docker image preparation. Please see how to install docker on a PC [here](https://docs.docker.com/get-docker/):
1. Pull the docker image from AWS destined to be employed for AWS Lambda serverless solution:
    docker pull public.ecr.aws/lambda/python:3.9
2. Have Dockerfile in 'deployment' directory.
3. Have lambda_function.py file in 'deployment' directory.
4. Build docker after having changed directory to 'deployment' folder:
    docker build -t cutlery:v001 .
5. Run docker:
    docker run -it --rm -p 8080:8080 cutlery:v001
6. Test docker service:
    python test_local_docker_deployment.py
    
#### Deploying to local kind kubernetes cluster:
Even though the created docker image is ready to be deployed to AWS Lambda serverless solution, we deploy solution locally to local kind kubernetes cluster. Please see the video demonstration [here](https://youtu.be/Ly-a4dacRjg).
1. Install local kind cluster, info [here](https://kind.sigs.k8s.io/docs/user/quick-start). Install kubectl, info [here](https://kubernetes.io/docs/tasks/tools/).
2. Create Kind cluster:
kind create cluster
3. Get info about cluster:
kubectl cluster-info
kubectl get services
4. Load docker image to cluster:
kind load docker-image cutlery:v001
5. Get up deployment and service running:
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
6. Set up port forwarding:
kubectl port-forward service/cutlery 9090:80
7. Test kubernetes deployment:
python test_local_kubernetes_deployment.py
8. Note about port forwarding:
a) docker image/service is listening on 8080 port
b) deployed pod is listening on 8080 port
c) inside the kubernetes service, all requests made to 80 port will transfer to 8080 port of the pod.
d) we will forward all connections from external commands from 9090 port (by test_local_kubernetes_deployement.py) (external outside of Kubernetes) to 80 port of service, which will route it to 8080 port of Kubernetes.

9. Stop kind server: 
kind delete cluster

10. Useful commands:
kubectl get pods // getter of pod
kubectl get deployments // getter of deployment
kubectl get services // getter of service
kubectl scale pod cutlery --replicas 0 // stop pod.
kubectl scale service cutlery --replicas 0 // stop service.

