# Output Plugins

- Lamina is designed as a plugin-first system.
- Output plugins are simple components through which Lamina can dump collected data.
- Lamina comes with a concise set of standard output plugins for most common use cases.
- Lamina promotes creation of custom collectors for any type of job requirement.
- Learn how to create a new plugin [here]()

## Available plugins

- [MQTT](../../lamina/plugins/outputs/mqtt/) : Publish collected data to several MQTT topics on a broker.

## How to use a plugin?

- Read the documentation and understand the config of the plugin you want to use.
- Copy the sample config format for your plugin from ```<plugin>/docs/config.toml``` file.
- Now open the root config file for your Lamina instance, preferrably ```lamina.toml```
- Now go under the ```[outputs]``` section of the config file and paste copied config.
- Give a name for to your plugin in the config ```[outputs.<type>.<name>]```
- Make sure the name is unique for a given type, i.e., you can't have two mqtt plugins with same name. However you may have two different types of plugin with same name.
- Configure the output plugin as you want according to the documentation provided.
- Finally go under the ```[stream]``` section of the config file and add the name of your newly added plugin in the outputs array.
- Save the file, restart your Lamina instance and pray!

Check the following example inside a rudimentary ```lamina.toml``` file where I illustrate adding a new MQTT output plugin named 'Labrador'
```
[lamina]
    // app level configs
    // ..

[inputs]
    // input plugins configs
    // ..

[outputs]
    [outputs.mqtt.someplug]
    // config params
    // ..

    [...]

    [outputs.mqtt.labrador]
    // config params
    // ..

[stream]
    // add your newly configured plugin here
    outputs = ["mqtt.someplug, ... , mqtt.labrador]
```