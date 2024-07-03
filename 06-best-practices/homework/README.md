
pipenv install
pipenv shell


docker-compose up -d
docker compose logs localstack
docker compose down


aws configure

aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration



