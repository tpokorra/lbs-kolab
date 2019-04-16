%if 0%{?fedora} || 0%{?epel} || 0%{?rhel} > 7
%global with_python3 1
%endif

Name:           python-icalendar
Version:        4.0.3
Release:        2%{?dist}
Summary:        Parser/generator of iCalendar files following the RFC 2445

License:        BSD
URL:            http://pypi.python.org/pypi/icalendar
Source0:        https://github.com/collective/icalendar/archive/%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python2-pytz
BuildRequires:  python2-dateutil
BuildRequires:  python2-hypothesis
BuildRequires:  python2-pytest
%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytz
BuildRequires:  python%{python3_pkgversion}-dateutil
BuildRequires:  python%{python3_pkgversion}-hypothesis
BuildRequires:  python%{python3_pkgversion}-pytest
%endif # if with_python3

%global _description\
iCalendar specification (RFC 2445) defines calendaring format used\
by many applications (Zimbra, Thunderbird and others). This\
module is a parser/generator of iCalendar files for use with\
Python. It follows the RFC 2445 (iCalendar) specification.\
The aim is to make a package that is fully compliant with RFC 2445,\
well designed, simple to use and well documented.\


%description %_description

%package -n python2-icalendar
Summary: %summary
Requires:       python2-pytz
Requires:       python2-dateutil
%{?python_provide:%python_provide python2-icalendar}

%description -n python2-icalendar %_description

%if 0%{?with_python3}
%package -n python3-icalendar
Summary:        Parser/generator of iCalendar files following the RFC 2445 for Python 3
Requires:       python3-pytz
Requires:       python3-dateutil

%description -n python3-icalendar
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.
%endif # with_python3

%prep
%setup -q -n icalendar-%{version}%{?veradd}

# we have only 2.7 and 3.3
sed -i 's/py26,//' tox.ini

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%{__sed} -i -e '/@unittest.expectedFailure/d' %{py3dir}/src/icalendar/tests/test_timezoned.py
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3


%check
%{__python2} -m pytest src/icalendar/tests

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} -m pytest src/icalendar/tests
popd
%endif

%files -n python2-icalendar
%doc README.rst CHANGES.rst LICENSE.rst
%{python2_sitelib}/icalendar
%{python2_sitelib}/*.egg-info
%if ! 0%{?with_python3}
%{_bindir}/icalendar
%endif

%if 0%{?with_python3}
%files -n python3-icalendar
%doc README.rst CHANGES.rst LICENSE.rst
%{python3_sitelib}/icalendar
%{python3_sitelib}/*.egg-info
%{_bindir}/icalendar
%endif # with_python3

%changelog
* Wed Mar 06 2019 Yatin Karel <ykarel@redhat.com> - 4.0.3-2
- Drop unnecessary BR on python-pip
- Enable python3 build on RHEL > 7
- Include icalendar binary in py2 package when py3 disabled

* Thu Jan 31 2019 Gwyn Ciesla <limburgher@gmail.com> 4.0.3-1
- 4.0.3

* Wed Jul 25 2018 Gwyn Ciesla <limburgher@gmail.com> - 3.11.5-9
- Fix FTBFS.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.11.5-7
- Rebuilt for Python 3.7

* Mon May 07 2018 Miro Hrončok <mhroncok@redhat.com> - 3.11.5-6
- Drop tox dependency, use pytest directly
- Use python2 instead of python

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.11.5-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.11.5-3
- Python 2 binary package renamed to python2-icalendar
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 3.11.5-1
- Upstream 3.11.5 (multiple bugfixes)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.11-2
- Rebuild for Python 3.6

* Fri Dec 09 2016 Jon Ciesla <limburgher@gmail.com> - 3.11-1
- 3.11

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 28 2015 Jon Ciesla <limburgher@gmail.com> - 3.9.0-1
- Latest upstream, BZ 1206758.

* Tue Jan 20 2015 Jon Ciesla <limburgher@gmail.com> - 3.8.4-1
- Latest upstream.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Apr 24 2014 Jon Ciesla <limburgher@gmail.com> - 3.6.2-1
- Latest upstream.

* Tue Jan 07 2014 Stanislav Ochotnicky <sochotnicky@rdhat.com> - 3.6.1-1
- Update to latest upstream
- Add python3 subpackage

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-2
- Install LICENSE file as well

* Thu May 30 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-1
- Update to latest upstream version (#824323)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-0.3.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-0.2.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.1-0.1.b2
- Update to 3.0b2
- Change license to BSD (see https://github.com/collective/icalendar/issues/2)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug  5 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-3
- Install examples
- Fix tests for Python 2.7 and run them
- Add GPLv2 for parser.py to licenses

* Wed Aug  4 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-2
- State correct licenses

* Tue Aug  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-1
- Initial package version
