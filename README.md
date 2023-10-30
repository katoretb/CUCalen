# CU-CALENDAR BAZOOKA!

This Repository serves as a testing ground for my contribution to the project.
Due to the experimental nature of my features, wacky errors are common.
Feel free to gather handy information here, but don't be too surprised if you happen to find out that
the comprehension rate of you towards this repository is very low. It's wacky, after all.

## Why BAZOOKA?

Testing out features in a way that's comparable to SPAMMING 360 NO SCOPE WITH A BAZOOKA!
Also because "Bazooka" is one funny word, at least to me.

## Something to note

1) All Docker Images prior to the release of [BAZOOKA] was deleted.

- v2.3.0 for Version 2 (DOCKER HUB VERSION) [BAZOOKA]
- v3.1.0 for Version 3 (GHCR VERSION) [BAZOOKA]

2) All GitHub Action Logs prior to firing the BAZOOKA (commit 4e329f0) was also deleted.

So that's why you cannot find any of these artifacts anymore.

3) Throughout all versions there's a noticable change in the way packages are tagged.
I wouldn't recommend any config prior to [BAZOOKA] if you cared about Semantic Versioning
because it recognizes beta versions as latest. The way semver works is different too, but that's just preference.

## Development Logs (Versions)

### Version 1 (1.0.0 and beyond)

- v1.2.4 is nothing more than just a payload to trigger GitHub Actions
- That's it, there's only one in this group

### Version 2 (2.0.0 and beyond) (DOCKER HUB VERSION)

- v2.0.0 [NONE] introduces both frontend and backend integration (CI)
- v2.1.0 [OPTIMIZED] is the optimized version of v2.0.0 (does not login when not needed)
- v2.2.0 [GODMODE] introduces signing the packages using sigstore/cosign (removed in v2.3.0)
- v2.2.1 [GODMODE-WITH-SCRIPT] introduces a script to help with creating the frontend.yml file
- v2.3.0 [BAZOOKA] removed sigstore/cosign integration because of it being too much of a hassle for us

### Version 3 (3.0.0 and beyond) (GHCL Version)

- GHCL stands for "GitHub Container Registry"
- v3.0.0 [GODMODE] same with v2.2.0 except that it pushes to GHCL rather than Docker Hub
- v3.1.0 [BAZOOKA] same with v2.3.0 except that it pushes to GHCL rather than Docker Hub
- v3.2.0 [SANE-SEMVER] the first sane version since OPTIMIZED, utilizing Semantic Versioning
- v3.2.1 [SANE-TAG] like v3.2.0 but instead of utilizing semver, it just tags the packages using the corresponding git tag

