%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global pkgname	phpMyAdmin

# Having below mentioned separate projects externally or only internally?
%global gettext	1
%global tcpdf	1

%if 0%{?fedora} >= 21
# nginx 1.6 with nginx-filesystem
%global with_nginx     1
# httpd 2.4 with httpd-filesystem
%global with_httpd     1
%else
%global with_nginx     0
%global with_httpd     0
%endif

Summary:	Handle the administration of MySQL over the World Wide Web
Name:		phpMyAdmin
Version:	4.4.15
Release:	1%{?dist}
# MIT (js/jquery/, js/canvg/, js/codemirror/, libraries/sql-formatter/),
# BSD (libraries/plugins/auth/recaptcha/),
# GPLv2+ (the rest)
License:	GPLv2+ and MIT and BSD
Group:		Applications/Internet
URL:		https://www.phpmyadmin.net/
Source0:	https://files.phpmyadmin.net/%{name}/%{version}/%{name}-%{version}-all-languages.tar.xz
Source1:	https://files.phpmyadmin.net/%{name}/%{version}/%{name}-%{version}-all-languages.tar.xz.asc
Source2:	phpMyAdmin-config.inc.php
Source3:	phpMyAdmin.htaccess
Source4:	phpMyAdmin.nginx
# Optional (and partially redundant) runtime requirements: php-bcmath, php-gmp, php-recode, php-soap,
# php-mcrypt, php-phpseclib-crypt-aes >= 2.0.0, php-phpseclib-crypt-random >= 2.0.0
Requires:	php(language) >= 5.3.7, php-filter, php-xmlwriter
%if %{with_nginx}
Requires:	nginx-filesystem
%endif
%if %{with_httpd}
Requires:	httpd-filesystem
Requires:	php(httpd)
Suggests:	httpd
%endif
Requires:	webserver, php-bz2, php-ctype, php-curl, php-date, php-gd >= 5.3.7, php-iconv
Requires:	php-json, php-libxml, php-mbstring >= 5.3.7, php-mysqli >= 5.3.7, php-openssl
Requires:	php-pcre, php-session, php-simplexml, php-spl, php-zip, php-zlib
%if 0%{?gettext}
Requires:	php-php-gettext
%endif
# Optional runtime requirements for tcpdf: php-openssl, php-tidy (usually not required in phpMyAdmin)
%if 0%{?tcpdf}
Requires:	php-tcpdf, php-tcpdf-dejavu-sans-fonts
%else
Requires:	php-hash, php-xml >= 5.3.7
%endif
Provides:	phpmyadmin = %{version}-%{release}
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the World Wide Web. Most frequently used operations are supported
by the user interface (managing databases, tables, fields, relations, indexes,
users, permissions), while you still have the ability to directly execute any
SQL statement.

Features include an intuitive web interface, support for most MySQL features
(browse and drop databases, tables, views, fields and indexes, create, copy,
drop, rename and alter databases, tables, fields and indexes, maintenance
server, databases and tables, with proposals on server configuration, execute,
edit and bookmark any SQL-statement, even batch-queries, manage MySQL users
and privileges, manage stored procedures and triggers), import data from CSV
and SQL, export data to various formats: CSV, SQL, XML, PDF, OpenDocument Text
and Spreadsheet, Word, Excel, LATEX and others, administering multiple servers,
creating PDF graphics of your database layout, creating complex queries using
Query-by-example (QBE), searching globally in a database or a subset of it,
transforming stored data into any format using a set of predefined functions,
like displaying BLOB-data as image or download-link and much more...

%prep
%setup -q -n %{pkgname}-%{version}-all-languages

# Setup vendor config file
sed -e "/'CHANGELOG_FILE'/s@./ChangeLog@%{_pkgdocdir}/ChangeLog@" \
    -e "/'LICENSE_FILE'/s@./LICENSE@%{_pkgdocdir}/LICENSE@" \
    -e "/'CONFIG_DIR'/s@'./'@'%{_sysconfdir}/%{pkgname}/'@" \
    -e "/'SETUP_CONFIG_FILE'/s@./config/config.inc.php@%{_localstatedir}/lib/%{pkgname}/config/config.inc.php@" \
%if 0%{?gettext}
    -e "/'GETTEXT_INC'/s@./libraries/php-gettext/gettext.inc@%{_datadir}/php/gettext/gettext.inc@" \
