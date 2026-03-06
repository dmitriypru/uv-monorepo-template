# Contributing to the uv monorepo template

When adding features or fixing bugs in the templates:

1. Ensure the change adheres to the Base + Component structure.
2. If modifying `uv` resolutions, verify workspace globs remain intact.
3. If modifying Dockerfiles, ensure `additional_contexts` and `--mount` strategies retain zero-bloat daemon transfers.
4. Run testing locally: The CI/CD uses `uvx copier copy` to dry-run generation and build the Docker containers. Ensure your changes pass the action workflow.

*Pull requests are welcome!*

## Legal Notice
When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.
