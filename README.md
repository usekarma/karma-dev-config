# karma-dev-config

This repository defines the configuration and environment metadata used to deploy infrastructure for [`usekarma.dev`](https://usekarma.dev).

This is the only part of the **AWS deployment framework designed to be forked and modified.**  
**You control it, and your fork does not need to be public.**

For a complete overview, see [Adage: AWS Deployment Framework](https://github.com/usekarma/adage).

This repo is designed to declare everything that can be deployed — but actual deployment is controlled separately.

It works together with:
For a complete overview, see [Adage: AWS Deployment Framework](https://github.com/usekarma/adage).

- [Adage: AWS Deployment Framework](https://github.com/usekarma/adage) for orchestration and walkthroughs
- [`aws-iac`](https://github.com/usekarma/aws-iac) for shared Terraform-based infrastructure components
- [`aws-lambda`](https://github.com/usekarma/aws-lambda) for optional Lambda handlers and tools

---

## Repository Structure

```
.
├── account_environments/
│   ├── dev.json           # Defines the environment binding for the 'dev' OU
│   └── prod.json          # Defines the environment binding for the 'prod' OU
├── iac/
│   ├── dev/
│   │   └── serverless-site/
│   │       └── karma-dev/
│   │           └── config.json
│   └── prod/
│       └── ...
├── scripts/
│   ├── define_account_environment.py
│   ├── deploy_config.py
│   ├── validate_account_environment.py
│   └── validate_config.py
```

---

## Developer Setup: AWS CLI Profiles

This project assumes you are using named AWS CLI profiles to authenticate into different AWS accounts.

Each script supports the `AWS_PROFILE` environment variable to explicitly target the correct account. If not set, scripts will default to the AWS CLI's currently active credentials.

To get started:

➡️ [See `setup/bash-aws-profile-prompt.md`](./setup/bash-aws-profile-prompt.md) for a quick explanation of:

- How to authenticate with `aws sso login`
- How to switch accounts using `AWS_PROFILE`
- How to update your terminal prompt and title to show your current profile

This small improvement reduces the chance of deploying to the wrong account and works well for both ad-hoc and CI/CD workflows.

---

## How Configuration Becomes Active

This repository defines configuration that can be deployed — but it is not automatically active.  
Only values that are explicitly published to AWS Systems Manager Parameter Store (via approved scripts) will be used at deploy time.

This two-step process ensures that:

- You can version and review changes in Git before applying them
- Only declared environments and components can be deployed
- Control over this repository — and how it is published to AWS — defines the allowed architecture for your environment

Each AWS account is explicitly bound to one environment by setting a single JSON parameter at `/iac/environment`. All other configuration is defined declaratively under this repo and selected at runtime based on that binding.

---

## Deploying a Config Instance

Once an environment is defined, you may deploy a configuration instance by referencing its logical path under the environment tree.

```bash
AWS_PROFILE=dev-iac python scripts/deploy_config.py --config serverless-site/usekarma-dev
```

- Resolves the current environment and repo via `/iac/environment`
- Clones the configured Git repo and branch
- Loads and validates the referenced config JSON
- (Currently performs dry run; deploy logic can be extended)

---

## Environment Setup

Each AWS account must define its environment binding before any configuration can be deployed. This is done by writing the `/iac/environment` parameter to Systems Manager Parameter Store using the provided script.

Each file in `account_environments/` corresponds to an environment (mapped to an Organizational Unit) and defines how accounts within that environment should be configured and constrained.

### Define the Environment Parameter

To define the environment parameter from the CLI:

```bash
AWS_PROFILE=dev-iac python scripts/define_account_environment.py --env dev
AWS_PROFILE=prod-iac python scripts/define_account_environment.py --env prod
```

- Loads from `account_environments/<env>.json`
- Writes to `/iac/environment` in the target AWS account
- Uses the Standard parameter tier by default

Once this parameter exists, it becomes the source of truth for what config and infrastructure the account is allowed to use.

---

## Roles and Separation of Responsibility

This system is designed to enforce strict separation between:

- **Defining an environment** — done once per account by administrators
- **Deploying a config** — done routinely by developers, CI/CD, or automation tools

Environment binding must be declared before any deployment is possible. IAM policies can be used to protect this parameter in production environments.

---

## Validation Scripts

These help verify correct setup before attempting deployment.

### Validate the environment parameter

```bash
AWS_PROFILE=dev-iac python scripts/validate_account_environment.py
```

- Loads the current value of `/iac/environment` from the AWS account
- Determines the environment name from the `name` field
- Compares it to `account_environments/<name>.json`

### Validate a config instance

```bash
python scripts/validate_config.py --config serverless-site/usekarma-dev
```

Checks that the referenced config exists and is valid JSON.

---

## Security and Governance

- All deployments are gated by the `/iac/environment` parameter
- That parameter is written by script using valid credentials
- IAM policies should restrict `ssm:PutParameter` in production environments
- No configuration is applied unless committed to Git and declared under an approved environment

---

## Customization

- Fork this repository to define your own environments and constraints
- Update `account_environments/` to define new OUs and controls
- Create new deployable configs under `iac/dev/` or `iac/prod/`

---

## License

[Apache 2.0 License](LICENSE)
