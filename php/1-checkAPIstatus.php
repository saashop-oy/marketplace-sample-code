<?php

$_API_STAGE = getenv('API_STAGE');
$_API_VERSION = getenv('API_VERSION');
$_INTERNAL_ERROR_CODE = 500;


/* This ping endpoint can be used to check the status of the API without any authentication headers.*/
function checkAPIStatus($stage, $version){
    try{
        $endpoint = "https://{$stage}/base/{$version}/ping";
        $curl = curl_init();        
        curl_setopt($curl, CURLOPT_URL, $endpoint);
        curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "GET");
        $response = curl_exec($curl);
        curl_close($curl);
        return $response;
    }
    catch (Exception $e) {
        print($e);
        return $_INTERNAL_ERROR_CODE;
    }
}

$ping = checkAPIStatus($_API_STAGE, $_API_VERSION);
if ($ping != $_INTERNAL_ERROR_CODE) {
    echo 'ERROR: API call failed.';
    exit();
}
echo $ping;
?> 