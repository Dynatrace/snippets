// Copyright 2019 Dynatrace LLC

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

{{- define "imagePullSecret" }}
{{- with .Values.dynatrace }}
{{- printf "{\"auths\":{\"%s\":{\"username\":\"%s\",\"password\":\"%s\",\"auth\":\"%s\"}}}" .host .environment .paasToken (printf "%s:%s" .environment .paasToken | b64enc) | b64enc }}
{{- end }}
{{- end }}



{{- define "image" }}
{{- with .Values.dynatrace }}
{{- printf "%s/linux/activegate" .host }}
{{- end }}
{{- end }}