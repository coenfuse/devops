# Input Plugins

- Lamina is designed as a plugin-first system.
- Input plugins are simple components through which Lamina can collect data.
- Lamina comes with a concise set of standard input plugins for most common use cases.
- Lamina promotes creation of custom collectors for any type of job requirement.
- Learn how to create a new plugin [here]()

## Available plugins

- [HTTP](../../lamina/plugins/inputs/http/) : Poll a HTTP server on an endpoint to collect data.
- [MQTT](../../lamina/plugins/inputs/mqtt/) : Subscribe to MQTT topics on a broker and start receiving data.

## How to use a plugin?

- Read the documentation and understand the config of the plugin you want to use.
- Copy the sample config format for your plugin from ```<plugin>/docs/config.toml``` file.
- Now open the root config file for your Lamina instance, preferrably ```lamina.toml```
- Now go under the ```[inputs]``` section of the config file and paste copied config.
- Give a name for to your plugin in the config ```[inputs.<type>.<name>]```
- Make sure the name is unique for a given type, i.e., you can't have two http plugins with same name. However you may have two different types of plugin with same name.
- Configure the input plugin as you want according to the documentation provided.
- Finally go under the ```[stream]``` section of the config file and add the name of your newly added plugin in the inputs array.
- Save the file, restart your Lamina instance and pray!

Check the following example inside a rudimentary ```lamina.toml``` file where I illustrate adding a new HTTP plugin named 'Pitbull'
```
[lamina]
    // app level configs
    // ..

[inputs]
    [inputs.http.someplug]
    // config params
    // ..

    [...]

    [inputs.http.pitbull]
    // config params
    // ..

[outputs]
    // output plugins configs
    // ..

[stream]
    // add your newly configured plugin here
    inputs = ["http.someplug, ... , http.pitbull]
```