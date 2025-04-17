# karma-dev-config

This repository defines the configuration and environment metadata used to deploy infrastructure for [`usekarma.dev`](https://usekarma.dev) using the [Adage](https://github.com/tstrall/adage) framework.

It is structured to work with Adage's `aws-config` and `aws-iac` repositories and can be used as a real-world example of config-driven AWS deployments.

## 🔧 Structure

- `account_environments/`: Defines environment-level metadata
- `iac/`: Component-level configuration inputs (e.g., for Terraform modules)

## 🔐 License

Licensed under the [Apache License 2.0](LICENSE).

## 📚 More

- Framework: [Adage](https://github.com/tstrall/adage)
- Website: [usekarma.dev](https://usekarma.dev)
