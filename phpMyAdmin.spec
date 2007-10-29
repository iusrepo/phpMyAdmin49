Name: phpMyAdmin
Version: 2.11.2
Release: 1%{?dist}
Summary: Web based MySQL browser written in php

Group:	Applications/Internet
License: GPLv2+
URL: http://www.phpmyadmin.net/	
Source0: http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-all-languages.tar.bz2
Source1: phpMyAdmin-config.inc.php
Source2: phpMyAdmin.htaccess
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: webserver 
Requires: php >= 4.1.0
Requires: php-mysql  >= 4.1.0
Requires: php-mbstring >= 4.1.0
Requires(postun): /sbin/service
Requires(post): /sbin/service

%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the Web. Currently it can create and drop databases,
create/drop/alter tables, delete/edit/add fields, execute any SQL statement,
manage keys on fields, manage privileges,export data into various formats and
is available in 50 languages

%prep
%setup -qn phpMyAdmin-%{version}-all-languages

%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}
%{__cp} -ad ./* %{buildroot}/%{_datadir}/%{name}
%{__cp} %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/phpMyAdmin.conf
%{__cp} %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}/config.inc.php
ln -s %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%{_datadir}/%{name}/config.inc.php

%{__rm} -f %{buildroot}/%{_datadir}/%{name}/*txt
%{__rm} -f %{buildroot}/%{_datadir}/%{name}/[IRLT]*
%{__rm} -f %{buildroot}/%{_datadir}/%{name}/CREDITS
%{__rm} -f %{buildroot}/%{_datadir}/%{name}/libraries/.htaccess

%clean
rm -rf %{buildroot}

%post
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%postun
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc INSTALL README LICENSE CREDITS TODO Documentation.txt
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/phpMyAdmin.conf
%config(noreplace) %{_sysconfdir}/%{name}

%changelog
* Fri Oct 29 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.2-1
* upstream released new version

* Mon Oct 22 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.1.2-1
* upstream released new version

* Thu Sep 06 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.0-1
- Upstream released new version
- Altered sources file as required
- Added proper license

* Mon Jul 23 2007 Mike McGrath <mmcgrath@redhat.com> 2.10.3-1
- Upstream released new version

* Sat Mar 10 2007 Mike McGrath <mmcgrath@redhat.com> 2.10.0.2-3
- Switched to the actual all-languages, not just utf-8

* Sun Mar 04 2007 Mike McGrath <mmcgrath@redhat.com> 2.10.0.2-1
- Upstream released new version

* Sat Jan 20 2007 Mike McGrath <imlinux@gmail.com> 2.9.2-1
- Upstream released new version

* Fri Dec 08 2006 Mike McGrath <imlinux@gmail.com> 2.9.1.1-2
- Fixed bug in spec file

* Fri Dec 08 2006 Mike McGrath <imlinux@gmail.com> 2.9.1.1-1
- Upstream released new version

* Wed Nov 15 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-3alpha
- Added dist tag

* Wed Nov 15 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-2alpha
- Fixed 215159

* Fri Nov 10 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-1alpha
- Added alpha tag since this is a release candidate

* Tue Nov 07 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-1
- Upstream released new version

* Wed Oct 04 2006 Mike McGrath <imlinux@gmail.com> 2.9.0.2-1
- Upstream released new version

* Thu Jul 06 2006 Mike McGrath <imlinux@gmail.com> 2.8.2-2
- Fixed a typo in the Apache config

* Mon Jul 03 2006 Mike McGrath <imlinux@gmail.com> 2.8.2-1
- Upstream released 2.8.2
- Added more restrictive directives to httpd/conf.d/phpMyAdmin.conf
- removed htaccess file from the libraries dir
- Specific versions for various requires

* Sat May 13 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.4-1
- Upstream released 2.8.0.4
- Added requires php, instead of requires httpd, now using webserver

* Sun May 07 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.3-2
- Added mysql-php and php-mbstring as a requires

* Thu Apr 07 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.3-1
- Fixed XSS vulnerability: PMASA-2006-1
- It was possible to conduct an XSS attack with a direct call to some scripts
- under the themes directory.

* Tue Apr 04 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.2-3
- Made config files actually configs
- Moved doc files to the doc dir

* Tue Apr 04 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.2-2
- Moved everything to %{_datadir}
- Moved config file to /etc/
- Used description from phpMyAdmin project info

* Mon Apr 03 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.2-1
- Initial Spec file creation for Fedora
