# HTTP Input Plugin
- Version - 1.0
- Release Date - 20 April 2023
- Author - [github.com/coenfuse](www.github.com/coenfuse)

This HTTP Input plugin is a component for the Lamina data collection application that allows you to collect data that is available on a local or remote HTTP server. With the help of this plugin you can set up a periodic poller, targeted at a particular URL endpoint, that'll be continously requesting the server for responses. Just like other input plugins, you can also assign a custom string tag. This taggnig will be particularly useful in routing data between different component of the data pipeline.

## How to use?

To use the HTTP input plugin in Lamina, follow these steps:
1. Open the root lamina.toml configuration file for your Lamina instance.
2. In the inputs section, add a new input plugin wit a unique name using the following naming convention ```inputs.http.<name>```. For example, ```inputs.http.lallu```
3. Fill the input plugin with required plugin parameters as mentioned in this sample
[config.toml](docs/config.toml)
4. Go the 'stream' config block at the end of lamina.toml and make sure to add the name of this newly created input plugin. For example,
```
    [stream]
        input = [http.lallu, ...]
        output = [...]
```
4. Save the lamina.toml configuration file and restart your Lamina instance.
5. The HTTP input plugin should now be able to connect to HTTP Server and start receiving messages based on the configured endpoints. Responses will be then forwarded to any outputs that are configured to receive messages from the plugins.

## Configuration

The following is the full configuration of this plugin in TOML format with complete documentation of each config parameter
```
[inputs.http.<name>]
    
    # the URL of the local or remote HTTP server
    # Lamina will try to raise an error if invalid URL is specified
    host.url = "https://httpbin.org/uuid"

    # [OPTIONAL] request parameters where you can customize your HTTP requests
    # If this block is empty, a basic GET request with empty payload is made
    
    # Specify the method of HTTP request, valid methods are
    # GET, PATCH, POST and PUT
    req.method = "GET"

    # Request headers
    # This is specified as a TOML key-map so make sure to write all your key-map
    # pairs in a single line, within curly braces, separated by comma and grouped
    # by '=' sign. For example,
    # req.headers = { "key" = "value", "key" = "value", ...}
    req.headers = { "accept" = "application/json"}

    # Provide request parameters as a dictionary of strings, As an example, if 
    # you wanted to pass key1=value1 and key2=value2 to httpbin.org/get, you'd
    # write, 
    # req.params = {'key1'='value1', 'key2'='value2'}
    # and this will be properly encoded into a URL as,
    # https://httpbin.org/get?key2=value2&key1=value1
    # 
    # You can also pass a list of items as a value:
    # req.params = {'key1' = 'value1', 'key2' = ['value2', 'value3']}
    # and this will be encoded into a URL as,
    # https://httpbin.org/get?key1=value1&key2=value2&key2=value3
    req.params = {}

    # Mention the request data that you may want to submit to the server. For
    # e.g., HTML FORM data. The data mentioned here should be a serialized string
    # and appropriate header for that must be provided in req.headers (if required
    # by the server)
    req.data = ""

    # If you wish this HTTP client to send a data file instead, the specify a
    # valid path of the file in the system. During initial configuration the
    # client will read the file in binary and keep it in memory. The read data
    # will be then used for every poll made by this client.
    req.file = ".vscode/launch.json"

    # Timeout for server response before the client raises warning
    req.timeout_s = 4

    # An array of acceptable HTML status codes, must have atleast one.
    res.success = [200]

    # If the server keeps responding with same content, do you want to ignore it
    # or keep it?
    res.content.allow_duplicates = false

    # Decoding of HTML response content
    # 1. 'auto' - the client will try to automatically decode the content using the response headers
    # 2. 'raw'  - the client will not touch the response content and just relay it in raw binary format
    # 3. <custom> - specify a custom decoder to decode the HTML response content from
    # one of the many available python3.11 decoders. An exhaustive list is 
    # mentioned here
    # https://docs.python.org/3.11/library/codecs.html#standard-encodings
    res.content.decoding = "utf-8"
    
    # specify the string tag you want to assign to the response received from the
    # server by this client. This tag will be used for identifying this payload
    # across the data collection pipeline further (if necessary)
    res.content.tag = "rha"
    
    # Specify the maximum allowed length of response. Set to 0 for no restriction.
    res.content.max_length = 10000

    # Specify the polling frequency in seconds
    poll.rate_s = 5

    # Specify the variance in your polling frequency. If not 0, the client will
    # then poll with frequency_s = base_rate_s ± variance_s
    # Make sure variance_s > rate_s
    poll.variance_s = 2

    # Specify the number of request attempts the client will make to the server
    # after first error before terminating. These attempts are NOT exponentially
    # backed-off. The fail counter will reset to 0 if client successfully handles
    # the content from server before the fail counter exceeds the max attempts
    poll.max_attempt = 10

    # Specify the logging verbosity for this client, the logs will be prefixed
    # with string OUTPUT - [http.<name>]
    # This logger will be using the Lamina's root logger and will dump its output
    # to same Stream / File as mentioned in the root logger. The level mentioned
    # here will be used for both File and Stream logging of data.
    # The logging levels are same as the root logger's
    # 0 - TRACE     [MOST DETAILED]
    # 1 - DEBUG
    # 2 - INFO
    # 3 - WARN
    # 4 - ERROR
    # 5 - CRITICAL  [MOST CONCISE]
    log.level = 0

```

## Release Notes
- v1.0 (20th April 2023)
    - Base version of HTTP collector.
    - Can setup a variance poller to HTTP endpoint on a server.
    - Support GET, PATCH, POST and PUT type of HTTP requests.
    - Support for sending custom headers in the HTTP requests.
    - Support for dynamically creating URL request parameters via key-map configs.
    - Support for sending custom data block or file as request content.
    - Support for auto, raw and custom decoding parameters for response content.
    - Dedicated and customizable logging handler.
    - Based on [requests](https://pypi.org/project/requests/) package for python.