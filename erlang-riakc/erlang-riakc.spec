
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riakc
%global debug_package %{nil}

Name:           erlang-%{realname}
Version:        2.4.1
Release:        1%{?dist}
Summary:        Erlang clients for Riak
Group:          Development/Libraries
License:        GPLv3+
URL:            https://github.com/basho/riak-erlang-client/
# wget --content-disposition https://github.com/basho/riak-erlang-client/archive/2.4.1.tar.gz
Source0:        riak-erlang-client-%{version}.tar.gz

Patch2:         basho-riak-erlang-client-d224a82-tests.patch

BuildRequires:  erlang-hamcrest >= 0.3
BuildRequires:  erlang-meck >= 0.1
BuildRequires:  erlang-protobuffs >= 0.8
BuildRequires:  erlang-rebar
BuildRequires:  erlang-riak_pb >= 2.1.4

Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
# Error:erlang(cover:compile_beam/2)
# Error:erlang(cover:get_term/1)
# Error:erlang(cover:write/2)
Requires:       erlang-tools%{?_isa}


%description
Erlang clients for Riak

%prep
%setup -q -n riak-erlang-client-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src

%patch2 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rebar skip_deps=true eunit -v


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl

%changelog
* Sun May 17 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.1-1
- First package