## Enrich PurePath with OpenTelemetry instrumentation
This repository has the sample app used within [this blog post](https://www.dynatrace.com/news/blog/unlock-end-to-end-observability-insights-with-dynatrace-purepath-4-seamless-integration-of-opentracing-for-java/) to show how to unlock end-to-end observability insights with Dynatrace PurePath 4 seamless integration of OpenTracing for Java.  
***

### Disclaimer
The contained code is considered educational and NOT SUPPORTED by Dynatrace. Please use at your own risk. You can contact the author via Github issues.
***

### Note
This sample app uses Spring Boot Framework.  
The `hazelcastInstance` is `@AutoWired`, but we've added the method `getTracingHazelcast` in order to replace the default `hazelcastInstance` to a `TracingHazelcastInstance`.  
This was done in the [CommandController](src/main/java/com/dynatrace/hazelcast/CommandController.java).  
  
The class `MyTracer` shows how the Tracer is set.  
If the OneAgent is deployed in the host, the `GlobalTracer` will be registered automatically, otherwise the method `initTracer()` registers a `JaegerTracer`.
