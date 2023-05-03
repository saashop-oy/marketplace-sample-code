
const saashop = require("./saashop-lib.js")

const main = async () => {
    
    /* Check Id API is Up and Get ping object */
    const ping = await saashop.ping();
    //console.log(ping.data);

    /* Get JWT Bearer token. */
    const token = await saashop.getToken();
    //console.log(token);

    /* Get marketplaceEvents and proceed to get Order or license. */     
    const marketplaceEvents = await saashop.getMarketplaceEvents(token);
    //console.log(marketplaceEvents);
    
    const additionalProperties = marketplaceEvents.map((marketplaceEvents) => marketplaceEvents.additionalProperties).flat();
    //console.log(additionalProperties);
    for (const additionalProperty of additionalProperties) {
        if (additionalProperty.name === 'licenseId') {
            const license = await saashop.getLicense(token, additionalProperty.value);
            console.log(license.data);
            //Add Custom Code Here
            //
            //
            //
            //

        } else if (additionalProperty.name === 'orderId') {
            const order = await saashop.getOrder(token, additionalProperty.value);
            console.log(order.data);
            //Add Custom Code Here
            //
            //
            //
            //
        }
    }

    /* Get order with Id */
    const order = await saashop.getOrder(token, "60abcede-1312-4caa-a435-d3e17e74e66d");
    //console.log(order.data);

    /* Get license with Id */
    const license = await saashop.getLicense(token, "f767fcda-d3e6-4229-9548-06f01de250ea");
    //console.log(license.data);

    /* Post marketplaceEvent */
    const orderId = '22e13cc4-7e2c-4899-8723-359444a9eb48'; // the Order we want to add marketplaceEvent
    const marketplaceEvent = {
        "additionalProperties": [
            {
                "description": "Unique identifier of the order. This identifer can be used to fetch the order.",
                "name": "orderId",
                "value": orderId
            }
        ],
        "description": 'Provisioning has been started',
        "eventTypeCode": 'ServicePurchased',
        "statusCode": 'ProvisioningInProgress'
    }
    const res = await saashop.postMarketplaceEvents(token, marketplaceEvent);
    //console.log(res.status);
}

main();