# End-to-end Grounding Dino flow
- This repo supports you to:
  - Serve your own Grounding Dino API
  - Train or fine-tune Grounding Dino on your own dataset

- Tech stack used in this project:
  - Tensorflow
  - MLFlow
  - Docker
  - K8s
  - FastAPI

- Docker: 
  - To push the image into docker hub, using:
    docker tag [IMAGE ID] [username]:[tag]
    docker push [username]:[tag]
    
- Using Kompose to translate docker-compose to kubernetes resources 
- Installation:
  https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/#install-kompose

