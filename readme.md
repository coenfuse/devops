# Lamina

- Lamina is modular, plugin-based data collection agent.
- Provides functionality for realtime data collection from remote or local sources.
- Can configure collection stream to route collected data to databases or any other consumer.
- Does not assume streaming endpoints and features simple configurable IO plugins.
- Focusing to be sandbox agent that can be configured for any fullfil any collection requirements.
- Primarily useful for collecting real-time metrics from remote devices and dumping into database.
- Written purely in Python 3.11 and is available on both Windows and Linux systems.

## How to use

1. Download and extract the .zip file into a folder.
2. Copy the built Lamina artifacts from the required platform folder ( win / lin )
3. Paste the copied artifacts wherever you want in your system
4. Open [config/lamina.toml](config/lamina.toml) file, edit as required and save.
5. Refer to [documentation](docs/plugin) on how to use IO plugins.
5. Start launch.bat or launch.sh file to start your Lamina instance.

## Project

- [Input Plugins](docs/plugins/input.md)
- [Output Plugins](docs/plugins/output.md)
- [Build Lamina](docs/project/build.md)
- [Setup development](docs/project/setup.md)
- [Understand codebase](docs/project/study.md)
- [Test Lamina](docs/project/test.md)

## Contribute

- [Code review](docs/contribute/code_review.md)
- [Pull Requests](docs/contribute/issue_pr.md)
- [Report bugs](docs/contribute/report_bug.md)
- [Write tests](docs/contribute/write_test.md)

## Guidelines

- [Branching](docs/guidelines/branch.md)
- [Commit](docs/guidelines/commit.md)
- [Logging](docs/guidelines/logging.md)
- [Versioning](docs/guidelines/versioning.md)

## Contact

- [@coenfuse](www.twitter.com/coenfuse)