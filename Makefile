builde:
	docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/emerald-cab-354713/opinion-galaxy-export-job/opinion-galaxy-export-image -f export/Dockerfile.export .

pushe:
	docker push asia-northeast1-docker.pkg.dev/emerald-cab-354713/opinion-galaxy-export-job/opinion-galaxy-export-image