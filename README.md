# IT4342E - Computer Vision Project
## Contributor

| NAME                | STUDENT ID | ROLE               |
| ------------------- | ---------- | ------------------ |
| Nguyen Thi Hong Anh | 20176679   | Back-end           |
| Nguyen Viet Hoang   | 20176762   | Documents. Denoise |
| Tran Phi Hung       | 20176774   | Model              |
| Nguyen Tri Hung     | 20176773   | Model              |
| Nguyen Manh Phuc    | 20176845   | Front end          |



## Installation

### Using Docker

#### Ubuntu

```shell
bash -x ./deploy.sh
```

#### Windows

```shell
docker build -t foodforfun:1.0 .

docker run \
--name foodforfun \
-p 4321:4321 \
--restart always \
foodforfun:1.0
```

