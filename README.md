# Introduction

This project is about background job multiprocessing.
## Idea
### Ideal case without this implementation
The client sends a request for performing heavy jobs something as generating pdf, or any other time and resource taking jobs. the server will receive this request and start performing the task and the `client has to wait for a response` then after client can do other things like moving around.

### With implementation
The client sends a request for performing a heavy job, and the server will receive this request and process it in the background, meanwhile server will send a response back saying that your job is received with a status URL for getting the status of the background task. In this case, the `client need not wait till the heavy job completes` its task. Also, the server can take requests meanwhile the `heavy job is being done in the background` `instead of blocking the server` from taking requests.

# Install

Run following command
```bash
python3 my_api.py
```

send `post` request to `http://127.0.0.1:6060/task/<any number>` with following body

```json
{
    "job_id":12312312,
    "operator": 34
}
```

send `GET` request to `http://127.0.0.1:6060/` for getting status of background task