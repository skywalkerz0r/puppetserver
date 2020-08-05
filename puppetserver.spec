Name:           puppetserver
Version:        6.10.0
Release:        1%{?dist}
Summary:        A network tool for managing many disparate systems
License:        ASL 2.0
URL:            http://puppetlabs.com
Source0:        http://downloads.puppetlabs.com/puppet/%{name}-%{version}.tar.gz
Source1:        http://downloads.puppetlabs.com/puppet/%{name}-%{version}.tar.gz.asc
Source2:        README.md
Source3:	LICENSE.md

# Puppetlabs messed up with default paths
Patch01:        0001-Fix-puppet-paths.patch
BuildArch:      noarch
BuildRequires:  puppet >= 6.9.0
BuildRequires:  ruby
BuildRequires:  ruby-devel
BuildRequires:  ruby
BuildRequires:  rubygem-fast_gettext >= 1.2.0
BuildRequires:  rubygem-gettext >= 3.2.9
BuildRequires:  rubygem-hocon >= 1.2.5
BuildRequires:  rubygem-locale >= 2.1.2
BuildRequires:  rubygem-puppetserver-ca = 1.8.0
BuildRequires:  rubygem-text >= 1.3.1

Requires: puppet >= 6.9.0
Requires: java-openjdk >= 1.8.0
Requires: java-openjdk-headless >= 1.8.0
Requires:  ruby
Requires:  ruby-devel
Requires:  rubygem-fast_gettext >= 1.2.0
Requires:  rubygem-gettext >= 3.2.9
Requires:  rubygem-hocon >= 1.2.5
Requires:  rubygem-locale >= 2.1.2
Requires:  rubygem-puppetserver-ca = 1.8.0
Requires:  rubygem-text >= 1.3.1

%description
Puppet lets you centrally manage every important aspect of your system using a
cross-platform specification language that manages all the separate elements
normally aggregated in different files, like users, cron jobs, and hosts,
along with obviously discrete elements like packages, services, and files.

%prep
%setup -q

%patch01 -p1

%build
# Nothing to build

%install
bash controller.sh %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/puppetlabs/server/data/puppetserver/vendored-jruby-gems
mkdir -p %{buildroot}/%{_datadir}/puppetlabs/puppet/lib/ruby/vendor_gems
mkdir -p %{buildroot}/usr/share/puppetlabs/puppet/lib/ruby/vendor_ruby/
ln -s /usr/share/gems/gems/puppetserver-ca-*/lib/puppetserver %{buildroot}/usr/share/puppetlabs/puppet/lib/ruby/vendor_ruby/

# install of puppetserver in /usr/bin
mkdir -p %{buildroot}/usr/bin/
ln -s /usr/share/puppetlabs/bin/puppetserver %{buildroot}/usr/bin/puppetserver

# setup for the first run
mkdir -p %{buildroot}/etc/puppetlabs/code/environments/production/manifest %{buildroot}/etc/puppetlabs/code/environments/production/modules

mkdir %{buildroot}/usr/share/puppetlabs/server/docs
cp %{_sourcedir}/README.md %{buildroot}/usr/share/puppetlabs/server/docs
cp %{_sourcedir}/LICENSE.md %{buildroot}/usr/share/puppetlabs/server/docs

install -Dp -m0644 ext/puppetserver.logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%files
%{_bindir}/puppetserver
%{_exec_prefix}/lib/systemd/system/puppetserver.service
%{_exec_prefix}/lib/tmpfiles.d/puppetserver.conf
%attr(-, puppet, puppet) %{_datadir}/puppetlabs/bin/puppetserver
%dir %attr(-, puppet, puppet) %{_datadir}/puppetlabs/server
%dir %attr(-, puppet, puppet) %{_datadir}/puppetlabs/bin
%attr(-, puppet, puppet) %{_datadir}/puppetlabs/server/apps
%attr(-, puppet, puppet) %{_datadir}/puppetlabs/server/bin
%dir %attr(-, puppet, puppet) %{_datadir}/puppetlabs/server/data
%dir %attr(0755, puppet, puppet) %{_datadir}/puppetlabs/server/data/puppetserver
%dir %attr(0755, puppet, puppet) %{_datadir}/puppetlabs/server/data/puppetserver/jars
%dir %attr(0755, puppet, puppet) %{_datadir}/puppetlabs/server/data/puppetserver/vendored-jruby-gems
%attr(-, puppet, puppet) %{_datadir}/puppetlabs/puppet/lib/ruby/vendor_ruby/puppetserver
%dir %attr(-, puppet, puppet) %{_datadir}/puppetlabs/puppet/lib/ruby/vendor_gems
%config(noreplace) %dir %attr(-, puppet, puppet) %{_sysconfdir}/puppetlabs/code
%config(noreplace) %dir %attr(-, puppet, puppet) %{_sysconfdir}/puppetlabs/code/environments
%config(noreplace) %dir %attr(-, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver
%config(noreplace) %dir %attr(-, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/auth.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/ca.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/global.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/metrics.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/puppetserver.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/web-routes.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/conf.d/webserver.conf
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/logback.xml
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/request-logging.xml
%config(noreplace) %dir %attr(-, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/services.d
%config(noreplace) %attr(644, puppet, puppet) %{_sysconfdir}/puppetlabs/puppetserver/services.d/ca.cfg
%config(noreplace) %{_sysconfdir}/sysconfig/puppetserver
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/logrotate.d/%{name}
%ghost %dir %attr(0755, puppet, puppet) %{_rundir}/puppetlabs/puppetserver
%dir %attr(0755, puppet, puppet) %{_localstatedir}/log/puppetlabs/puppetserver
%doc %dir %attr(-, puppet, puppet) %{_datadir}/puppetlabs/server/docs
%doc %attr(-, puppet, puppet) %{_datadir}/puppetlabs/server/docs/README.md
%license %attr(-, puppet, puppet) %{_datadir}/puppetlabs/server/docs/LICENSE.md

%changelog
* Wed Aug 05 2020 Breno Fernandes <brandfbb@gmail.com> - 6.10.0-1
- Build of puppetserver 6.
