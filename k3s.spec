%global k3s_version 1.36.5+k3s1

Name:           k3s
Version:        %{k3s_version}
Release:        1%{?dist}
Summary:        Lightweight Kubernetes

License:        Apache-2.0
URL:            https://k3s.io

%ifarch x86_64
Source0:        https://github.com/k3s-io/k3s/releases/download/v%{version}/k3s
%endif

%ifarch aarch64
Source0:        https://github.com/k3s-io/k3s/releases/download/v%{version}/k3s-arm64
%endif

Source1:        k3s.service
Source2:        k3s.sysconfig

ExclusiveArch:  x86_64 aarch64

Requires:       k3s-selinux
Requires:       systemd
BuildRequires:  systemd-rpm-macros


%description
K3s is a lightweight, fully compliant Kubernetes distribution designed
for production workloads in resource-constrained environments, edge
computing, development, and single-node installations.


%prep
# Binary-only package; nothing to unpack.


%build
# Nothing to build.


%install
install -Dpm0755 %{SOURCE0} %{buildroot}%{_bindir}/k3s
install -Dpm0644 %{SOURCE1} %{buildroot}%{_unitdir}/k3s.service
install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/k3s


%post
%systemd_post k3s.service


%preun
%systemd_preun k3s.service


%postun
%systemd_postun_with_restart k3s.service


%files
%license
%{_bindir}/k3s
%{_unitdir}/k3s.service
%config(noreplace) %{_sysconfdir}/sysconfig/k3s


%changelog
* Tue Oct 06 2026 Mike Gerber <mike@mike-gerber.de> - 1.36.5+k3s1-1
- Initial package
