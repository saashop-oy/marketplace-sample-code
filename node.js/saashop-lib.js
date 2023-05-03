
const uuid = require('uuid');
const axios = require('axios').default;


/*
    Source env.rc to export some sensitive data to Environment Variables.
    Get these Variable here.
*/
const API_STAGE = process.env.API_STAGE;
const API_VERSION = process.env.API_VERSION;
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const baseURL = `https://${API_STAGE}`;


/* 
    Check the status of the API without any authentication headers. 
*/
const ping = async () => {
    const url = `${baseURL}/base/${API_VERSION}/ping`;
    console.log(`Invoke API: GET ${url}`);
    return axios.get(url);
}

/*
    pass ClientId and ClientSecret to this method and get time-limited JWT Bearer token.
    - clientID
    - clientSecret
    Token will be expired in 30 minutes.
*/
const getToken = async (clientID=CLIENT_ID, clientSecret=CLIENT_SECRET) => {
    const url = `${baseURL}/auth/${API_VERSION}/tokens`;
    const b64 = Buffer.from(`${clientID}:${clientSecret}`, 'utf8').toString('base64');
    const config = {
        headers: {
            'X-Request-ID': uuid.v4(),
            'Authorization': 'Basic ' + b64
        }
    };
    console.log(`Invoke API: POST ${url}`);
    const response = await axios.post(url, null, config);
    const token = `${response.data.tokenType} ${response.data.accessToken}`
    return token;
}

/*
    Get chunk of marketplaceEvents.
    - token
    - limit: indicate the amount of data retrieves. recommended value is 50
    return value is an array of new added marketplaceEvents with maximum size of "limit".
*/
const getMarketplaceEventsChunk = (token, limit=50) => {
    const url = `${baseURL}/lead/${API_VERSION}/marketplaceEvents`;
    const config = {
        params: {
            "limit": limit
        },
        headers: {
            "X-Request-ID": uuid.v4(),
            "Authorization": token
        }
    };
    console.log(`Invoke API: GET ${url}?limit=${limit}`);
    return axios.get(url, config);
}

/*
    Get all marketplaceEvents.
    This is a recursive function and call itself untill get all marketplaceEvents chunk by chunk.
    - token
    - limit: indicate the amount of data retrieves. recommended value is 50    
    - marketplaceEvents: An array that we fill it in each recursive function call.    
    return value is an array of all new added marketplaceEvents.
*/
const getMarketplaceEvents = async (token, limit=50, marketplaceEvents=[]) => {
    const { data } = await getMarketplaceEventsChunk(token, limit);

    marketplaceEvents = data.marketplaceEvents.concat(marketplaceEvents);
    if (data.hasMore) {
        return getMarketplaceEvents(token, limit, marketplaceEvents);
    }
    return marketplaceEvents
}

/*
    Get order by it's Id.
    - token
    - orderId
    return value is an Order object.
*/
var getOrder = function (token, orderId) {
    const url = `${baseURL}/lead/${API_VERSION}/orders/${orderId}`;
    const config = {
        headers: {
            "X-Request-ID": uuid.v4(),
            "Authorization": token
        }
    };
    console.log(`Invoke API: GET ${url}`);
    return axios.get(url, config)
}

/*
    Get License by it's Id.
    - token
    - licenseId
    return value is an License object.
*/
var getLicense = function (token, licenseId) {
    const url = `${baseURL}/lead/${API_VERSION}/licenses/${licenseId}`;  
    const config = {
        headers: {
            "X-Request-ID": uuid.v4(),
            "Authorization": token
        }
    };
    console.log(`Invoke API: GET ${url}`);
    return axios.get(url, config);
}

/*
    pass body to this method and post marketplaceEvent.
    - Id of order you want to add marketplaceEvent.
    - eventTypeCode, required, string
        - Enum: "ServicePurchased" "Evaluation" "Trial" "UpgradeToTrial" "UpgradeToPurchase" 
        - Currently supported types: ServicePurchased
    - statusCode, required, string
        - Enum: "ProvisioningStarted" "ProvisioningInProgress" "ProvisioningCompleted" "ProvisioningFailed"
    body = marketplaceEvent = {
        "additionalProperties": [
            {
                "description": "Unique identifier of the order. This identifer can be used to fetch the order.",
                "name": "orderId",
                "value": orderId
            }
        ],
        "description": Description,
        "eventTypeCode": eventTypeCode,
        "statusCode": statusCode
    }    
*/
const postMarketplaceEvents = (token, body) => {
    const url = `${baseURL}/lead/${API_VERSION}/marketplaceEvents`;
    const config = {
        headers: {
            "Content-Type": "application/json",
            "X-Request-ID": uuid.v4(),
            "Authorization": token
        }
    };
    console.log(`Invoke API: POST ${url}`);
    return axios.post(url, body, config);
}


module.exports = { ping, getToken, getMarketplaceEvents, postMarketplaceEvents, getOrder, getLicense };