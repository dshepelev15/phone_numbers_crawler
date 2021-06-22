## Steps for running

### Python usage  
1. Prepare venv
```
virtualenv -p python3 .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
```
2. Run tests
```
pytest
```
3. Run crawler locally
```
python crawler.py --urls https://hands.ru https://repetitors.info 
``` 
4. Get results in `result.json` file in your local directory


### [Docker](https://www.docker.com/) usage
1. Download and install docker
2. Build image:
```
docker build -t crawler .
```
* Run container and pass urls for crawling  
```
docker run --rm -it -v ${PWD}:/code crawler --urls https://hands.ru https://repetitors.info
```
4. Get results in `result.json` file in your local directory
