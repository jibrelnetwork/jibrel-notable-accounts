builder(
        buildTasks: [
                [
                        name: "Linters",
                        type: "lint",
                        method: "inside",
                        runAsUser: "root",
                        jUnitPath: "/junit-reports",
                        entrypoint: "",
                        command: [
                                "apk add --no-cache gcc build-base",
                                "pip install --no-cache-dir -r requirements/dev.txt",
                                "mkdir -p /junit-reports",
                                "flake8 -v --format junit-xml --output-file=/junit-reports/flake8-junit-report.xml",
                                "mypy --cache-dir=/dev/null --junit-xml=/junit-reports/mypy-junit-report.xml .",

                        ],
                ],
                [
                        name: "Tests",
                        type: "test",
                        method: "inside",
                        runAsUser: "root",
                        jUnitPath: "/junit-reports",
                        coveragePath: "/coverage-reports",
                        entrypoint: "",
                        environment: [
                                DB_DSN: "postgres://app:pass@db/app-db",
                        ],
                        sidecars: [
                                db: [
                                        image: "postgres:11.0-alpine",
                                        environment: [
                                                POSTGRES_USER: "app",
                                                POSTGRES_PASSWORD: "pass",
                                                POSTGRES_DB: "app-db",
                                        ],
                                ],
                        ],
                        command: [
                                "apk add --no-cache gcc build-base",
                                "pip install --no-cache-dir -r requirements/dev.txt",
                                "mkdir -p /junit-reports",
                                "pytest --junitxml=/junit-reports/pytest-junit-report.xml --cov-report xml:/coverage-reports/pytest-coverage-report.xml",
                        ],
                ],
        ],
)
