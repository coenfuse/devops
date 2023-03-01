A plugin first component driven metrics collector and data aggregator. It will
have facility to create or customize, existing plugins, that divided into three
primary categories: Input Plugin, Process Plugin and Output Plugin

In input plugin we specify the input channel to be used, whether it is CAN, MQTT,
Modbus, Docker, HTTP and then we specify the content type via configuration.
Currently it only supports YAML, JSON, CSV and XML content types. More content
types will be added in the future.

Every content blob passing through the channel will then be converted into a
single depth map. With this hashmap we do the processing as default or by the
customization logic. The processed data is then written to the output endpoint
using the output plugin.

Both the input and output plugins must be an extension of mflux's generic input
classes and input channels must use existing connection drivers. For
example, an HTTP based input plugin must use Mflux's HTTP Driver, similarly,
MQTT based plugin must use Mflux's Mosquitto Driver.

Mflux should also have inbuilt file buffering mechanism to write processed output
to a dump file in case of outbound connection loss. Outbound writes will be dumped
into a file until outflow connection reconnects. When it does reconnect, all the
dumps from the file will be written off first (likely to be in a single pass) then
subsequent writes will be done.

MFlux should also have a TOML based configuration and configuration generator
module that helps users in generating pipeline specific configuration.