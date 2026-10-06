# renovate: datasource=github-releases depName=k3s-io/k3s versioning=loose
%global k3s_upstream_version v1.37.1+k3s1

%global k3s_version %{lua:
  local v = rpm.expand("%{k3s_upstream_version}")
  print(v:match("^v([^+]+)"))
}

%global k3s_revision %{lua:
  local v = rpm.expand("%{k3s_upstream_version}")
  print(v:match("%+k3s(.+)$"))
}

Name:           k3s
Version:        %{k3s_version}
Release:        %{k3s_revision}.k3s1%{?dist}
Summary:        Lightweight Kubernetes

License:        Apache-2.0
URL:            https://k3s.io
ExclusiveArch:  x86_64 aarch64


%ifarch x86_64
Source0:        https://github.com/k3s-io/k3s/releases/download/%{k3s_upstream_version}/k3s
Source10:       https://github.com/k3s-io/k3s/releases/download/%{k3s_upstream_version}/sha256sum-amd64.txt
%endif

%ifarch aarch64
Source0:        https://github.com/k3s-io/k3s/releases/download/%{k3s_upstream_version}/k3s-arm64
Source10:       https://github.com/k3s-io/k3s/releases/download/%{k3s_upstream_version}/sha256sum-arm64.txt
%endif

Source1:        k3s.service
Source2:        k3s.sysconfig

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

%ifarch x86_64
expected=$(awk '$2 == "k3s" { print $1 }' %{SOURCE10})
%endif

%ifarch aarch64
expected=$(awk '$2 == "k3s-arm64" { print $1 }' %{SOURCE10})
%endif

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


%build
# Nothing to build.


%install
install -Dpm0755 %{SOURCE0} %{buildroot}%{_bindir}/k3s
install -Dpm0644 %{SOURCE1} %{buildroot}%{_unitdir}/k3s.service
install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/k3s
install -d %{buildroot}%{_sysconfdir}/rancher/k3s


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


%changelog
* Tue Oct 06 2026 Mike Gerber <mike@mike-gerber.de> - 1.36.5-1.k3s1
- Initial package