%endif
%if 0%{?tcpdf}
    -e "/'TCPDF_INC'/s@./libraries/tcpdf/tcpdf.php@%{_datadir}/php/tcpdf/tcpdf.php@" \
%endif
    -e "/'PHPSECLIB_INC_DIR'/s@./libraries/phpseclib@%{_datadir}/pear@" \
%if 0%{?_licensedir:1}
    -e '/LICENSE_FILE/s:%_defaultdocdir:%_defaultlicensedir:' \
%endif
    -i libraries/vendor_config.php

# Remove bundled libraries
%if 0%{?gettext}
rm -rf libraries/php-gettext/
%endif

%if 0%{?tcpdf}
rm -rf libraries/tcpdf/
%endif

rm -rf libraries/phpseclib/

# Remove sources of JavaScript libraries
rm -rf js/jquery/src/ js/openlayers/src/

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{pkgname}/{upload,save,config}/
cp -ad * $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/
install -Dpm 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{pkgname}.conf
install -Dpm 0640 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{pkgname}/config.inc.php
%if %{with_nginx}
install -Dpm 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/%{pkgname}.conf
%endif

rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/{[CDLR]*,*.txt,config.sample.inc.php}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/{doc,examples}/
rm -f doc/html/.buildinfo

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/doc/
ln -s ../../../..%{_pkgdocdir}/html/ $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/doc/html
mv -f config.sample.inc.php examples/

mv -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/js/jquery/MIT-LICENSE.txt LICENSE-jquery
mv -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/js/canvg/MIT-LICENSE.txt LICENSE-canvg
mv -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/js/codemirror/LICENSE LICENSE-codemirror
mv -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/libraries/plugins/auth/recaptcha/LICENSE LICENSE-recaptcha
mv -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/libraries/sql-formatter/LICENSE.txt LICENSE-sql-formatter
%if ! 0%{?tcpdf}
mv -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/libraries/tcpdf/LICENSE.TXT LICENSE-tcpdf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Generate a secret key for this installation
sed -e "/'blowfish_secret'/s/MUSTBECHANGEDONINSTALL/$RANDOM$RANDOM$RANDOM$RANDOM/" \
    -i %{_sysconfdir}/%{pkgname}/config.inc.php

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc ChangeLog README DCO doc/html/ examples/
%{_datadir}/%{pkgname}/
%dir %attr(0750,root,apache) %{_sysconfdir}/%{pkgname}/
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/%{pkgname}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{pkgname}.conf
%if %{with_nginx}
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{pkgname}.conf
%endif
%dir %{_localstatedir}/lib/%{pkgname}/
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{pkgname}/upload/
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{pkgname}/save/
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{pkgname}/config/

%changelog
* Sun Sep 20 2015 Robert Scheck <robert@fedoraproject.org> 4.4.15-1
- Upgrade to 4.4.15

* Tue Sep 08 2015 Robert Scheck <robert@fedoraproject.org> 4.4.14.1-1
- Upgrade to 4.4.14.1

* Thu Aug 20 2015 Robert Scheck <robert@fedoraproject.org> 4.4.14-1
- Upgrade to 4.4.14

* Sat Aug 08 2015 Robert Scheck <robert@fedoraproject.org> 4.4.13.1-1
- Upgrade to 4.4.13.1

* Fri Aug 07 2015 Robert Scheck <robert@fedoraproject.org> 4.4.13-1
- Upgrade to 4.4.13

* Thu Jul 21 2015 Robert Scheck <robert@fedoraproject.org> 4.4.12-1
- Upgrade to 4.4.12 (thanks to Remi Collet)

* Mon Jul 06 2015 Robert Scheck <robert@fedoraproject.org> 4.4.11-1
- Upgrade to 4.4.11

