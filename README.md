# WebGL-Unity-AWS-CD#
## Uses 3 AWS services (free tier works) to continuosly deploy off of Unity's CI integration with github. Sorry it's so complicated :D ##
### Lambda (running this script) ###
Simply edit the script.py file with your AWS S3 key, Secret key, bucket name, and unity API key. The zip up this entire repo, and upload to AWS Lambda. Make sure you select python 2.7 (3 not supported yet), and make sure the handler is script.lambda_handler
### API Gateway ###
Definately the hardest to configure. Create a Post at the root level, and configure that post's intergration Request (Should use the lambda we created). For the body mapping template, create a new one for "application/json", and paste this as the template body: 
```
##  See http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
##  This template will pass through all parameters including path, querystring, header, stage variables, and context through to the integration endpoint via the body/payload
#set($allParams = $input.params())
{
"body-json" : $input.json('$'),
"params" : {
#foreach($type in $allParams.keySet())
    #set($params = $allParams.get($type))
"$type" : {
    #foreach($paramName in $params.keySet())
    "$paramName" : "$util.escapeJavaScript($params.get($paramName))"
        #if($foreach.hasNext),#end
    #end
}
    #if($foreach.hasNext),#end
#end
},
"stage-variables" : {
#foreach($key in $stageVariables.keySet())
"$key" : "$util.escapeJavaScript($stageVariables.get($key))"
    #if($foreach.hasNext),#end
#end
},
"context" : {
    "account-id" : "$context.identity.accountId",
    "api-id" : "$context.apiId",
    "api-key" : "$context.identity.apiKey",
    "authorizer-principal-id" : "$context.authorizer.principalId",
    "caller" : "$context.identity.caller",
    "cognito-authentication-provider" : "$context.identity.cognitoAuthenticationProvider",
    "cognito-authentication-type" : "$context.identity.cognitoAuthenticationType",
    "cognito-identity-id" : "$context.identity.cognitoIdentityId",
    "cognito-identity-pool-id" : "$context.identity.cognitoIdentityPoolId",
    "http-method" : "$context.httpMethod",
    "stage" : "$context.stage",
    "source-ip" : "$context.identity.sourceIp",
    "user" : "$context.identity.user",
    "user-agent" : "$context.identity.userAgent",
    "user-arn" : "$context.identity.userArn",
    "request-id" : "$context.requestId",
    "resource-id" : "$context.resourceId",
    "resource-path" : "$context.resourcePath"
    }
}
```
After that, you're all set here
### S3 (hosting the files) ### 
Just need to set up a bucket, and make that bucket public. You can upload the files, then make the files all public, or you can change the permissions to the files to have Read access by everyone
### Unity Cloud Build ### 
Configure a web hook on Unity Cloud build on successful build to the API root that you created on AWS API Gateway (to the post reciever configured on API Gateway, and with application/json as the payload)
