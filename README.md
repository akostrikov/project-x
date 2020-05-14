# This project is intented to be deployed with kubernetes.

## Test step is:
Simply run pytest in project folder.

## Build step is:
```docker login
docker build -t akostrikov/first:latest .
docker push akostrikov/first:latest
```


## Deployment step is:
```
kubectl apply -f project-x.yaml
kubectl apply -f project-x-service.yaml

curl --data "@tests/fixtures/input.json" -H "Content-Type: application/json" -X POST 192.168.99.100:30007/trip
```

## Further improvements:
```
Get more test data.
Use Jenkins for testing, building and deployment.
Add configuration, secret, auth.
```