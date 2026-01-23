# Jenkins_02_INTERMEDIATE

## The Practitioner of Jenkins

*Target Audience*: Junior Developer / Daily User.  
*Philosophy*: Focus on "Getting things done". Standard patterns and libraries.

### Standard Library Usage (Core Jenkins Features for Daily Tasks)
- **Freestyle Jobs Configuration**: Setting up simple jobs with source code management (SCM) polling, build triggers (manual, scheduled via cron, SCM changes), and basic build steps (shell scripts, batch commands, Ant/Maven/Gradle invocations).
- **Pipeline as Code Fundamentals**: Introduction to Jenkins Pipeline for defining build processes as code, including Scripted Pipeline syntax (Groovy-based) vs Declarative Pipeline syntax (structured YAML-like), with focus on reusability and version control.
- **Declarative Pipeline Syntax Essentials**: Key directives such as `agent` (specifying execution environment: any, none, label, docker, kubernetes), `stages` (logical grouping of build phases), `steps` (individual actions like `sh`, `bat`, `echo`), `environment` (global variables), `options` (build timeouts, retry logic), and `post` (cleanup actions with conditions: always, success, failure, unstable, changed).
- **Scripted Pipeline Basics**: Using Groovy scripting for dynamic pipelines, including node allocation, stage definitions, parallel execution, and conditional logic with `if/else` and loops.
- **Common Build Tools Integration**: Maven for Java projects (pom.xml parsing, lifecycle phases: clean, compile, test, package), Gradle for flexible builds (task execution, dependency management), Ant for legacy XML-based builds, and npm/yarn for Node.js projects.

### Common Data Structures (Organizing Build Data)
- **Parameters in Jobs**: Defining build parameters (string, boolean, choice, file) for user input, with validation and default values to customize job runs.
- **Environment Variables**: Setting and using environment variables in pipelines (e.g., `env.BRANCH_NAME`, `env.BUILD_NUMBER`) for dynamic configuration and cross-stage data sharing.
- **Artifacts and Archives**: Storing build outputs (jars, binaries, test reports) using `archiveArtifacts` step, with patterns like `**/target/*.jar` and retention policies.
- **Test Results Parsing**: Integrating JUnit, TestNG, or xUnit test reports for trend analysis, failure detection, and dashboard visualization.
- **Credentials Management**: Storing and retrieving sensitive data (passwords, API keys) via Jenkins credentials store, with types like username/password, secret text, and SSH keys.

### Modular Programming (Reusable Components)
- **Shared Libraries**: Creating and using global shared libraries for common pipeline code, with `vars/` for custom steps (e.g., `def call(Map config)` for parameterized functions) and `src/` for classes.
- **Pipeline Templates**: Defining reusable pipeline templates using `Jenkinsfile` inheritance or library functions to standardize CI/CD across projects.
- **Parameterized Builds**: Using `parameters` block in Declarative pipelines to create flexible jobs that accept inputs like branch names or environment targets.
- **Multi-Branch Pipelines**: Automatic job creation for each branch in a repository, with branch-specific configurations and build strategies (e.g., build PRs, tags).
- **Job DSL (Domain Specific Language)**: Programmatically creating Jenkins jobs using Groovy scripts, including job configurations, views, and folders for automation.

### Error Handling (Robust Build Processes)
- **Try-Catch in Pipelines**: Using `try/catch/finally` blocks in Scripted pipelines for exception handling, with `catchError` step to continue builds on failures.
- **Post Actions in Declarative Pipelines**: Defining `post` blocks for cleanup, notifications, and conditional actions based on build results (e.g., `always { cleanWs() }` for workspace cleanup).
- **Build Stability Checks**: Monitoring build health with metrics like success rate, duration trends, and failure causes using plugins like Build Monitor or Pipeline Stage View.
- **Retry Mechanisms**: Implementing `retry` step for transient failures (e.g., network issues) and `timeout` for preventing hung builds.
- **Failure Notifications**: Integrating email, Slack, or webhook notifications on build failures, with detailed logs and artifact links.

### File I/O (Managing Build Artifacts and Logs)
- **Workspace Management**: Understanding Jenkins workspaces (per-job directories), with `dir` step for changing directories and `stash/unstash` for transferring files between stages/nodes.
- **Artifact Upload/Download**: Using `archiveArtifacts` for storing outputs and `copyArtifacts` for retrieving from other jobs, with filters and permissions.
- **Log Handling**: Accessing and parsing console logs via `currentBuild.rawBuild.log` in scripts, with log rotation and external storage options.
- **File Operations in Steps**: Using `fileExists`, `readFile`, `writeFile` for file checks, reading configurations, and generating reports.
- **Distributed Builds**: Leveraging agent nodes for parallel execution, with file transfer via `stash` for cross-node artifact sharing.

### Additional Practical Patterns
- **Blue-Green Deployments**: Setting up pipelines for zero-downtime deployments using plugins like Blue Ocean or custom scripts.
- **Scheduled Builds**: Configuring cron-based triggers (e.g., `H 2 * * *` for nightly builds) and SCM polling for continuous integration.
- **Integration with Version Control**: Git, SVN, and Mercurial integrations with webhooks, pull request builders, and merge checks.
- **Containerized Builds**: Using Docker agents in pipelines for isolated environments, with `docker.build` and `docker.push` steps.
- **Security Best Practices**: Managing permissions with Role-Based Access Control (RBAC), audit logging, and secure credential usage.

This intermediate syllabus focuses on practical, day-to-day Jenkins usage for building, testing, and deploying applications efficiently.