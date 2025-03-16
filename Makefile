build-dev:
	docker build . -t opinion-galaxy  --platform linux/amd64 -f dev/Dockerfile.dev
run-dev:
	docker run --privileged -it --platform linux/amd64 -e FIREBASE_API_KEY="" -v /Users/yuhiaoki/dev/opinion-galaxy-mvp/data/database:/var/lib/litefs -p 8080:8080 -p 20202:20202 -t opinion-galaxy
builde:
	docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/emerald-cab-354713/opinion-galaxy-export-job/opinion-galaxy-export-image -f export/Dockerfile.export .

pushe:
	docker push asia-northeast1-docker.pkg.dev/emerald-cab-354713/opinion-galaxy-export-job/opinion-galaxy-export-image