* Sat Jun 20 2015 Robert Scheck <robert@fedoraproject.org> 4.4.10-1
- Upgrade to 4.4.10 (#1232982)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Robert Scheck <robert@fedoraproject.org> 4.4.9-1
- Upgrade to 4.4.9

* Thu May 28 2015 Robert Scheck <robert@fedoraproject.org> 4.4.8-1
- Upgrade to 4.4.8

* Sat May 16 2015 Robert Scheck <robert@fedoraproject.org> 4.4.7-1
- Upgrade to 4.4.7 (#1222215)

* Thu May 14 2015 Robert Scheck <robert@fedoraproject.org> 4.4.6.1-1
- Upgrade to 4.4.6.1 (#1221418, #1221580, #1221581)

* Thu May 07 2015 Robert Scheck <robert@fedoraproject.org> 4.4.6-1
- Upgrade to 4.4.6

* Tue May 05 2015 Robert Scheck <robert@fedoraproject.org> 4.4.5-1
- Upgrade to 4.4.5 (#1218633)

* Sun Apr 26 2015 Robert Scheck <robert@fedoraproject.org> 4.4.4-1
- Upgrade to 4.4.4 (#1215417)

* Mon Apr 20 2015 Robert Scheck <robert@fedoraproject.org> 4.4.3-1
- Upgrade to 4.4.3

* Mon Apr 13 2015 Robert Scheck <robert@fedoraproject.org> 4.4.2-1
- Upgrade to 4.4.2

* Fri Apr 10 2015 Robert Scheck <robert@fedoraproject.org> 4.4.1.1-1
- Upgrade to 4.4.1.1 (#1208320)

- Mon Apr 06 2015 Robert Scheck <robert@fedoraproject.org> 4.4.0-1
- Upgrade to 4.4.0 (thanks to Remi Collet)

* Mon Mar 30 2015 Robert Scheck <robert@fedoraproject.org> 4.3.13-1
- Upgrade to 4.3.13

* Sat Mar 14 2015 Robert Scheck <robert@fedoraproject.org> 4.3.12-1
- Upgrade to 4.3.12

* Wed Mar 04 2015 Robert Scheck <robert@fedoraproject.org> 4.3.11.1-1
- Upgrade to 4.3.11.1

* Tue Mar 03 2015 Robert Scheck <robert@fedoraproject.org> 4.3.11-1
- Upgrade to 4.3.11

* Sat Feb 21 2015 Robert Scheck <robert@fedoraproject.org> 4.3.10-1
- Upgrade to 4.3.10 (#1194949)

* Fri Feb 06 2015 Robert Scheck <robert@fedoraproject.org> 4.3.9-1
- Upgrade to 4.3.9

* Sat Jan 24 2015 Robert Scheck <robert@fedoraproject.org> 4.3.8-1
- Upgrade to 4.3.8

* Sat Jan 24 2015 Robert Scheck <robert@fedoraproject.org> 4.3.7-1
- Upgrade to 4.3.7 (#1183602)

* Wed Jan 07 2015 Robert Scheck <robert@fedoraproject.org> 4.3.6-1
- Upgrade to 4.3.6

* Mon Jan 05 2015 Robert Scheck <robert@fedoraproject.org> 4.3.5-1
- Upgrade to 4.3.5

* Sun Jan 04 2015 Robert Scheck <robert@fedoraproject.org> 4.3.4-1
- Upgrade to 4.3.4 (#1178413)

* Sun Dec 21 2014 Robert Scheck <robert@fedoraproject.org> 4.3.3-1
- Upgrade to 4.3.3

* Fri Dec 12 2014 Robert Scheck <robert@fedoraproject.org> 4.3.2-1
- Upgrade to 4.3.2

* Thu Dec 11 2014 Robert Scheck <robert@fedoraproject.org> 4.3.1-2
- Use %%{pkgname} rather %%{name} in %%post scriptlet (#1173189)

* Tue Dec 09 2014 Robert Scheck <robert@fedoraproject.org> 4.3.1-1
- Upgrade to 4.3.1

* Sat Dec 06 2014 Robert Scheck <robert@fedoraproject.org> 4.3.0-1
- Upgrade to 4.3.0 (thanks to Remi Collet)

* Thu Dec 04 2014 Robert Scheck <robert@fedoraproject.org> 4.2.13.1-1
- Upgrade to 4.2.13.1

* Sun Nov 30 2014 Robert Scheck <robert@fedoraproject.org> 4.2.13-1
- Upgrade to 4.2.13

* Thu Nov 20 2014 Robert Scheck <robert@fedoraproject.org> 4.2.12-1
- Upgrade to 4.2.12 (#1166397)

* Sat Nov 01 2014 Robert Scheck <robert@fedoraproject.org> 4.2.11-1
- Upgrade to 4.2.11 (#1159524)

* Wed Oct 22 2014 Robert Scheck <robert@fedoraproject.org> 4.2.10.1-1
- Upgrade to 4.2.10.1 (#1155272, #1155362)

* Mon Oct 13 2014 Robert Scheck <robert@fedoraproject.org> 4.2.10-1
- Upgrade to 4.2.10 (#1152115)

* Sat Oct  4 2014 Remi Collet <remi@fedoraproject.org> 4.2.9.1-2
- provide nginx configuration (Fedora >= 21)
- fix license handling

* Thu Oct 02 2014 Robert Scheck <robert@fedoraproject.org> 4.2.9.1-1
- Upgrade to 4.2.9.1 (#1148664)

* Sun Sep 21 2014 Robert Scheck <robert@fedoraproject.org> 4.2.9-1
- Upgrade to 4.2.9
- Set default charset for Apache explicitly

* Wed Sep 17 2014 Robert Scheck <robert@fedoraproject.org> 4.2.8.1-2
- Move rm(1) calls from %%install to %%prep (#1121355 #c10)

* Tue Sep 16 2014 Robert Scheck <robert@fedoraproject.org> 4.2.8.1-1
- Upgrade to 4.2.8.1 (#1141635)

* Mon Sep 01 2014 Robert Scheck <robert@fedoraproject.org> 4.2.8-1
- Upgrade to 4.2.8

* Mon Aug 18 2014 Robert Scheck <robert@fedoraproject.org> 4.2.7.1-1
- Upgrade to 4.2.7.1 (#1130865, #1130866, #1131104)

* Thu Jul 31 2014 Robert Scheck <robert@fedoraproject.org> 4.2.7-1
- Upgrade to 4.2.7

* Sat Jul 19 2014 Robert Scheck <robert@fedoraproject.org> 4.2.6-1
- Upgrade to 4.2.6 (#548260, #959946, #989660, #989668, #993613
  and #1000261, #1067713, #1110877, #1117600, #1117601)
- Switch from HTTP- to cookie-based authentication (for php-fpm)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.5.8.2-2
- Fix paths to changelog and license when doc dir is unversioned (#994036).
- Fix source URL, use xz compressed tarball.

* Wed Oct 09 2013 Paul Wouters <pwouters@redhat.com> - 3.5.8.2-1
- Upgrade to 3.5.8.2 (Various security issues)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Robert Scheck <robert@fedoraproject.org> 3.5.8.1-1
- Upgrade to 3.5.8.1 (#956398, #956401)

* Sat Apr 13 2013 Robert Scheck <robert@fedoraproject.org> 3.5.8-1
- Upgrade to 3.5.8 (#949868)

* Sat Feb 23 2013 Robert Scheck <robert@fedoraproject.org> 3.5.7-1
- Upgrade to 3.5.7 (#912097)

* Sun Feb 10 2013 Robert Scheck <robert@fedoraproject.org> 3.5.6-1
- Upgrade to 3.5.6 (#889450)

* Sun Nov 18 2012 Robert Scheck <robert@fedoraproject.org> 3.5.4-1
- Upgrade to 3.5.4 (#877727)

* Tue Oct 09 2012 Robert Scheck <robert@fedoraproject.org> 3.5.3-1
- Upgrade to 3.5.3

* Wed Aug 15 2012 Robert Scheck <robert@fedoraproject.org> 3.5.2.2-1
- Upgrade to 3.5.2.2 (#845736)

* Sat Aug 11 2012 Robert Scheck <robert@fedoraproject.org> 3.5.2.1-1
- Upgrade to 3.5.2.1 (#845736)

* Mon Jul 30 2012 Robert Scheck <robert@fedoraproject.org> 3.5.2-1
- Upgrade to 3.5.2 (#838310)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Robert Scheck <robert@fedoraproject.org> 3.5.1-1
- Upgrade to 3.5.1 (#819171)

* Sat May 05 2012 Remi Collet <remi@fedoraproject.org> 3.5.0-2
- make configuration compatible apache 2.2 / 2.4

* Sun Apr 08 2012 Robert Scheck <robert@fedoraproject.org> 3.5.0-1
- Upgrade to 3.5.0 (#790782, #795020, #809146)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Robert Scheck <robert@fedoraproject.org> 3.4.9-1
- Upgrade to 3.4.9 (#769818)

* Sun Dec 04 2011 Robert Scheck <robert@fedoraproject.org> 3.4.8-1
- Upgrade to 3.4.8 (#759441)

* Sat Nov 12 2011 Robert Scheck <robert@fedoraproject.org> 3.4.7.1-1
- Upgrade to 3.4.7.1 (#753119)

* Sat Nov 05 2011 Robert Scheck <robert@fedoraproject.org> 3.4.7-1
- Upgrade to 3.4.7 (#746630, #746880)

* Sun Sep 18 2011 Robert Scheck <robert@fedoraproject.org> 3.4.5-1
- Upgrade to 3.4.5 (#733638, #738681, #629214)

* Thu Aug 25 2011 Robert Scheck <robert@fedoraproject.org> 3.4.4-1
- Upgrade to 3.4.4 (#733475, #733477, #733480)

* Tue Jul 26 2011 Robert Scheck <robert@fedoraproject.org> 3.4.3.2-2
- Disabled the warning for missing internal database relation
- Reworked spec file to build phpMyAdmin3 for RHEL 5 (#725885)

* Mon Jul 25 2011 Robert Scheck <robert@fedoraproject.org> 3.4.3.2-1
- Upgrade to 3.4.3.2 (#725377, #725381, #725382, #725383, #725384)

* Wed Jul 06 2011 Robert Scheck <robert@fedoraproject.org> 3.4.3.1-1
- Upgrade to 3.4.3.1 (#718964)

* Mon Jun 13 2011 Robert Scheck <robert@fedoraproject.org> 3.4.2-1
- Upgrade to 3.4.2 (#711743)

* Sun May 29 2011 Robert Scheck <robert@fedoraproject.org> 3.4.1-1
- Upgrade to 3.4.1 (#704171)

* Mon Mar 21 2011 Robert Scheck <robert@fedoraproject.org> 3.3.10-1
- Upstream released 3.3.10 (#661335, #662366, #662367, #689213)

* Sun Feb 13 2011 Robert Scheck <robert@fedoraproject.org> 3.3.9.2-1
- Upstream released 3.3.9.2 (#676172)

* Thu Feb 10 2011 Robert Scheck <robert@fedoraproject.org> 3.3.9.1-1
- Upstream released 3.3.9.1 (#676172)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Robert Scheck <robert@fedoraproject.org> 3.3.9-1
- Upstream released 3.3.9 (#666925)

* Mon Nov 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.8.1-1
- Upstream released 3.3.8.1

* Fri Oct 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.8-1
- Upstream released 3.3.8 (#631748)

* Wed Sep 08 2010 Robert Scheck <robert@fedoraproject.org> 3.3.7-1
- Upstream released 3.3.7 (#631824, #631829)

* Sun Aug 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.6-1
- Upstream released 3.3.6 (#628301)

* Fri Aug 20 2010 Robert Scheck <robert@fedoraproject.org> 3.3.5.1-1
- Upstream released 3.3.5.1 (#625877, #625878)
- Added patch to fix wrong variable check at nopassword (#622428)

* Tue Jul 27 2010 Robert Scheck <robert@fedoraproject.org> 3.3.5-1
- Upstream released 3.3.5 (#618586)

* Tue Jun 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.4-1
- Upstream released 3.3.4 (#609057)

* Sat Jun 26 2010 Robert Scheck <robert@fedoraproject.org> 3.3.3-1
- Upstream released 3.3.3 (#558322, #589288, #589487)

* Sun Jan 10 2010 Robert Scheck <robert@fedoraproject.org> 3.2.5-1
- Upstream released 3.2.5

* Thu Dec 03 2009 Robert Scheck <robert@fedoraproject.org> 3.2.4-1
- Upstream released 3.2.4 (#540871, #540891)

* Thu Nov 05 2009 Robert Scheck <robert@fedoraproject.org> 3.2.3-1
- Upstream released 3.2.3

* Tue Oct 13 2009 Robert Scheck <robert@fedoraproject.org> 3.2.2.1-1
- Upstream released 3.2.2.1 (#528769)
- Require php-mcrypt for cookie authentication (#526979)

* Sun Sep 13 2009 Robert Scheck <robert@fedoraproject.org> 3.2.2-1
- Upstream released 3.2.2

* Sun Sep 06 2009 Robert Scheck <robert@fedoraproject.org> 3.2.1-2
- Added ::1 for localhost/loopback access (for IPv6 users)

* Mon Aug 10 2009 Robert Scheck <robert@fedoraproject.org> 3.2.1-1
- Upstream released 3.2.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Robert Scheck <robert@fedoraproject.org> 3.2.0.1-1
- Upstream released 3.2.0.1 (#508879)

* Tue Jun 30 2009 Robert Scheck <robert@fedoraproject.org> 3.2.0-1
- Upstream released 3.2.0

* Fri May 15 2009 Robert Scheck <robert@fedoraproject.org> 3.1.5-1
- Upstream released 3.1.5

* Sat Apr 25 2009 Robert Scheck <robert@fedoraproject.org> 3.1.4-1
- Upstream released 3.1.4

* Tue Apr 14 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3.2-1
- Upstream released 3.1.3.2 (#495768)

* Wed Mar 25 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3.1-1
- Upstream released 3.1.3.1 (#492066)

* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3-1
- Upstream released 3.1.3

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 3.1.2-2
- Rebuilt against rpm 4.6

* Tue Jan 20 2009 Robert Scheck <robert@fedoraproject.org> 3.1.2-1
- Upstream released 3.1.2

* Thu Dec 11 2008 Robert Scheck <robert@fedoraproject.org> 3.1.1-1
- Upstream released 3.1.1 (#475954)

* Sat Nov 29 2008 Robert Scheck <robert@fedoraproject.org> 3.1.0-1
- Upstream released 3.1.0
- Replaced LocationMatch with Directory directive (#469451)

* Thu Oct 30 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1.1-1
- Upstream released 3.0.1.1 (#468974)

* Wed Oct 22 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1-1
- Upstream released 3.0.1

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-1
- Upstream released 3.0.0

* Mon Sep 22 2008 Robert Scheck <robert@fedoraproject.org> 2.11.9.2-1
- Upstream released 2.11.9.2 (#463260)

* Tue Sep 16 2008 Robert Scheck <robert@fedoraproject.org> 2.11.9.1-1
- Upstream released 2.11.9.1 (#462430)

* Fri Aug 29 2008 Robert Scheck <robert@fedoraproject.org> 2.11.9-1
- Upstream released 2.11.9

* Mon Jul 28 2008 Robert Scheck <robert@fedoraproject.org> 2.11.8.1-1
- Upstream released 2.11.8.1 (#456637, #456950)

* Mon Jul 28 2008 Robert Scheck <robert@fedoraproject.org> 2.11.8-1
- Upstream released 2.11.8 (#456637)

* Tue Jul 15 2008 Robert Scheck <robert@fedoraproject.org> 2.11.7.1-1
- Upstream released 2.11.7.1 (#455520)

* Mon Jun 23 2008 Robert Scheck <robert@fedoraproject.org> 2.11.7-1
- Upstream released 2.11.7 (#452497)

* Tue Apr 29 2008 Robert Scheck <robert@fedoraproject.org> 2.11.6-1
- Upstream released 2.11.6

* Tue Apr 22 2008 Robert Scheck <robert@fedoraproject.org> 2.11.5.2-1
- Upstream released 2.11.5.2 (#443683)

* Sat Mar 29 2008 Robert Scheck <robert@fedoraproject.org> 2.11.5.1-1
- Upstream released 2.11.5.1

* Mon Mar 03 2008 Robert Scheck <robert@fedoraproject.org> 2.11.5-1
- Upstream released 2.11.5

* Sun Jan 13 2008 Robert Scheck <robert@fedoraproject.org> 2.11.4-1
- Upstream released 2.11.4
- Corrected mod_security example in configuration file (#427119)

* Sun Dec 09 2007 Robert Scheck <robert@fedoraproject.org> 2.11.3-1
- Upstream released 2.11.3
- Removed the RPM scriptlets doing httpd restarts (#227025)
- Patched an information disclosure known as CVE-2007-0095 (#221694)
- Provide virtual phpmyadmin package and a httpd alias (#231431)

* Wed Nov 21 2007 Robert Scheck <robert@fedoraproject.org> 2.11.2.2-1
- Upstream released 2.11.2.2 (#393771)

* Tue Nov 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.2.1-1
- Upstream released new version

* Mon Oct 29 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.2-1
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

* Fri Apr 07 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.3-1
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
