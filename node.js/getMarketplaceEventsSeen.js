const uuid = require('uuid');
const axios = require('axios').default;

const _API_STAGE = process.env.API_STAGE;
const _API_VERSION = process.env.API_VERSION;
const _CLIENT_ID = process.env.CLIENT_ID;
const _CLIENT_SECRET = process.env.CLIENT_SECRET;


var getMarketplaceEventsSeen = function (token, url, offset, limit) {
    console.log(`Invoke API: ${url}?offset=${offset}&limit=${limit}`);
    return new Promise((resolve, reject) => {    
        config = {
            params: {
                "offset": offset,
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

var getMarketplaceEventsSeenRecursive = function (token, url, offset, limit, marketplaceEvents) {
    return new Promise((resolve, reject) => {
        getMarketplaceEventsSeen(token, url, offset, limit)
            .then(response => {
                response.data.marketplaceEvents.forEach(element => {
                    marketplaceEvents.push(element);
                });
                if(response.data.hasMore) {
                    resolve(getMarketplaceEventsSeenRecursive(token, url, offset+limit, limit, marketplaceEvents));
                }else{
                    resolve(marketplaceEvents);
                }
            })
            .catch(error => {
                reject(error);
            });
    });
}

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

authenticate()
    .then((response) => {
        getMarketplaceEventsSeenRecursive(response, `https://${_API_STAGE}/lead/${_API_VERSION}/marketplaceEvents/seen`, 0, 40, marketplaceEvents=[])
            .then((marketplaceEvents) => {
                console.log(marketplaceEvents);
            })
            .catch((error) => {
                console.log(error);
            });
    })
    .catch(error => {
        console.log(error);
    });