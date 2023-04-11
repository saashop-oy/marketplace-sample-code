const uuid = require('uuid');
const axios = require('axios').default;


/*
    Source env.rc to export some sensitive data to Environment Variables.
    Get these Variable here.
*/
const _API_STAGE = process.env.API_STAGE;
const _API_VERSION = process.env.API_VERSION;
const _CLIENT_ID = process.env.CLIENT_ID;
const _CLIENT_SECRET = process.env.CLIENT_SECRET;

/*
    Check the status of the API without any authentication headers.
*/
var checkAPIstatus = function () {
    return new Promise((resolve, reject) => {    
        const url = `https://${_API_STAGE}/base/${_API_VERSION}/ping`;        
        axios
            .get(url)
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
}

/*
    Get chunk of marketplaceEvents.
    - limit: indicate the amount of data retrieves. recommended value is 50
    return value is an array of new added marketplaceEvents with maximum size of "limit".
*/
var getMarketplaceEvents = function (token, url, limit) {
    console.log(`Invoke API: ${url}?limit=${limit}`);
    return new Promise((resolve, reject) => {
        config = {
            params: {
                "limit": limit
            },
            headers: {
                "X-Request-ID": uuid.v4(),
                "Authorization": token
            }
        };
        axios
            .get(url, config)
            .then(response => {
                resolve(response);
            })
            .catch(error => {
                reject(error);
            });
    });
}


/*
    Get all of marketplaceEvents.
    This is a recursive function and call itself untill get all marketplaceEvents chunk by chunk.
    - limit: indicate the amount of data retrieves. recommended value is 50    
    - marketplaceEvents: An array that we fill it in each recursive function call.    
    return value is an array of all new added marketplaceEvents.
*/
var getMarketplaceEventsRecursive = function (token, url, limit, marketplaceEvents) {
    return new Promise((resolve, reject) => {
        getMarketplaceEvents(token, url, limit)
            .then(response => {
                response.data.marketplaceEvents.forEach(element => {
                    marketplaceEvents.push(element);
                });
                if(response.data.hasMore) {
                    resolve(getMarketplaceEventsRecursive(token, url, limit, marketplaceEvents));
                }else{
                    resolve(marketplaceEvents);
                }
            })
            .catch(error => {
                reject(error);
            });
    });
}


/*
    Get order by it's Id.    
    - orderId
    return value is an Order object.
*/
var getOrder = function (token, orderId) {
    const url = `https://${_API_STAGE}/lead/${_API_VERSION}/orders/${orderId}`;
    console.log(`Invoke API: ${url}`);
    return new Promise((resolve, reject) => {
        config = {
            headers: {
                "X-Request-ID": uuid.v4(),
                "Authorization": token
            }
        };
        axios
            .get(url, config)
            .then(response => {
                resolve(response);
            })
            .catch(error => {
                reject(error);
            });
    });
}


/*
    Get License by it's Id.    
    - licenseId
    return value is an License object.
*/
var getLicense = function (token, licenseId) {
    const url = `https://${_API_STAGE}/lead/${_API_VERSION}/licenses/${licenseId}`;
    console.log(`Invoke API: ${url}`);
    return new Promise((resolve, reject) => {
        config = {
            headers: {
                "X-Request-ID": uuid.v4(),
                "Authorization": token
            }
        };
        axios
            .get(url, config)
            .then(response => {
                resolve(response);
            })
            .catch(error => {
                reject(error);
            });
    });
}

/*
    Dispatch request to get Order or License based on additionalProperties in marketplaceEvent.
    You have to add your custom code to provision service or license here.
    - marketplaceEvent
    return value is an License object or an Order object.
*/
var dispatch = function (marketplaceEvent) {
    return new Promise((resolve, reject) => {
        additionalProperties = marketplaceEvent["additionalProperties"]
        additionalProperties.forEach(additionalProperty => {
            if (additionalProperty["name"] == "orderId") {
                getOrder(token, additionalProperty["value"])
                    .then(response => {
                        // This is Order
                        // Add Your provisioning code here
                        resolve('Success!')
                    })
                    .catch(error => {
                        reject(error)
                    });
            } else if (additionalProperty["name"] == "licenseId"){
                getLicense(token, additionalProperty["value"])
                    .then(response => {
                        // This is License
                        // Add Your license management code here
                        resolve('Success!')
                    })
                    .catch(error => {
                        reject(error)
                    });
            }    
        });
    });
}

/*
    pass ClientId and ClientSecret to this method and get time-limited JWT Bearer token.
    Token will be expired in 30 minutes.
*/
var authenticate = function () {
    return new Promise((resolve, reject) => {
        const url = `https://${_API_STAGE}/auth/${_API_VERSION}/tokens`;
        config = {
            headers: {
                'X-Request-ID': uuid.v4(),
                'Authorization': 'Basic ' + Buffer.from(`${_CLIENT_ID}:${_CLIENT_SECRET}`, 'utf8').toString('base64')
            }
        };
        axios
            .post(url, null, config)
            .then(response => {
                token = `${response.data.tokenType} ${response.data.accessToken}`;
                resolve(token);
            })
            .catch(error => {
                reject(error);
            });
    });
}


/*
    Call checkAPIstatus to see the simple ping response form API server.
*/
/*checkAPIstatus()
    .then((ping) => {
        console.log(ping);
    })
    .catch(error => {
        console.log(error);
    });
*/



/*
    1. First call authenticate function to have a JWT tokne.
    2. Get new marketplaceEvents by call getMarketplaceEventsRecursive
    3. For each marketplaceEvent, call Dispatch function.
*/
authenticate(_API_STAGE, _API_VERSION, _CLIENT_ID, _CLIENT_SECRET)
    .then((token) => {
        getMarketplaceEventsRecursive(token, `https://${_API_STAGE}/lead/${_API_VERSION}/marketplaceEvents`, 40, marketplaceEvents=[])
            .then((marketplaceEvents) => {
                marketplaceEvents.forEach(marketplaceEvent => {
                    dispatch(marketplaceEvent)
                        .then(response => {
                            console.log(response);
                        })
                        .catch(error => {
                            reject(error);
                        });
                });
            })
            .catch((error) => {
                console.log(error);
            });
    })
    .catch(error => {
        console.log(error);
    });
