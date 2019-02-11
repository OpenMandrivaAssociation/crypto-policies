%global git_date 20190211
%global git_commit_hash e3eacfcd06d8897ad6771b0673d8974048d3b11a

Name:           crypto-policies
Version:        %{git_date}
Release:        1
Summary:        Systemwide crypto policies

License:        LGPLv2+
URL:            https://gitlab.com/redhat-crypto/fedora-crypto-policies

# This is a tarball of the git repository without the .git/
# directory.
Source0:        https://gitlab.com/redhat-crypto/fedora-crypto-policies/-/archive/master/fedora-crypto-policies-%{git_commit_hash}.tar.bz2

BuildArch: noarch
BuildRequires: asciidoc
BuildRequires: xsltproc
BuildRequires: openssl
BuildRequires: gnutls >= 3.6.0
BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: perl-interpreter
BuildRequires: perl(File::Temp), perl(File::Copy)
BuildRequires: perl(File::Which), perl(File::pushd)
BuildRequires: python3

# used by update-crypto-policies
Requires: coreutils
Requires: grep
Requires: sed
Requires(post): coreutils
Requires(post): grep
Requires(post): sed

%description
This package provides a tool update-crypto-policies, which sets
the policy applicable for the various cryptographic back-ends, such as
SSL/TLS libraries. The policy set by the tool will be the default policy
used by these back-ends unless the application user configures them otherwise.

The package also provides a tool fips-mode-setup, which can be used
to enable or disable the system FIPS mode.

%prep
%setup -q -n fedora-%{name}-master-%{git_commit_hash}

%build
make %{?_smp_mflags}

%install
mkdir -p -m 755 %{buildroot}%{_datarootdir}/crypto-policies/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/local.d/
mkdir -p -m 755 %{buildroot}%{_bindir}

make DESTDIR=%{buildroot} DIR=%{_datarootdir}/crypto-policies MANDIR=%{_mandir} %{?_smp_mflags} install
install -p -m 644 default-config %{buildroot}%{_sysconfdir}/crypto-policies/config

%check
#make check %{?_smp_mflags}

%post
%{_bindir}/update-crypto-policies --no-check >/dev/null


%files

%dir %{_sysconfdir}/crypto-policies/
%dir %{_sysconfdir}/crypto-policies/back-ends/
%dir %{_sysconfdir}/crypto-policies/local.d/
%dir %{_datarootdir}/crypto-policies/

%config(noreplace) %{_sysconfdir}/crypto-policies/config

%ghost %{_sysconfdir}/crypto-policies/back-ends/gnutls.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openssl.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/opensslcnf.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openssh.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/opensshserver.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/nss.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/bind.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/java.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/krb5.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openjdk.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/libreswan.config

%{_bindir}/update-crypto-policies
%{_bindir}/fips-mode-setup
%{_bindir}/fips-finish-install
%{_mandir}/man7/crypto-policies.7*
%{_mandir}/man8/update-crypto-policies.8*
%{_mandir}/man8/fips-mode-setup.8*
%{_mandir}/man8/fips-finish-install.8*
%{_datarootdir}/crypto-policies/LEGACY/*
%{_datarootdir}/crypto-policies/DEFAULT/*
%{_datarootdir}/crypto-policies/NEXT/*
%{_datarootdir}/crypto-policies/FUTURE/*
%{_datarootdir}/crypto-policies/FIPS/*
%{_datarootdir}/crypto-policies/EMPTY/*
%{_datarootdir}/crypto-policies/default-config
%{_datarootdir}/crypto-policies/reload-cmds.sh

%{!?_licensedir:%global license %%doc}
%license COPYING.LESSER
