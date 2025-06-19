# Reproduce Unified Service Detection behavior using Service Detection v2 rules


For all rules, `If condition matches` option set to `Detect request on endpoint`

| Rule # | Rule Name                                      | Condition                                                                                                                                                                                                 | Endpoint Name Template             |
|--------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| 1      | istio gateway                                  | matchesValue(service.name, "istio-*")                                                                                                                                                                   | /                                  |
| 2      | rpc.method, rpc.service                        | span.kind == "server" and isNotNull(rpc.method) and isNotNull(rpc.service)                                                                                                                              | {rpc.service}.{rpc.method}         |
| 3      | rpc.method                                     | span.kind == "server" and isNotNull(rpc.method)                                                                                                                                                         | {rpc.method}                       |
| 4      | adobe.em, http.request.method Health Check     | isNotNull(adobe.em.env_type) and matchesValue(http.request.method, "HEAD*")                                                                                                                             | Health Check                       |
| 5      | adobe.em, url.path Health Check                | isNotNull(adobe.em.env_type) and matchesValue(url.path, "/system/probes/health*")                                                                                                                       | Health Check                       |
| 6      | adobe.em url.truncated_path                    | span.kind == "server" and isNotNull(adobe.em.env_type) and isNotNull(url.truncated_path)                                                                                                                | {url.truncated_path}              |
| 7      | http.route                                     | span.kind == "server" and isNotNull(http.route)                                                                                                                                                         | {http.route}                       |
| 8      | webservers                                     | span.kind == "server" and isNotNull(http.method) and (matchesValue(telemetry.sdk.language, "Cpp*") or matchesValue(telemetry.sdk.language, "Apache*") or matchesValue(telemetry.sdk.language, "Nginx*")) | /                                  |
| 9      | faas incoming                                  | isNotNull(faas.name)                                                                                                                                                                                    | invoke                             |
| 10     | code.function, code.namespace                  | isNotNull(code.function) and isNotNull(code.namespace)                                                                                                                                                  | {code.namespace}.{code.function}   |
| 11     | code.function                                  | isNotNull(code.function)                                                                                                                                                                                | {code.function}                    |
| 12     | code.namespace                                 | isNotNull(code.namespace)                                                                                                                                                                               | {code.namespace}                   |
| 13     | span.name fallback                             | isNotNull(span.name)                                                                                                                                                                                    | {span.name}                        |


## Steps to apply the Setting automatically
1. Generate an access token by following the steps described [here](https://docs.dynatrace.com/docs/shortlink/token#create-api-token). The token needs "Write settings" (settings.write) and "Read settings" (settings.read) permissions.
1. Replace the URL with your environment ID and the generated access token.
1. Run the script in your terminal:

```shell
curl --location --request POST 'https://REPLACE.dynatrace.com/api/v2/settings/objects' \
--header 'Authorization: Api-Token dt0c01.REPLACE.REPLACE' \
--header 'Content-Type: application/json' \
--data-raw '[{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "istio gateway",
				"description": null,
				"condition": "matchesValue(service.name, \"istio-*\")",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "/"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "rpc.method, rpc.service",
				"description": null,
				"condition": "span.kind == \"server\" and isNotNull(rpc.method) and isNotNull(rpc.service) ",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{rpc.service}.{rpc.method}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "rpc.method",
				"description": null,
				"condition": "span.kind == \"server\" and isNotNull(rpc.method)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{rpc.method}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "adobe.em, http.request.method Health Check",
				"description": null,
				"condition": "isNotNull(adobe.em.env_type) and matchesValue(http.request.method, \"HEAD*\")",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "Health Check"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "adobe.em, url.path Health Check",
				"description": null,
				"condition": "isNotNull(adobe.em.env_type) and matchesValue(url.path, \"/system/probes/health*\")",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "Health Check"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "adobe.em url.truncated_path",
				"description": null,
				"condition": "span.kind == \"server\" and isNotNull(adobe.em.env_type) and isNotNull(url.truncated_path)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{url.truncated_path}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "http.route",
				"description": null,
				"condition": "span.kind == \"server\" and isNotNull(http.route)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{http.route}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "webservers",
				"description": null,
				"condition": "span.kind == \"server\" and isNotNull(http.method) and (matchesValue(telemetry.sdk.language, \"Cpp*\") or matchesValue(telemetry.sdk.language, \"Apache*\") or matchesValue(telemetry.sdk.language, \"Nginx*\"))",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "/"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "faas incoming",
				"description": null,
				"condition": "isNotNull(faas.name)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "invoke"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "code.function, code.namespace",
				"description": null,
				"condition": "isNotNull(code.function) and isNotNull(code.namespace)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{code.namespace}.{code.function}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "code.function",
				"description": null,
				"condition": "isNotNull(code.function)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{code.function}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "code.namespace",
				"description": null,
				"condition": "isNotNull(code.namespace)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{code.namespace}"
			}
		}
	},
	{
		"schemaId": "builtin:endpoint-detection-rules",
		"schemaVersion": "0.0.4",
		"scope": "environment",
		"value": {
			"enabled": true,
			"rule": {
				"ruleName": "span.name fallback",
				"description": null,
				"condition": "isNotNull(span.name)",
				"ifConditionMatches": "DETECT_REQUEST_ON_ENDPOINT",
				"endpointNameTemplate": "{span.name}"
			}
		}
	}
]'
```