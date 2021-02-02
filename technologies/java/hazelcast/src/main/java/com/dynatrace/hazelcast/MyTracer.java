package com.dynatrace.hazelcast;

import io.jaegertracing.internal.JaegerTracer;
import io.jaegertracing.internal.samplers.ConstSampler;
import io.opentracing.Tracer;
import io.opentracing.util.GlobalTracer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MyTracer {

	@Bean
	public Tracer initTracer() {
		GlobalTracer.registerIfAbsent(createJaegerTracer("Hazelcast-Tracer"));
		return GlobalTracer.get();
	}

	private JaegerTracer createJaegerTracer(String service) {
		io.jaegertracing.Configuration.SamplerConfiguration samplerConfig = io.jaegertracing.Configuration.SamplerConfiguration.fromEnv()
				.withType(ConstSampler.TYPE)
				.withParam(1);

		io.jaegertracing.Configuration.ReporterConfiguration reporterConfig = io.jaegertracing.Configuration.ReporterConfiguration.fromEnv()
				.withLogSpans(true);

		io.jaegertracing.Configuration config = new io.jaegertracing.Configuration(service)
				.withSampler(samplerConfig)
				.withReporter(reporterConfig);

		return config.getTracer();
	}
}
