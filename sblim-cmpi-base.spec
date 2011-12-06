%define tog_pegasus_version 2:2.5.1
%define provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-base
Version:        1.6.0
Release:        1%{?dist}
Summary:        SBLIM CMPI Base Providers

Group:          Applications/System
License:        EPL
URL:            http://sblim.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  tog-pegasus-devel >= %{tog_pegasus_version}
Requires:       tog-pegasus >= %{tog_pegasus_version}

%description
SBLIM (Standards Based Linux Instrumentation for Manageability)
CMPI (Common Manageability Programming Interface) Base Providers
for System-Related CIM (Common Information Model) classes.

%package devel
Summary: SBLIM CMPI Base Providers Development Header Files
Group: Development/Libraries
BuildRequires: tog-pegasus-devel >= %{tog_pegasus_version}
Requires: %{name} = %{version}-%{release}

%description devel
SBLIM (Standards Based Linux Instrumentation for Manageability)
CMPI (Common Manageability Programming Interface) Base Provider
development header files and link libraries.

%package test
Summary: SBLIM CMPI Base Providers Test Cases
Group: Applications/System
BuildRequires: tog-pegasus-devel >= %{tog_pegasus_version}
Requires: %{name} = %{version}-%{release}
Requires: sblim-testsuite

%description test
SBLIM (Standards Based Linux Instrumentation for Manageability)
CMPI (Common Manageability Programming Interface) Base Provider
Testcase Files for the SBLIM Testsuite.

%prep
%setup -q

%build
%configure TESTSUITEDIR=%{_datadir}/sblim-testsuite \
           PROVIDERDIR=%{provider_dir} \
           CIMSERVER=pegasus
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cp -fp *OSBase_UnixProcess.h $RPM_BUILD_ROOT/%{_includedir}/sblim
chmod 644 $RPM_BUILD_ROOT/%{_includedir}/sblim/*OSBase_UnixProcess.h
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/cmpi/*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%docdir %{_datadir}/doc/%{name}-%{version}
%{_datadir}/doc/%{name}-%{version}
%{_datadir}/%{name}
%{_libdir}/*.so.*
%{provider_dir}/*.so*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so

%files test
%defattr(-,root,root,-)
%{_datadir}/sblim-testsuite

%pre
%define SCHEMA %{_datadir}/%{name}/Linux_Base.mof
%define REGISTRATION %{_datadir}/%{name}/Linux_Base.registration
# If upgrading, deregister old version
if [ $1 -gt 1 ]
then
  %{_datadir}/%{name}/provider-register.sh \
        -d -t pegasus \
        -m %{SCHEMA} \
        -r %{REGISTRATION} > /dev/null  2>&1 || :;
  # don't let registration failure when server not running fail upgrade!
fi

%post
/sbin/ldconfig
if [ $1 -ge 1 ]
then
# Register Schema and Provider - this is higly provider specific
  %{_datadir}/%{name}/provider-register.sh \
        -t pegasus \
        -m %{SCHEMA} \
        -r %{REGISTRATION} > /dev/null  2>&1 || :;
  # don't let registration failure when server not running fail install!
fi

%preun
# Deregister only if not upgrading 
if [ $1 -eq 0 ]
then
  %{_datadir}/%{name}/provider-register.sh \
        -d -t pegasus \
        -m %{SCHEMA} \
        -r %{REGISTRATION} > /dev/null  2>&1 || :;
  # don't let registration failure when server not running fail erase!
fi

%postun -p /sbin/ldconfig

%changelog
* Wed Jun 30 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.0-1
- Update to sblim-cmpi-base-1.6.0

* Thu Aug 27 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.9-1
- Update to 1.5.9

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.7-2
- Fix %%files (to be able build -devel dependent packages)
- Remove rpath from libraries
- Spec file cleanup, rpmlint check

* Fri Oct 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.7-1
- Update to 1.5.7
  Resolves: #468325

* Wed Jul  2 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.5-2
- Fix testsuite dependency

* Tue Jul  1 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.5.5-1
- Update to 1.5.5
- Spec file revision

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.4-8
- Autorebuild for GCC 4.3

* Tue Dec 05 2006 Mark Hamzy <hamzy@us.ibm.com> - 1.5.4-7
- Ignore failures when running provider-register.sh.  cimserver may be down

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.5.4-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Nov 10 2005  <mihajlov@de.ibm.com> - 1.5.4-3
- suppress error output in post scriptlets

* Wed Oct 27 2005  <mihajlov@de.ibm.com> - 1.5.4-2
- went back to original provider dir location as FC5 pegasus 2.5.1 support
  /usr/lib[64]/cmpi

* Wed Oct 12 2005  <mihajlov@de.ibm.com> - 1.5.4-1
- new spec file specifically for Fedora/RedHat

* Wed Jul 20 2005 Mark Hamzy <hamzy@us.ibm.com> - 1.5.3-1
- initial support
