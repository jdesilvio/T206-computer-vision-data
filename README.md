# A Data-only container for T206 Computer Vision

### Setup
    docker build --rm --build-arg ACCESS_KEY='access key' --build-arg SECRET_KEY='secret key' -t t206cv-data .
    docker run -d -t -v /app/dbdata --name data t206cv-data
