from db_procedures import db_execute
from sys_config import sys_idiom
from sys_log import log
from sys_error_messages import ErrorMessageConfig
from sys_information_messages import InformationMessageConfig

import hashlib
import time
from dataclasses import dataclass, asdict
import json

from functools import wraps
from typing import Any, Callable, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()


# Mock database of API keys and their respective limits
@dataclass
class RateLimit:
    max_calls: int
    period: int

api_key_limits = {
    "api_key_1": RateLimit(max_calls=5, period=60),
    "api_key_2": RateLimit(max_calls=10, period=60),
}

# Configuration Message based on the idiom
config_error = ErrorMessageConfig(idiom=sys_idiom)
config_information = InformationMessageConfig(idiom=sys_idiom)


def rate_limit():
    def decorator(func: Callable[[Request], Any]) -> Callable[[Request], Any]:
        usage: dict[str, list[float]] = {}

        @wraps(func)
        async def wrapper(request: Request) -> Any:
            # get the API key
            api_key = request.headers.get("X-API-KEY")
            if not api_key:
                raise HTTPException(status_code=400, detail=config_error.get_message("HTTPException-400"))

            # check if the API key is valid
            if api_key not in api_key_limits:
                raise HTTPException(status_code=403, detail=config_error.get_message("HTTPException-403"))

            # get the rate limits for the API key
            limits = api_key_limits[api_key]

            # get the client's IP address
            if not request.client:
                raise ValueError(config_error.get_message("ERR-003"))
            ip_address: str = request.client.host

            # create a unique identifier for the client
            unique_id: str = hashlib.sha256((api_key + ip_address).encode()).hexdigest()

            # update the timestamps
            now = time.time()
            if unique_id not in usage:
                usage[unique_id] = []
            timestamps = usage[unique_id]
            timestamps[:] = [t for t in timestamps if now - t < limits.period]

            if len(timestamps) < limits.max_calls:
                timestamps.append(now)
                return await func(request)

            # calculate the time to wait before the next request
            wait = limits.period - (now - timestamps[0])
            raise HTTPException(
                status_code=429,
                detail=f"{config_error.get_message("HTTPException-429")}"
                       + f" {config_information.get_message("wait")} "
                       + f"{wait:.2f} s."
            )

        return wrapper

    return decorator


'''
#####################
### PROFILE CLASS ###
#####################
'''
cfg_api_key = 'api_key_1'


class Profiles:
    def __init__(self):
        # Initialize any attributes if needed
        pass

    @staticmethod
    def profile_login(api_key: str, user_name: str, user_password: str):
        """
        Login to the user account
        result = db_execute("exec [dbo].[zPython_v01_sp_Login_Get_json]
        @UserName = 'joanxtb@gmail.com', @Password = 'master*10*'")

        """

        if api_key == cfg_api_key:
            try:

                database_owner = 'dbo'
                procedure_name = 'zPyv01_sp_Login_Get_json'

                # Replace 'get_user_profile' with your actual function call
                cmd_execute = (f"exec [{database_owner}].[{procedure_name}] "
                               f"@UserName = '{user_name}'"
                               f", @Password = '{user_password}'")

                # Execute the stored procedure and get JSON result
                sql_response_json_data = db_execute(cmd_execute)

                if sql_response_json_data:
                    # Fetch all rows from the cursor
                    return sql_response_json_data

                # Return an empty DataFrame if no response
                return '{}'

            except Exception as e:
                log(str(e))
        else:
            log(config_error.get_message("HTTPException-403"))


# Request model for the login
class LoginRequest(BaseModel):
    api_key: str
    email: str
    password: str


@app.get("/")
@rate_limit()
async def root(request: Request):
    return {f"{config_information.get_message("message")}": f"{config_information.get_message("INF-001")}"}


@app.post("/login")
async def login_user(login_request: LoginRequest):
    profiles = Profiles()

    if login_request.api_key == cfg_api_key:
        user = profiles.profile_login(login_request.api_key, login_request.email, login_request.password)
        if user:
            return JSONResponse(content=json.loads(user))
        else:
            raise HTTPException(status_code=401, detail=config_error.get_message("ERR-002"))
    else:
        raise HTTPException(status_code=401, detail=config_error.get_message("ERR-001"))


'''
EXECUTE IN THE TERMINAL 
uvicorn sp_profiles:app --reload --port 9000

TO TEST THE API:
 curl -X POST "http://127.0.0.1:9000/login" -H "Content-Type: application/json"
 -d '{"email": "joanxtb@gmail.com", "password": "master*10*"}'

# Internal Server Error 
curl -X POST "http://127.0.0.1:9000/login" -H "Content-Type: application/json" -d '{"email": "joanxtb@gmail.com", "password": "master*10*"}'

curl -X GET "http://127.0.0.1:9000" -H "X-API-KEY":api_key_1

curl -X POST "http://127.0.0.1:9000/login" -H "Content-Type: application/json" -d '{"email": "joanxtb@gmail.com", "password": "master*10*", "api_key": "api_key_1"}'


JSON Documentation:
https://learn.microsoft.com/en-us/sql/relational-databases/json/json-data-sql-server?view=sql-server-ver16

'''
