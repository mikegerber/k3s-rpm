## Building the RPM

On a Fedora system:

```
just build
```

This yields the RPMs in your `~/rpmbuild/RPMS` directory by default.


## Updating

Updates to the RPM are handled by Renovate. It updates the `k3s_version` in the spec via a PR on
GitHub.
