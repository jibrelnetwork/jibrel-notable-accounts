builder(
        buildTasks: [
                [
                        name: "Linters",
                        type: "lint",
                        method: "inside",
                        runAsUser: "root",
                        entrypoint: "",
                        command: [
                                "apk add --no-cache gcc build-base",
                                "pip install --no-cache-dir flake8==3.6.0 mypy==0.720",
                                "flake8",
                                "mypy --cache-dir=/dev/null .",
                        ],
                ],
                [
                        name: "Tests",
                        type: "test",
                        method: "inside",
                        runAsUser: "root",
                        command: [
                                "apk add --no-cache gcc build-base",
                                "pip install --no-cache-dir -r requirements/dev.txt",
                                "pytest"
                        ],
                ],
        ],
)
