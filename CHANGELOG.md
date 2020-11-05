## [3.0.8](https://github.com/enter-at/python-aws-lambda-handlers/compare/v3.0.7...v3.0.8) (2020-11-05)


### Bug Fixes

* **HTTPHandler:** do not parse body if value is  None ([bd4402b](https://github.com/enter-at/python-aws-lambda-handlers/commit/bd4402b7f5e5acf0c1c0d1664e109688f484d5ca))

## [3.0.7](https://github.com/enter-at/python-aws-lambda-handlers/compare/v3.0.6...v3.0.7) (2020-11-04)


### Bug Fixes

* **CI:** avoid installing pre-commit in CI pipelines ([4c31d14](https://github.com/enter-at/python-aws-lambda-handlers/commit/4c31d143b7f9f351895a35526f6691ee9f2265d8))
* **CI:** install dev dependencies for the release step ([a63f415](https://github.com/enter-at/python-aws-lambda-handlers/commit/a63f41575f718a7c61da3e7941856beeb59ed6a1))

## [3.0.6](https://github.com/enter-at/python-aws-lambda-handlers/compare/v3.0.5...v3.0.6) (2020-11-04)


### Bug Fixes

* **CI:** fix typo in release step ([8ffefc9](https://github.com/enter-at/python-aws-lambda-handlers/commit/8ffefc9756c7e83572012751c17d02a5c5beebd2))

## [3.0.5](https://github.com/enter-at/python-aws-lambda-handlers/compare/v3.0.4...v3.0.5) (2020-11-04)


### Bug Fixes

* **ci:** add PYPI_PASS & PYPI_USER ([63b3891](https://github.com/enter-at/python-aws-lambda-handlers/commit/63b3891048a3f9875b13c6242d3caa30056f6401))

## [3.0.4](https://github.com/enter-at/python-aws-lambda-handlers/compare/v3.0.3...v3.0.4) (2020-11-04)


### Bug Fixes

* **workflow:** restore semantic release action ([6548dc8](https://github.com/enter-at/python-aws-lambda-handlers/commit/6548dc8e5d129c97bffd49ba33ca68fb8909e475))
* debug pipeline ([ba2dffd](https://github.com/enter-at/python-aws-lambda-handlers/commit/ba2dffd0bd0563a32546d935a0c2935f96e806bc))
* debug pipeline ([d10c8bb](https://github.com/enter-at/python-aws-lambda-handlers/commit/d10c8bb376a211fc5b186321e9bf6b679209cb19))
* **docs:** trigger semantic release ([940b1c8](https://github.com/enter-at/python-aws-lambda-handlers/commit/940b1c82454577a2f16768dbe433d59af464054d))
* **workflow/release:** update bot token ([d6d5f8d](https://github.com/enter-at/python-aws-lambda-handlers/commit/d6d5f8dfa03f8ea0a26f7951890decd2db4f0d82))

## [3.0.3](https://github.com/enter-at/python-aws-lambda-handlers/compare/v3.0.2...v3.0.3) (2020-11-03)


### Bug Fixes

* **errors:** add back EventValidationError as ValidationError ([2eaa8fe](https://github.com/enter-at/python-aws-lambda-handlers/commit/2eaa8fe302520429a0aee217c9df50e5766965e7))

## [3.0.2](https://github.com/enter-at/lambda-handlers/compare/v3.0.1...v3.0.2) (2019-10-05)


### Bug Fixes

* **lambda_handler:** gracefully handle None return values ([1f63abe](https://github.com/enter-at/lambda-handlers/commit/1f63abe))

## [3.0.1](https://github.com/enter-at/lambda-handlers/compare/v3.0.0...v3.0.1) (2019-10-05)


### Bug Fixes

* **lambda_handler:** ensure decorator forwards handler self ([e914f37](https://github.com/enter-at/lambda-handlers/commit/e914f37))

# [3.0.0](https://github.com/enter-at/lambda-handlers/compare/v2.0.1...v3.0.0) (2019-10-04)


### chore

* **marshmallow:** update to version 3.x ([99f935f](https://github.com/enter-at/lambda-handlers/commit/99f935f))


### BREAKING CHANGES

* **marshmallow:** Marshmallow version changed to 3.x

## [2.0.1](https://github.com/enter-at/lambda-handlers/compare/v2.0.0...v2.0.1) (2019-08-02)


### Bug Fixes

* **validators:** import http module ([34387e2](https://github.com/enter-at/lambda-handlers/commit/34387e2))

# [2.0.0](https://github.com/enter-at/lambda-handlers/compare/v1.1.1...v2.0.0) (2019-08-01)


### Bug Fixes

* **LambdaHandler:** remove context option ([29f71c3](https://github.com/enter-at/lambda-handlers/commit/29f71c3))


* Merge pull request #58 from enter-at/fix/remove-context-update ([d79deb8](https://github.com/enter-at/lambda-handlers/commit/d79deb8)), closes [#58](https://github.com/enter-at/lambda-handlers/issues/58)


### BREAKING CHANGES

* The context option has been removed
* **LambdaHandler:** The context option has been removed.

## [1.1.1](https://github.com/enter-at/lambda-handlers/compare/v1.1.0...v1.1.1) (2019-07-30)


### Bug Fixes

* **release:** fix build target in Makefile ([81a4bab](https://github.com/enter-at/lambda-handlers/commit/81a4bab))

# [1.1.0](https://github.com/enter-at/lambda-handlers/compare/v1.0.5...v1.1.0) (2019-07-30)


### Features

* **event_handler:** add EventHandler for non-http handlers ([7c3eca8](https://github.com/enter-at/lambda-handlers/commit/7c3eca8))

## [1.0.5](https://github.com/enter-at/lambda-handlers/compare/v1.0.4...v1.0.5) (2019-07-05)


### Bug Fixes

* **docs:** fix docs build setup to import lambda_handlers ([56f6441](https://github.com/enter-at/lambda-handlers/commit/56f6441))

## [1.0.4](https://github.com/enter-at/lambda-handlers/compare/v1.0.3...v1.0.4) (2019-07-03)


### Bug Fixes

* **validators:** remove marshmallow usage in type hint ([99dada3](https://github.com/enter-at/lambda-handlers/commit/99dada3))

## [1.0.3](https://github.com/enter-at/lambda-handlers/compare/v1.0.2...v1.0.3) (2019-07-02)


### Bug Fixes

* **setup.cfg:** add missing packaging setting ([6cb71dc](https://github.com/enter-at/lambda-handlers/commit/6cb71dc))

## [1.0.2](https://github.com/enter-at/lambda-handlers/compare/v1.0.1...v1.0.2) (2019-07-02)


### Bug Fixes

* **packaging:** add missing pypi configuration ([029524a](https://github.com/enter-at/lambda-handlers/commit/029524a))

## [1.0.1](https://github.com/enter-at/lambda-handlers/compare/v1.0.0...v1.0.1) (2019-07-02)


### Bug Fixes

* **makefile:** remove tag target ([aefe5a6](https://github.com/enter-at/lambda-handlers/commit/aefe5a6))

# 1.0.0 (2019-07-01)


### Bug Fixes

* handle import errors gracefully ([eea9f6f](https://github.com/enter-at/lambda-handlers/commit/eea9f6f))
* **formatters:** add FormattingError exception ([8a94c66](https://github.com/enter-at/lambda-handlers/commit/8a94c66))
* **MarshmallowValidator:** handler empty error messages ([0bf03b0](https://github.com/enter-at/lambda-handlers/commit/0bf03b0))
* **version:** set the version used for pre-release ([3873a5f](https://github.com/enter-at/lambda-handlers/commit/3873a5f))


### Features

* **validator:** add request and response validation ([0e0af4e](https://github.com/enter-at/lambda-handlers/commit/0e0af4e))
* **validator:** add request and response validation ([0029a97](https://github.com/enter-at/lambda-handlers/commit/0029a97))
* **validator:** extract validator abstraction ([bfc697e](https://github.com/enter-at/lambda-handlers/commit/bfc697e))
