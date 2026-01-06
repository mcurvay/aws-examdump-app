#!/bin/bash
# Docker build and push script for AWS SAA-C03 Exam App

set -e

IMAGE_NAME="mcurvay/aws-examdump-app"
VERSION=${1:-latest}

echo "🐳 Building Docker image: ${IMAGE_NAME}:${VERSION}"
docker build -t ${IMAGE_NAME}:${VERSION} .

echo "✅ Build successful!"
echo ""
echo "📦 Image details:"
docker images ${IMAGE_NAME}:${VERSION}

echo ""
read -p "Do you want to push to Docker Hub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🔐 Please login to Docker Hub..."
    docker login
    
    echo "📤 Pushing ${IMAGE_NAME}:${VERSION} to Docker Hub..."
    docker push ${IMAGE_NAME}:${VERSION}
    
    if [ "$VERSION" != "latest" ]; then
        echo "📤 Also pushing as latest..."
        docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest
        docker push ${IMAGE_NAME}:latest
    fi
    
    echo "✅ Push successful!"
    echo ""
    echo "🎉 Image is now available on Docker Hub:"
    echo "   docker pull ${IMAGE_NAME}:${VERSION}"
else
    echo "⏭️  Skipping push. You can push later with:"
    echo "   docker push ${IMAGE_NAME}:${VERSION}"
fi

