# Put the RPM in the current directory.
%define _rpmdir .
# Find the tarball produced by `make dist' in the current directory.
%define _sourcedir %(echo $PWD)

Name:		opentsdb
Version:	2.0.0
Release:	1
Summary:	A scalable, distributed Time Series Database
Packager:	opentsdb@googlegroups.com
BuildArch:	noarch
Group:		Service/Monitoring
License:	LGPLv2.1+
URL:		http://opentsdb.net
Source:		opentsdb-2.0.0.tar.gz

Requires:	gnuplot

# Disable the stupid stuff rpm distros include in the build process by
# default:
#   Disable any prep shell actions. replace them with simply 'true'
%define __spec_prep_pre true
%define __spec_prep_post true
#   Disable any build shell actions. replace them with simply 'true'
%define __spec_build_pre cd %{_builddir}
%define __spec_build_post true
#   Disable any install shell actions. replace them with simply 'true'
%define __spec_install_pre cd %{_builddir}
%define __spec_install_post true
#   Disable any clean shell actions. replace them with simply 'true'
%define __spec_clean_pre cd %{_builddir}
%define __spec_clean_post true


%description
OpenTSDB is a distributed, scalable Time Series Database (TSDB) written on top
of HBase. OpenTSDB was written to address a common need: store, index and
serve metrics collected from computer systems (network gear, operating
systems, applications) at a large scale, and make this data easily accessible
and graphable.

Thanks to HBase's scalability, OpenTSDB allows you to collect many thousands
of metrics from thousands of hosts and applications, at a high rate (every few
seconds). OpenTSDB will never delete or downsample data and can easily store
billions of data points.

%prep
%setup -q


%build
%configure
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/var/cache/opentsdb


%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_datarootdir}/opentsdb/*.sh
%doc
%{_datarootdir}/opentsdb
%{_bindir}/tsdb
%dir %{_localstatedir}/cache/opentsdb


%changelog

