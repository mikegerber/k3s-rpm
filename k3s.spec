# renovate: datasource=github-releases depName=k3s-io/k3s versioning=loose
%global k3s_upstream_version v1.37.1+k3s1

%global k3s_version %{lua:
  local v = rpm.expand("%{k3s_upstream_version}")
  print(v:match("^v(.+)"))
}

Name:           k3s
Version:        %{k3s_version}
Release:        1%{?dist}
Summary:        Lightweight Kubernetes

License:        Apache-2.0
URL:            https://k3s.io
ExclusiveArch:  x86_64 aarch64


%ifarch x86_64
%global k3s_upstream_arch amd64
%global k3s_upstream_binary k3s
%else
%ifarch aarch64
%global k3s_upstream_arch arm64
%global k3s_upstream_binary k3s-arm64
%endif
%endif

Source0:  https://github.com/k3s-io/k3s/releases/download/%{k3s_upstream_version}/k3s#/k3s-%{k3s_upstream_version}-%{k3s_upstream_arch}
Source10: https://github.com/k3s-io/k3s/releases/download/%{k3s_upstream_version}/sha256sum-%{k3s_upstream_arch}.txt#/sha256sum-%{k3s_upstream_version}-%{k3s_upstream_arch}.txt

Source1:        k3s.service
Source2:        k3s.sysconfig

Source3:  https://raw.githubusercontent.com/k3s-io/k3s/refs/heads/main/LICENSE

Requires:       k3s-selinux
Requires:       systemd

BuildRequires:  coreutils
BuildRequires:  systemd-rpm-macros


%description
K3s is a lightweight, fully compliant Kubernetes distribution designed
for production workloads in resource-constrained environments, edge
computing, development, and single-node installations.


%prep
# Verify the downloaded release binary against the checksum file
# published with the same upstream release.

expected=$(awk '$2 == "%{k3s_upstream_binary}" { print $1 }' %{SOURCE10})
actual=$(sha256sum %{SOURCE0} | awk '{ print $1 }')

if [ -z "$expected" ]; then
    echo "Could not find k3s checksum in %{SOURCE10}" >&2
    exit 1
fi

if [ "$expected" != "$actual" ]; then
    echo "Checksum mismatch:" >&2
    echo "  expected: $expected" >&2
    echo "  actual:   $actual" >&2
    exit 1
fi

cp %{SOURCE3} LICENSE


%build
# Nothing to build.


%install
install -Dpm0755 %{SOURCE0} %{buildroot}%{_bindir}/k3s
install -Dpm0644 %{SOURCE1} %{buildroot}%{_unitdir}/k3s.service
install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/k3s
install -d %{buildroot}%{_sysconfdir}/rancher/k3s


%check
# Check that the installed binary is runnable and returns the correct version.
%{buildroot}%{_bindir}/k3s --version | grep 'version %{k3s_upstream_version}'


%post
%systemd_post k3s.service


%preun
%systemd_preun k3s.service


%postun
%systemd_postun_with_restart k3s.service


%files
%{_bindir}/k3s
%{_unitdir}/k3s.service
%config(noreplace) %{_sysconfdir}/sysconfig/k3s
%dir %{_sysconfdir}/rancher
%dir %{_sysconfdir}/rancher/k3s
%license LICENSE


%changelog
* Tue Oct 06 2026 Mike Gerber <mike@mike-gerber.de> - 1.37.1+k3s1-1
- Revert to using the upstream version scheme
- Add LICENSE

* Tue Oct 06 2026 Mike Gerber <mike@mike-gerber.de> - 1.36.5-1.k3s1
- Initial package
